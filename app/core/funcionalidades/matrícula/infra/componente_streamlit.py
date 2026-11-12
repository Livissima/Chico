"""Integração com o Streamlit: publica o formulário HTML como componente customizado."""
from __future__ import annotations

import inspect
import os
import sys
import threading
import types
from pathlib import Path
from typing import Any, Mapping

import streamlit.components.v1 as components

from app.core.funcionalidades.matrícula.infra.renderizador import RenderizadorJinja
from ..dominio.campos import Esquema

DIRETORIO_COMPONENTE = Path(__file__).resolve().parent / "component_form_dinamico"
_TRAVA = threading.Lock()


def _gravar_se_mudou(caminho: Path, conteudo: str) -> None:
    if caminho.exists() and caminho.read_text(encoding="utf-8") == conteudo:
        return
    temporario = caminho.with_suffix(".tmp")
    temporario.write_text(conteudo, encoding="utf-8")
    os.replace(temporario, caminho)  # troca atômica: nenhuma sessão lê arquivo pela metade


def _declarar_componente(nome: str, diretorio: Path):
    """Contorno herdado do código original.

    `declare_component` usa `inspect.getmodule()` do chamador e quebra quando ele devolve None.
    O patch é temporário e protegido por trava (acontece uma vez por processo).
    """
    with _TRAVA:
        original = inspect.getmodule

        def getmodule_seguro(objeto=None, _filename=None):
            modulo = original(objeto, _filename)
            if modulo is None:
                return sys.modules.get(__name__) or types.ModuleType(__name__)
            return modulo

        inspect.getmodule = getmodule_seguro
        try:
            return components.declare_component(nome, path=str(diretorio))
        finally:
            inspect.getmodule = original


class ComponenteFormulário:
    """Implementa `FormularioUI` (ver servico.py) com o componente HTML/JS customizado."""
    TEMPLATE = "preenchimento.html.j2"


    def __init__(
        self,
        esquema: Esquema,
        renderizador: RenderizadorJinja,
        *,
        diretorio: Path = DIRETORIO_COMPONENTE,
        nome: str = "form_dinamico",
        chave: str = "form_matricula_completo",
    ) -> None:

        self._esquema = esquema
        self._renderizador = renderizador
        self._diretorio = diretorio
        self._chave = chave
        diretorio.mkdir(parents=True, exist_ok=True)

        self._publicar()
        self._componente = _declarar_componente(nome, diretorio)

    def _publicar(self) -> None:
        """Gera o index.html do formulário. É refeito a cada execução da página (só grava se mudou)
        para que valores padrão dinâmicos, como a data de hoje, não fiquem velhos."""
        html = self._renderizador.renderizar(
            template= self.TEMPLATE,

            contexto= {
                "esquema": self._esquema,
                "regras_js": self._esquema.regras_js,
                "styles": self._renderizador.ler_fonte("styles.css"),
                "scripts": self._renderizador.ler_fonte("scripts.js"),
            },
        )
        _gravar_se_mudou(self._diretorio / "index.html", html)

    def coletar(self, erros: Mapping[str, str] | None = None, envio: Any = None) -> dict[str, Any] | None:
        """Desenha o formulário e devolve os dados quando o usuário envia (ou None antes disso).

        `erros` (chave do campo -> mensagem) é destacado no formulário. `envio` identifica a submissão
        a que os erros se referem: o formulário só os reaplica quando esse identificador muda.
        """
        self._publicar()
        return self._componente(key=self._chave, default=None, erros=dict(erros or {}), envio=envio)
