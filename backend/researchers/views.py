import threading

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import LattesReportRun
from .lattes_runner import (
    InvalidLattesIdError,
    parse_extra_ids,
    run_scriptlattes,
)

# Dados fictícios simulando o retorno de uma busca via scriptLattes.
# TODO: substituir por integração real com o crawler scriptLattes.
MOCK_AUTHORS = [
    {
        "id": 1,
        "name": "Jorge Lima de Magalhães",
        "lattes_id": "9829199474735249",
        "lattes_url": "http://lattes.cnpq.br/9829199474735249",
        "institution": "Fiocruz - Farmanguinhos",
        "interests": [
            "inteligência competitiva",
            "inovação tecnológica",
            "saúde pública",
            "prospecção tecnológica",
        ],
    },
    {
        "id": 2,
        "name": "Carla Cristina de Freitas da Silveira",
        "lattes_id": "0896415734552449",
        "lattes_url": "http://lattes.cnpq.br/0896415734552449",
        "institution": "Fiocruz - Farmanguinhos",
        "interests": [
            "propriedade intelectual",
            "gestão da inovação",
            "saúde coletiva",
        ],
    },
    {
        "id": 3,
        "name": "Renata Oliveira Fagundes",
        "lattes_id": "4854637109722444",
        "lattes_url": "http://lattes.cnpq.br/4854637109722444",
        "institution": "Fiocruz - Farmanguinhos",
        "interests": [
            "indústria farmacêutica",
            "pesquisa e desenvolvimento",
            "engenharia de produção",
        ],
    },
    {
        "id": 4,
        "name": "Henrique Koch Chaves",
        "lattes_id": "2605608269201041",
        "lattes_url": "http://lattes.cnpq.br/2605608269201041",
        "institution": "Instituto Nacional de Cardiologia",
        "interests": [
            "química analítica",
            "radiofármacos",
            "economia da saúde",
        ],
    },
    {
        "id": 5,
        "name": "Edson Ferreira da Silva",
        "lattes_id": "1471443262299422",
        "lattes_url": "http://lattes.cnpq.br/1471443262299422",
        "institution": "Universidade Federal do Rio de Janeiro",
        "interests": [
            "química orgânica",
            "química medicinal",
            "cromatografia gasosa",
        ],
    },
    {
        "id": 6,
        "name": "Denize Gomes Maranhão",
        "lattes_id": "1795725319151820",
        "lattes_url": "http://lattes.cnpq.br/1795725319151820",
        "institution": "Fiocruz - Farmanguinhos",
        "interests": [
            "arquivologia",
            "gestão da informação",
        ],
    },
    {
        "id": 7,
        "name": "Carlos Eduardo Collazo Pontes",
        "lattes_id": "0359870978393939",
        "lattes_url": "http://lattes.cnpq.br/0359870978393939",
        "institution": "Fiocruz - Farmanguinhos",
        "interests": [
            "saúde pública",
            "gestão estratégica",
            "inovação tecnológica",
        ],
    },
]


class ResearcherSearchView(APIView):
    """Busca simulada de autores/pesquisadores por tema ou palavra-chave."""

    def get(self, request, *args, **kwargs):
        query = request.query_params.get("q", "").strip()
        query_lower = query.lower()

        if query_lower:
            results = []
            for author in MOCK_AUTHORS:
                matched_interests = [
                    interest
                    for interest in author["interests"]
                    if query_lower in interest.lower()
                ]
                name_matches = query_lower in author["name"].lower()
                if matched_interests or name_matches:
                    results.append({**author, "matched_interests": matched_interests})
        else:
            results = [{**author, "matched_interests": []} for author in MOCK_AUTHORS]

        return Response(
            {
                "query": query,
                "count": len(results),
                "results": results,
            }
        )


def _run_lattes_report_in_background(run_id):
    try:
        run = LattesReportRun.objects.get(pk=run_id)
        result = run_scriptlattes(run.extra_ids)
        run.status = LattesReportRun.STATUS_DONE
        run.log = result["log"]
        run.ignored_duplicate_ids = result["ignored_duplicate_ids"]
    except Exception as exc:  # noqa: BLE001 - queremos capturar qualquer falha do subprocess
        run.status = LattesReportRun.STATUS_FAILED
        run.error = str(exc)
    finally:
        run.save()


class LattesReportTriggerView(APIView):
    """Dispara a execução do scriptLattes com os membros de Farmanguinhos + IDs extras."""

    def post(self, request, *args, **kwargs):
        if LattesReportRun.objects.filter(
            status__in=[LattesReportRun.STATUS_PENDING, LattesReportRun.STATUS_RUNNING]
        ).exists():
            return Response(
                {"detail": "Já existe uma execução do scriptLattes em andamento."},
                status=status.HTTP_409_CONFLICT,
            )

        raw_ids = request.data.get("extra_ids", [])
        if not isinstance(raw_ids, list):
            return Response(
                {"detail": "extra_ids deve ser uma lista de IDs Lattes."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            extra_ids = parse_extra_ids(raw_ids)
        except InvalidLattesIdError as exc:
            return Response({"detail": str(exc)}, status=status.HTTP_400_BAD_REQUEST)

        run = LattesReportRun.objects.create(
            status=LattesReportRun.STATUS_RUNNING, extra_ids=extra_ids
        )
        thread = threading.Thread(
            target=_run_lattes_report_in_background, args=(run.pk,), daemon=True
        )
        thread.start()

        return Response(
            {"run_id": run.pk, "status": run.status, "extra_ids": extra_ids},
            status=status.HTTP_202_ACCEPTED,
        )


class LattesReportStatusView(APIView):
    """Consulta o status da última execução do scriptLattes."""

    def get(self, request, *args, **kwargs):
        run = LattesReportRun.objects.first()
        if run is None:
            return Response({"status": "never_run"})

        return Response(
            {
                "run_id": run.pk,
                "status": run.status,
                "extra_ids": run.extra_ids,
                "ignored_duplicate_ids": run.ignored_duplicate_ids,
                "log": run.log,
                "error": run.error,
                "created_at": run.created_at,
                "updated_at": run.updated_at,
                "report_url": "/media/lattes_report/index.html"
                if run.status == LattesReportRun.STATUS_DONE
                else None,
            }
        )
