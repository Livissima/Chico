"""Único ponto do projeto que conhece o Jinja2."""
from __future__ import annotations

from pathlib import Path
from typing import Any, Mapping

from jinja2 import Environment, FileSystemLoader, StrictUndefined, meta, select_autoescape

DIRETORIO_TEMPLATES = Path(__file__).resolve().parent.parent / "templates"


class RenderizadorJinja:
    """Renderiza templates da pasta `templates/`.

    - autoescape ligado para .html e .j2 (valores do usuário nunca viram HTML);
    - StrictUndefined: variável ausente no contexto levanta erro em vez de sair vazia.
    """

    def __init__(self, diretorio: Path = DIRETORIO_TEMPLATES) -> None:
        if not diretorio.is_dir():
            raise FileNotFoundError(f"Diretório de templates não encontrado: {diretorio}")
        self._env = Environment(
            loader=FileSystemLoader(str(diretorio)),
            autoescape=select_autoescape(enabled_extensions=("html", "j2"), default_for_string=True),
            undefined=StrictUndefined,
        )

    def renderizar(self, template: str, contexto: Mapping[str, Any]) -> str:
        return self._env.get_template(template).render(**contexto)

    def ler_fonte(self, arquivo: str) -> str:
        """Texto bruto de um arquivo (ex.: styles.css, scripts.js), sem interpretar Jinja."""
        return self._env.loader.get_source(self._env, arquivo)[0]

    def variaveis_do_template(self, template: str) -> set[str]:
        """Nomes que o template espera receber do contexto (útil em testes de contrato)."""
        fonte = self.ler_fonte(template)
        return meta.find_undeclared_variables(self._env.parse(fonte))
