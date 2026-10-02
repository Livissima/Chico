from pathlib import Path

import streamlit as st
from jinja2 import Environment, FileSystemLoader



# ---------------------------------------------------------
# RENDERIZADOR JINJA2,
# ---------------------------------------------------------
@st.cache_resource
def get_jinja_env() :
    # Encontra a pasta onde este arquivo .py está localizado
    diretorio_atual = Path(__file__).resolve().parent

    # Aponta para a pasta 'app/ui/assets'
    pasta_assets = diretorio_atual.parent / "assets"

    return Environment(loader=FileSystemLoader(pasta_assets))


def render_html_template(dados) :
    env = get_jinja_env()
    # Chama apenas o nome do arquivo, pois o FileSystemLoader já aponta para a pasta assets
    template = env.get_template('ficha_matricula.html')
    return template.render(**dados)
