"""Regras de validação.

Cada regra é uma classe pequena e independente. Para criar uma regra nova basta
herdar de `Regra`; nenhuma outra classe precisa ser alterada.

Convenção: toda regra, exceto `Obrigatorio`, ignora valores vazios.
"""
from __future__ import annotations

import re
from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import date
from typing import TYPE_CHECKING

from .tipos import TipoDado

if TYPE_CHECKING:  # evita import circular em tempo de execução
    from .campos import Campo


class Regra(ABC):
    @abstractmethod
    def verificar(self, campo: "Campo", valor: str) -> str | None:
        """Devolve a mensagem de erro, ou None se o valor é aceitável."""

    def atributos_html(self) -> dict[str, str]:
        """Atributos que o <input> recebe para o JS aplicar máscara/limite no navegador."""
        return {}


# ---------------------------------------------------------------- regras básicas
@dataclass(frozen=True)
class Obrigatorio(Regra):
    def verificar(self, campo, valor):
        if not valor:
            return f"O campo {campo.rotulo} é obrigatório."
        return None


@dataclass(frozen=True)
class ComprimentoMinimo(Regra):
    n: int

    def verificar(self, campo, valor):
        if valor and len(valor) < self.n:
            return f"{campo.rotulo} deve ter no mínimo {self.n} caracteres. {len(valor)} inseridos."
        return None


@dataclass(frozen=True)
class ComprimentoMaximo(Regra):
    n: int

    def verificar(self, campo, valor):
        if valor and len(valor) > self.n:
            return f"{campo.rotulo} deve ter no máximo {self.n} caracteres. {len(valor)} inseridos."
        return None

    def atributos_html(self):
        return {"maxlength": str(self.n)}


_FORMATACAO = str.maketrans("", "", ".-/() ")


@dataclass(frozen=True)
class ApenasNumeros(Regra):
    """Aceita dígitos, ignorando a pontuação comum de CPF, data e telefone."""

    def verificar(self, campo, valor):
        limpo = valor.translate(_FORMATACAO)
        if valor and not (limpo.isascii() and limpo.isdigit()):
            return f"O campo {campo.rotulo} aceita apenas números."
        return None

    def atributos_html(self):
        return {"data-numeros": "true"}


@dataclass(frozen=True)
class ApenasLetras(Regra):
    """Aceita letras (com acento) e espaços."""

    def verificar(self, campo, valor):
        if valor and not all(c.isalpha() or c.isspace() for c in valor):
            return f"O campo {campo.rotulo} aceita apenas letras."
        return None

    def atributos_html(self):
        return {"data-letras": "true"}


# ------------------------------------------------------- regras por tipo de dado
def cpf_valido(texto: str) -> bool:
    digitos = re.sub(r"\D", "", texto)
    if len(digitos) != 11 or digitos == digitos[0] * 11:
        return False
    for tamanho in (9, 10):
        soma = sum(int(d) * peso for d, peso in zip(digitos[:tamanho], range(tamanho + 1, 1, -1)))
        resto = (soma * 10) % 11
        if resto == 10:
            resto = 0
        if resto != int(digitos[tamanho]):
            return False
    return True


def data_valida(texto: str, ano_minimo: int = 1900, ano_maximo: int | None = None) -> bool:
    ano_maximo = ano_maximo or date.today().year
    achado = re.fullmatch(r"(\d{2})/(\d{2})/(\d{4})", texto)
    if not achado:
        return False
    dia, mes, ano = (int(g) for g in achado.groups())
    if not ano_minimo <= ano <= ano_maximo:
        return False
    try:
        date(ano, mes, dia)
    except ValueError:
        return False
    return True


def telefone_valido(texto: str) -> bool:
    return len(re.sub(r"\D", "", texto)) in (10, 11)


@dataclass(frozen=True)
class CpfValido(Regra):
    def verificar(self, campo, valor):
        if valor and not cpf_valido(valor):
            return f"{campo.rotulo}: CPF inválido."
        return None


@dataclass(frozen=True)
class DataValida(Regra):
    def verificar(self, campo, valor):
        if valor and not data_valida(valor):
            return f"{campo.rotulo}: data inválida ou fora do intervalo."
        return None


@dataclass(frozen=True)
class TelefoneValido(Regra):
    def verificar(self, campo, valor):
        if valor and not telefone_valido(valor):
            return f"{campo.rotulo}: telefone incompleto."
        return None


_REGRA_POR_TIPO_DADO: dict[TipoDado, Regra] = {
    TipoDado.DATA: DataValida(),
    TipoDado.CPF: CpfValido(),
    TipoDado.TELEFONE: TelefoneValido(),
}


def regra_para(tipo_dado: TipoDado) -> Regra | None:
    """Regra aplicada automaticamente a todo campo daquele tipo de dado."""
    return _REGRA_POR_TIPO_DADO.get(tipo_dado)
