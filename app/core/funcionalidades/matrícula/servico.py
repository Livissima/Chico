"""Caso de uso: validar os dados enviados e gerar a ficha de matrícula.

Este módulo não importa Streamlit nem Jinja: depende apenas das "portas" abaixo, o que
permite testá-lo sem navegador e trocar as implementações sem mexer aqui.
"""
from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any, Mapping, Protocol

from .dominio.campos import Esquema
from .dominio.contexto import ConstrutorDeContexto


class Renderizador(Protocol):
    def renderizar(self, template: str, contexto: Mapping[str, Any]) -> str: ...


class FormularioUI(Protocol):
    def coletar(self) -> dict[str, Any] | None: ...


@dataclass(frozen=True)
class ResultadoFicha:
    html: str | None = None
    erros: tuple[str, ...] = ()

    @property
    def valido(self) -> bool:
        return not self.erros


class ServicoFicha:
    def __init__(
        self,
        esquema: Esquema,
        construtor_contexto: ConstrutorDeContexto,
        renderizador: Renderizador,
        template_ficha: str = "pagina_print.html",
    ) -> None:
        self._esquema = esquema
        self._construtor_contexto = construtor_contexto
        self._renderizador = renderizador
        self._template_ficha = template_ficha

    def gerar(self, dados: Mapping[str, Any]) -> ResultadoFicha:
        erros = self._esquema.validar(dados)
        if erros:
            return ResultadoFicha(erros=tuple(erros))
        contexto = self._construtor_contexto.construir(self._esquema, dados)
        return ResultadoFicha(html=self._renderizador.renderizar(self._template_ficha, contexto))

    @staticmethod
    def nome_arquivo(dados: Mapping[str, Any]) -> str:
        nome = str(dados.get("nome_estudante") or "Estudante").strip()
        seguro = re.sub(r"[^\w-]+", "_", nome).strip("_") or "Estudante"
        return f"Ficha_{seguro}.html"
