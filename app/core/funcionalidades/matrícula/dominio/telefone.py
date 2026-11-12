"""Interpretação, validação e formatação de telefones (contexto: Goiânia, DDD padrão 62).

Regras (iguais às do scripts.js, que repete esta lógica no navegador):
  8 dígitos : começa com 8 ou 9 -> celular sem o 9 extra (acrescenta DDD e 9); senão -> fixo (acrescenta DDD)
  9 dígitos : precisa começar com 98 ou 99 -> celular sem DDD (acrescenta DDD)
 10 dígitos : 3º dígito 8 ou 9 -> celular com DDD sem o 9 extra (acrescenta o 9); senão inválido
 11 dígitos : 3º dígito 9 e 4º dígito 8 ou 9 -> celular completo; senão inválido

Exceção: um fixo já formatado, '(62) 3208 9777' ou '(62) 3208-9777', é aceito como está. Sem isso, o valor
que o próprio sistema produz (10 dígitos, 3º dígito diferente de 8/9) seria rejeitado ao ser reprocessado.
A digitação crua '6232089777' continua inválida: fixo se digita só com os 8 dígitos.
"""
from __future__ import annotations

import re
from dataclasses import dataclass

from .texto import só_dígitos

DDD_PADRAO = "62"


class TelefoneInvalido(ValueError):
    """A mensagem já vem pronta para ser exibida ao usuário."""


@dataclass(frozen=True)
class Telefone:
    ddd: str
    numero: str  # 8 dígitos (fixo) ou 9 dígitos (celular, já com o 9 extra)

    @property
    def celular(self) -> bool:
        return len(self.numero) == 9

    @property
    def digitos(self) -> str:
        return self.ddd + self.numero

    def formatar(self, separador: str = " ") -> str:
        corte = 5 if self.celular else 4
        return f"({self.ddd}) {self.numero[:corte]}{separador}{self.numero[corte:]}"


def _conferir_ddd(ddd: str) -> None:
    if "0" in ddd:
        raise TelefoneInvalido("DDD inválido.")


_FIXO_FORMATADO = re.compile(r"\((\d{2})\) (\d{4})[ -](\d{4})")


def interpretar_telefone(texto: str, ddd_padrao: str = DDD_PADRAO) -> Telefone:
    if (fixo := _FIXO_FORMATADO.fullmatch(texto.strip())):
        _conferir_ddd(fixo.group(1))
        return Telefone(fixo.group(1), fixo.group(2) + fixo.group(3))

    digitos = só_dígitos(texto)
    quantidade = len(digitos)

    if quantidade == 8:
        if digitos[0] in "89":
            return Telefone(ddd_padrao, "9" + digitos)
        return Telefone(ddd_padrao, digitos)

    if quantidade == 9:
        if digitos[0] != "9" or digitos[1] not in "89":
            raise TelefoneInvalido("com 9 dígitos, o número deve começar com 98 ou 99.")
        return Telefone(ddd_padrao, digitos)

    if quantidade == 10:
        ddd, resto = digitos[:2], digitos[2:]
        if resto[0] not in "89":
            raise TelefoneInvalido(
                "com 10 dígitos o número deve ser celular com DDD (3º dígito 8 ou 9). "
                "Telefone fixo deve ser digitado só com 8 dígitos."
            )
        _conferir_ddd(ddd)
        return Telefone(ddd, "9" + resto)

    if quantidade == 11:
        ddd, resto = digitos[:2], digitos[2:]
        if resto[0] != "9" or resto[1] not in "89":
            raise TelefoneInvalido("com 11 dígitos, o 3º dígito deve ser 9 e o 4º deve ser 8 ou 9.")
        _conferir_ddd(ddd)
        return Telefone(ddd, resto)

    raise TelefoneInvalido("informe 8 dígitos (fixo ou celular sem DDD), 9, 10 ou 11 dígitos.")
