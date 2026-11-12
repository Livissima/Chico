"""Formatação dos valores por tipo de dado.

Cada valor tem três apresentações:
  formulario : como aparece no campo do formulário (com máscara)
  ficha      : como aparece na ficha impressa (HTML/PDF)
  json       : como é gravado no arquivo .json

Para criar um formato novo: herde de `Formato`, sobrescreva o que for diferente
e registre em `_FORMATOS`. Os tipos sem formato próprio ficam como o usuário digitou.
"""
from __future__ import annotations

from .telefone import TelefoneInvalido, interpretar_telefone
from .texto import só_dígitos
from .tipos import TipoDado


class Formato:
    def formulario(self, valor: str) -> str:
        return valor

    def ficha(self, valor: str) -> str:
        return self.formulario(valor)

    def json(self, valor: str) -> str:
        return self.formulario(valor)


class FormatoTelefone(Formato):
    """Completa DDD e o 9 extra. Valor que não for um telefone válido é devolvido sem mudança
    (quem acusa o erro é a regra TelefoneValido)."""

    @staticmethod
    def _interpretar(valor: str):
        if not valor:
            return None
        try:
            return interpretar_telefone(valor)
        except TelefoneInvalido:
            return None

    def formulario(self, valor):
        telefone = self._interpretar(valor)
        return telefone.formatar(" ") if telefone else valor

    def ficha(self, valor):
        telefone = self._interpretar(valor)
        return telefone.formatar("-") if telefone else valor

    def json(self, valor):
        telefone = self._interpretar(valor)
        return telefone.digitos if telefone else valor


class FormatoCep(Formato):
    def formulario(self, valor):
        digitos = só_dígitos(valor)
        return f"{digitos[:5]}-{digitos[5:]}" if len(digitos) == 8 else valor


_SEM_FORMATO = Formato()

_FORMATOS: dict[TipoDado, Formato] = {
    TipoDado.TELEFONE: FormatoTelefone(),
    TipoDado.CEP: FormatoCep(),
}


def formato_de(tipo_dado: TipoDado) -> Formato:
    return _FORMATOS.get(tipo_dado, _SEM_FORMATO)
