from rest_framework.views import APIView
from rest_framework.response import Response

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
