"""Caso de uso: validar os dados enviados e gerar a ficha de matrícula (PDF) e o JSON dos dados.

Este módulo não importa Streamlit nem Jinja: depende apenas das "portas" abaixo, o que
permite testá-lo sem navegador e trocar as implementações sem mexer aqui.
"""
from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Callable, Mapping, Protocol

from .dominio.campos import Esquema
from .dominio.contexto import ConstrutorDeContexto
from .dominio.exportacao import dados_para_json, nome_base_arquivos
from .dominio.regras import Erro


class Renderizador(Protocol):
    def renderizar(self, template: str, contexto: Mapping[str, Any]) -> str: ...


class GeradorPdf(Protocol):
    def gerar(self, html: str) -> bytes: ...


class FormularioUI(Protocol):
    def coletar(self, erros: Mapping[str, str] | None = None, envio: Any = None) -> dict[str, Any] | None: ...


@dataclass(frozen=True)
class ResultadoFicha:
    html: str | None = None
    pdf: bytes | None = None
    json: str | None = None
    nome_base: str | None = None  # 'ddmmaaaa_HH-MM_Nome', sem extensão
    erros: tuple[Erro, ...] = ()

    @property
    def valido(self) -> bool:
        return not self.erros

    @property
    def mensagens(self) -> list[str]:
        return [erro.mensagem for erro in self.erros]

    @property
    def erros_por_campo(self) -> dict[str, str]:
        """chave do campo -> mensagem, para o formulário destacar os campos com problema."""
        return {chave: erro.mensagem for erro in self.erros for chave in erro.chaves}


class ServicoFicha:
    def __init__(
        self,
        esquema: Esquema,
        construtor_contexto: ConstrutorDeContexto,
        renderizador: Renderizador,
        gerador_pdf: GeradorPdf,
        template_ficha: str = "pagina_print.html",
        relogio: Callable[[], datetime] = datetime.now,
    ) -> None:
        self._esquema = esquema
        self._construtor_contexto = construtor_contexto
        self._renderizador = renderizador
        self._gerador_pdf = gerador_pdf
        self._template_ficha = template_ficha
        self._relogio = relogio

    def gerar(self, dados: Mapping[str, Any]) -> ResultadoFicha:
        """Valida e, se estiver tudo certo, devolve HTML, PDF e JSON com o mesmo carimbo de data/hora.
        Havendo qualquer erro (campo, CPF repetido, datas incoerentes, família...), nada é gerado."""
        preparados = self._esquema.preparar(dados)
        erros = self._esquema.validar(preparados)
        if erros:
            return ResultadoFicha(erros=tuple(erros))

        contexto = self._construtor_contexto.construir(self._esquema, preparados)
        html = self._renderizador.renderizar(self._template_ficha, contexto)
        return ResultadoFicha(
            html=html,
            pdf=self._gerador_pdf.gerar(html),
            json=json.dumps(dados_para_json(self._esquema, preparados), ensure_ascii=False, indent=2),
            nome_base=nome_base_arquivos(preparados.get("nome_estudante"), self._relogio()),
        )
