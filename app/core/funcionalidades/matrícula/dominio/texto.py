"""Funções de texto e de data usadas pelo domínio."""
from __future__ import annotations

import re
import unicodedata
from datetime import date, datetime
from typing import Any


def slug(texto: str) -> str:
    """'Baixa Visão' -> 'baixa_visao'."""
    sem_acento = unicodedata.normalize("NFKD", texto).encode("ascii", "ignore").decode("ascii")
    return re.sub(r"[^a-z0-9]+", "_", sem_acento.lower()).strip("_")


def é_coleção(valor: Any) -> bool:
    return isinstance(valor, (list, tuple, set, frozenset))


def normalizar_valor(valor: Any) -> str:
    """Converte o que veio do formulário (None, str ou lista) em str já sem espaços nas pontas."""
    if valor is None:
        return ""
    if é_coleção(valor):
        return ", ".join(t for t in (str(v).strip() for v in valor) if t)
    return str(valor).strip()


def só_dígitos(texto: str) -> str:
    return re.sub(r"\D", "", texto)


def hoje() -> str:
    """Data de hoje como 'dd/mm/aaaa'. Pode ser usada como `valor_padrao` (é chamada a cada
    carregamento do formulário, então não fica velha se o app ficar ligado de um dia para o outro)."""
    return datetime.now().strftime("%d/%m/%Y")


def analisar_data(texto: str, ano_minimo: int = 1900, ano_maximo: int | None = None) -> date | None:
    """'dd/mm/aaaa' -> date, ou None se o texto não for uma data real dentro do intervalo de anos."""
    ano_maximo = ano_maximo or date.today().year
    achado = re.fullmatch(r"(\d{2})/(\d{2})/(\d{4})", texto.strip())
    if not achado:
        return None
    dia, mes, ano = (int(g) for g in achado.groups())
    if not ano_minimo <= ano <= ano_maximo:
        return None
    try:
        return date(ano, mes, dia)
    except ValueError:
        return None
