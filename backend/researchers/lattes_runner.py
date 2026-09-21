"""Lógica de junção/validação de IDs Lattes e execução do scriptLattes vendorizado."""
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
VENDOR_DIR = BASE_DIR / "vendor"
MEDIA_ROOT = BASE_DIR / "media"
REPORT_OUTPUT_DIR = MEDIA_ROOT / "lattes_report"

LATTES_ID_RE = re.compile(r"^\d{16}$")

# Membros de Farmanguinhos processados hoje (extraído de nitfar.list).
FARMANGUINHOS_MEMBERS = [
    ("9829199474735249", "Jorge Lima de Magalhães"),
    ("0896415734552449", "Carla Cristina de Freitas da Silveira"),
    ("4854637109722444", "Renata Oliveira Fagundes"),
    ("2605608269201041", "Henrique Koch Chaves"),
    ("1471443262299422", "Edson Ferreira da Silva"),
    ("1795725319151820", "Denize Gomes Maranhão"),
    ("0359870978393939", "Carlos Eduardo Collazo Pontes"),
]

CONFIG_TEMPLATE = """\
global-nome_do_grupo                      = NIT-Far
global-arquivo_de_entrada                 = {lista_path}
global-diretorio_de_saida                 = {saida_path}
global-email_do_admin                     = admin@email.com
global-idioma                             = PT
global-itens_desde_o_ano                  = 1900
global-itens_ate_o_ano                    = 2100
global-itens_por_pagina                   = 5000

relatorio-incluir_artigo_em_periodico                  = sim
relatorio-incluir_livro_publicado                      = sim
relatorio-incluir_capitulo_de_livro_publicado          = sim
relatorio-incluir_texto_em_jornal_de_noticia           = sim
relatorio-incluir_trabalho_completo_em_congresso       = sim
relatorio-incluir_resumo_expandido_em_congresso        = sim
relatorio-incluir_resumo_em_congresso                  = sim
relatorio-incluir_artigo_aceito_para_publicacao        = sim
relatorio-incluir_apresentacao_de_trabalho             = sim
relatorio-incluir_outro_tipo_de_producao_bibliografica = sim

relatorio-incluir_software_com_registro                = sim
relatorio-incluir_software_sem_registro                = sim
relatorio-incluir_produto_tecnologico                  = sim
relatorio-incluir_processo_ou_tecnica                  = sim
relatorio-incluir_trabalho_tecnico                     = sim
relatorio-incluir_outro_tipo_de_producao_tecnica       = sim
relatorio-incluir_entrevista_mesas_e_comentarios       = sim

relatorio-incluir_producao_artistica                   = sim

relatorio-mostrar_orientacoes                                          = sim
relatorio-incluir_orientacao_em_andamento_pos_doutorado                = sim
relatorio-incluir_orientacao_em_andamento_doutorado                    = sim
relatorio-incluir_orientacao_em_andamento_mestrado                     = sim
relatorio-incluir_orientacao_em_andamento_monografia_de_especializacao = sim
relatorio-incluir_orientacao_em_andamento_tcc                          = sim
relatorio-incluir_orientacao_em_andamento_iniciacao_cientifica         = sim
relatorio-incluir_orientacao_em_andamento_outro_tipo                   = sim
relatorio-incluir_orientacao_concluida_pos_doutorado                   = sim
relatorio-incluir_orientacao_concluida_doutorado                       = sim
relatorio-incluir_orientacao_concluida_mestrado                        = sim
relatorio-incluir_orientacao_concluida_monografia_de_especializacao    = sim
relatorio-incluir_orientacao_concluida_tcc                             = sim
relatorio-incluir_orientacao_concluida_iniciacao_cientifica            = sim
relatorio-incluir_orientacao_concluida_outro_tipo                      = sim

relatorio-incluir_projeto                = sim
relatorio-incluir_premio                 = sim
relatorio-incluir_participacao_em_evento = sim
relatorio-incluir_organizacao_de_evento  = sim

grafo-mostrar_grafo_de_colaboracoes                         = sim
grafo-mostrar_todos_os_nos_do_grafo                         = sim
grafo-considerar_rotulos_dos_membros_do_grupo               = nao

grafo-incluir_artigo_em_periodico                           = sim
grafo-incluir_livro_publicado                               = sim
grafo-incluir_capitulo_de_livro_publicado                   = sim
grafo-incluir_texto_em_jornal_de_noticia                    = sim
grafo-incluir_trabalho_completo_em_congresso                = sim
grafo-incluir_resumo_expandido_em_congresso                 = sim
grafo-incluir_resumo_em_congresso                           = sim
grafo-incluir_artigo_aceito_para_publicacao                 = sim
grafo-incluir_apresentacao_de_trabalho                      = sim
grafo-incluir_outro_tipo_de_producao_bibliografica          = sim

grafo-incluir_software_com_registro                         = sim
grafo-incluir_software_sem_registro                         = sim
grafo-incluir_produto_tecnologico                           = sim
grafo-incluir_processo_ou_tecnica                           = sim
grafo-incluir_trabalho_tecnico                              = sim
grafo-incluir_outro_tipo_de_producao_tecnica                = sim
grafo-incluir_entrevista_mesas_e_comentarios                = sim

grafo-incluir_producao_artistica                            = sim

relatorio-incluir_metricas           = sim
"""


class InvalidLattesIdError(ValueError):
    pass


def normalize_lattes_id(raw):
    candidate = re.sub(r"\D", "", raw or "")
    if not LATTES_ID_RE.match(candidate):
        raise InvalidLattesIdError(
            f"ID Lattes inválido: '{raw}'. Deve conter 16 dígitos numéricos."
        )
    return candidate


def parse_extra_ids(raw_ids):
    """Recebe uma lista de strings (uma por ID, possivelmente com nome junto) e
    retorna uma lista normalizada e validada, preservando a ordem e sem repetir."""
    seen = set()
    result = []
    for raw in raw_ids:
        raw = (raw or "").strip()
        if not raw:
            continue
        lattes_id = normalize_lattes_id(raw)
        if lattes_id in seen:
            continue
        seen.add(lattes_id)
        result.append(lattes_id)
    return result


def merge_members(extra_ids):
    """Junta os membros fixos de Farmanguinhos com os IDs extras, sem duplicar.

    Retorna (membros, ids_ignorados) onde membros é uma lista de (id, nome) e
    ids_ignorados são os extras que já existiam entre os membros fixos.
    """
    fixed_ids = {member_id for member_id, _ in FARMANGUINHOS_MEMBERS}
    members = list(FARMANGUINHOS_MEMBERS)
    ignored = []
    added = set()
    for lattes_id in extra_ids:
        if lattes_id in fixed_ids or lattes_id in added:
            ignored.append(lattes_id)
            continue
        members.append((lattes_id, f"Membro externo {lattes_id}"))
        added.add(lattes_id)
    return members, ignored


def build_list_file(members, path):
    with open(path, "w", encoding="utf-8") as fh:
        for lattes_id, nome in members:
            fh.write(f"{lattes_id} , {nome}\n")


def build_config_file(list_path, output_dir, config_path):
    content = CONFIG_TEMPLATE.format(lista_path=list_path, saida_path=output_dir)
    with open(config_path, "w", encoding="utf-8") as fh:
        fh.write(content)


def run_scriptlattes(extra_ids, timeout_seconds=3600):
    """Executa o scriptLattes com os membros de Farmanguinhos + IDs extras.

    Roda de forma síncrona (bloqueante) num processo separado; o chamador
    (view) deve invocar isto numa thread de background.

    Retorna dict com: members, ignored_duplicate_ids, log, returncode.
    Lança RuntimeError se o scriptLattes não existir ou o subprocess falhar.
    """
    if not (VENDOR_DIR / "scriptLattes.py").exists():
        raise RuntimeError("scriptLattes não encontrado em backend/vendor.")

    members, ignored = merge_members(extra_ids)

    with tempfile.TemporaryDirectory(prefix="lattes_run_") as tmp:
        tmp_path = Path(tmp)
        list_path = tmp_path / "membros.list"
        saida_path = tmp_path / "saida"
        saida_path.mkdir(parents=True, exist_ok=True)
        config_path = tmp_path / "run.config"

        build_list_file(members, list_path)
        build_config_file(list_path, saida_path, config_path)

        env = os.environ.copy()
        env.setdefault("SCRIPTLATTES_CHROMEDRIVER_PATH", "/usr/bin/chromedriver")
        env.setdefault("SCRIPTLATTES_CHROME_BINARY", "/usr/bin/chromium")

        process = subprocess.run(
            [sys.executable, "scriptLattes.py", str(config_path)],
            cwd=str(VENDOR_DIR),
            env=env,
            capture_output=True,
            text=True,
            timeout=timeout_seconds,
        )

        log = (process.stdout or "") + "\n" + (process.stderr or "")

        if process.returncode != 0:
            raise RuntimeError(
                f"scriptLattes terminou com código {process.returncode}.\n{log}"
            )

        if REPORT_OUTPUT_DIR.exists():
            shutil.rmtree(REPORT_OUTPUT_DIR)
        MEDIA_ROOT.mkdir(parents=True, exist_ok=True)
        shutil.copytree(saida_path, REPORT_OUTPUT_DIR)

    return {
        "members": members,
        "ignored_duplicate_ids": ignored,
        "log": log,
        "returncode": process.returncode,
    }
