"""Enumerações do domínio do formulário."""
from __future__ import annotations

from enum import StrEnum


class TipoCampo(StrEnum):
    """Como o campo é desenhado. O valor é o nome do template em templates/campos/."""

    TEXTO = "texto"
    SELECT = "select"
    RADIO = "radio"
    MULTISELECT = "multiselect"


class TipoDado(StrEnum):
    """Natureza do dado. O valor é o que o scripts.js lê em `data-tipo`."""

    TEXTO = "str"
    DATA = "date"
    CPF = "cpf"
    TELEFONE = "telefone"

    @property
    def placeholder(self) -> str | None:
        return _PLACEHOLDERS.get(self)


_PLACEHOLDERS: dict[TipoDado, str] = {
    TipoDado.CPF: "000.000.000-00",
    TipoDado.DATA: "DD/MM/AAAA",
    TipoDado.TELEFONE: "(00) 00000-0000",
}
