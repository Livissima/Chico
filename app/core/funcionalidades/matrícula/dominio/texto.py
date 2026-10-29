"""Funções puras de texto usadas pelo domínio."""
from __future__ import annotations

import re
import unicodedata
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
