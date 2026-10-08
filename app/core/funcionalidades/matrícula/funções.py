import inspect
import os
import sys
import types
from typing import List, Dict, Any, Tuple

import streamlit.components.v1 as components


# ---------------------------------------------------------
# 1. GERADOR DO DOCUMENTO FINAL (Jinja2)
# ---------------------------------------------------------
from pathlib import Path
import streamlit as st
from jinja2 import Environment, FileSystemLoader

from app.core.funcionalidades.matrícula.elements.templates import SeçãoFormulário
from app.core.funcionalidades.matrícula.gerar_html_form import gerar_html_formulário
from app.functions.geral import encontrar_raiz_projeto


@st.cache_resource
def obter_ambiente_jinja():
    """Essa aqui é usada para obter o template HTML que receberá os dados preenchidos"""
    raiz = encontrar_raiz_projeto()

    locais_busca = [
        raiz / 'app' / 'core' / 'funcionalidades' / 'matrícula' / 'templates',
        Path(__file__).resolve().parent / "templates",
        ]

    # Filtra apenas os caminhos que realmente existem no disco
    diretorios_validos = [str(p) for p in locais_busca if p.is_dir()]

    if not diretorios_validos:
        raise FileNotFoundError(
            f"Nenhum diretório de assets foi localizado a partir de: {raiz}"
        )

    return Environment(loader=FileSystemLoader(diretorios_validos))


def renderizar_template_html(dados, nome_template: str):
    env = obter_ambiente_jinja()
    template = env.get_template(nome_template)
    return template.render(**dados)


# ---------------------------------------------------------
# 2. CONSTRUTOR PYTHON DO FORMULÁRIO HTML
# ---------------------------------------------------------
COMPONENT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "component_form_dinamico")
os.makedirs(COMPONENT_DIR, exist_ok=True)
INDEX_HTML_PATH = os.path.join(COMPONENT_DIR, "index.html")


# Localiza o diretório /templates relativo a este arquivo


def ler_arquivo_template(nome_arquivo: str) -> str:
    DIRETORIO_TEMPLATES = Path(__file__).parent / "templates"
    """Função auxiliar para ler o conteúdo de um arquivo de template."""
    caminho = DIRETORIO_TEMPLATES / nome_arquivo
    return caminho.read_text(encoding="utf-8")


def montar_html_completo(corpo_html: str) -> str:
    html_base = ler_arquivo_template("preenchimento.html")
    styles = ler_arquivo_template("styles.css")
    scripts = ler_arquivo_template("scripts.js")

    return html_base.format(
        styles=styles,
        corpo_html=corpo_html,
        scripts=scripts
    )


def _declarar_componente_seguro() :
    orig_getmodule = inspect.getmodule

    def safe_getmodule(object=None, _filename=None) :
        mod = orig_getmodule(object, _filename)
        if mod is None :
            return sys.modules.get(__name__) or types.ModuleType(__name__)
        return mod

    inspect.getmodule = safe_getmodule
    try :
        return components.declare_component("form_dinamico", path=COMPONENT_DIR)
    finally :
        inspect.getmodule = orig_getmodule


def renderizar_formulario_completo(secoes) :
    """Gera o HTML estático no servidor Python e renderiza o componente."""
    corpo_html = gerar_html_formulário(secoes)
    html_final = montar_html_completo(corpo_html)

    with open(INDEX_HTML_PATH, "w", encoding="utf-8") as f :
        f.write(html_final)

    componente = _declarar_componente_seguro()
    return componente(key="form_matricula_completo", default=None)


def conextualizar_jinja(dados: dict) -> dict:
    contexto = dados.copy()

    gênero = dados.get('gênero', '')
    contexto['gênero_m'] = 'X' if gênero == 'Masculino' else ''
    contexto['gênero_f'] = 'X' if gênero == 'Feminino' else ''

    cor_etnia = dados.get('cor_etnia', '')
    for opção in ['Branca', 'Preta', 'Parda', 'Indígena', 'Amarela', 'Não declarado']:
        chave_cor = f'cor_{opção.lower().replace(' ', '_').replace('í', 'i')}'
        contexto[chave_cor] = 'X' if cor_etnia == opção else ''

    return contexto


def validar(seções: List[SeçãoFormulário], dados: Dict[str, Any]) -> Tuple[bool, List[str]]:
    erros = []
    for seção in seções:
        for linha in seção.linhas:
            for campo in linha.campos:
                valor = dados.get(campo.chave)
                erro = campo.validar(valor)

                if erro: erros.append(erro)

    é_valido = len(erros) == 0
    return é_valido, erros
