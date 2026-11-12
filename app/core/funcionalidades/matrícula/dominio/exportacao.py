"""Dados que saem do sistema: conteúdo do JSON e nome dos arquivos gerados."""
from __future__ import annotations

import re
from datetime import datetime
from typing import Any, Mapping

from .campos import Esquema

_PROIBIDOS_NO_WINDOWS = re.compile(r'[<>:"/\\|?*\x00-\x1f]')
_TAMANHO_MAXIMO_DO_NOME = 80


def dados_para_json(esquema: Esquema, dados: Mapping[str, Any]) -> dict[str, Any]:
    """Todas as chaves dos campos, na ordem do formulário. Vazio/oculto vira "" (ou [] no multiselect).

    Os valores seguem `Campo.para_json` (ex.: telefone só com números, já com DDD).
    """
    return {campo.chave: campo.para_json(dados.get(campo.chave)) for campo in esquema.campos()}


def nome_base_arquivos(nome: str | None, momento: datetime) -> str:
    """'05112026_15-30_Lívia Pereira Neves' (sem extensão).

    Mantém acentos e espaços do nome digitado; remove só o que o Windows não aceita em nomes de arquivo.
    """
    limpo = _PROIBIDOS_NO_WINDOWS.sub("", nome or "")
    limpo = re.sub(r"\s+", " ", limpo).strip(" .")[:_TAMANHO_MAXIMO_DO_NOME].strip(" .")
    return f"{momento:%d%m%Y_%H-%M}_{limpo or 'Estudante'}"
