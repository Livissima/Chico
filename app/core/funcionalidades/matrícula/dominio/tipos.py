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
    """Natureza do dado. Define máscara, validação e formatação do campo."""

    TEXTO = "str"
    DATA = "date"
    NASCIMENTO = "nascimento"  # data + exibição da idade ao lado do campo
    CPF = "cpf"
    TELEFONE = "telefone"
    CEP = "cep"

    @property
    def tipo_js(self) -> str:
        """Valor de `data-tipo` lido pelo scripts.js (nascimento se comporta como data)."""
        return "date" if self is TipoDado.NASCIMENTO else self.value

    @property
    def mostra_idade(self) -> bool:
        return self is TipoDado.NASCIMENTO

    @property
    def placeholder(self) -> str | None:
        return _PLACEHOLDERS.get(self)


_PLACEHOLDERS: dict[TipoDado, str] = {
    TipoDado.CPF: "000.000.000-00",
    TipoDado.DATA: "DD/MM/AAAA",
    TipoDado.NASCIMENTO: "DD/MM/AAAA",
    TipoDado.TELEFONE: "(00) 00000 0000",
    TipoDado.CEP: "00000-000",
}
