from pathlib import Path
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
from app.functions.genéricas import encontrar_raiz_projeto


@st.cache_resource
def get_jinja_env():
    raiz = encontrar_raiz_projeto()

    # Mapeia possíveis locais de assets no projeto
    locais_busca = [
        raiz / "app" / "ui" / "assets",
        raiz / "app" / "assets",
        raiz / "assets",
        raiz / 'app' / 'core' / 'funcionalidades' / 'matrícula' / 'templates',
        Path(__file__).resolve().parent / "assets",
        ]

    # Filtra apenas os caminhos que realmente existem no disco
    diretorios_validos = [str(p) for p in locais_busca if p.is_dir()]

    if not diretorios_validos:
        raise FileNotFoundError(
            f"Nenhum diretório de assets foi localizado a partir de: {raiz}"
        )

    return Environment(loader=FileSystemLoader(diretorios_validos))


def render_html_template(dados, nome_template="pagina_print.html"):
    env = get_jinja_env()
    template = env.get_template(nome_template)
    return template.render(**dados)


# ---------------------------------------------------------
# 2. CONSTRUTOR PYTHON DO FORMULÁRIO HTML
# ---------------------------------------------------------
COMPONENT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "component_form_dinamico")
os.makedirs(COMPONENT_DIR, exist_ok=True)
INDEX_HTML_PATH = os.path.join(COMPONENT_DIR, "index.html")


def gerar_html_corpo_formulario(secoes) :
    """Converte o objeto TODAS_AS_SECOES em HTML calculando a proporção exata de cada coluna."""
    html_buffer = []

    for sec in secoes :
        titulo = getattr(sec, "título", getattr(sec, "titulo", ""))
        html_buffer.append(f'<div class="secao-titulo">{titulo}</div>')

        for linha in sec.linhas :
            props = getattr(linha, "proporções", getattr(linha, "proporcoes", []))
            qtd_campos = len(linha.campos)

            # Caso não haja proporções definidas, distribui uniformemente
            if not props or len(props) != qtd_campos :
                props = [1] * qtd_campos

            soma_props = sum(props) if sum(props) > 0 else 1
            html_buffer.append('<div class="grid">')

            for idx, c in enumerate(linha.campos) :
                p = props[idx]
                # Normaliza a proporção em percentagem real do container
                flex_pct = round((p / soma_props) * 100, 4)

                chave = getattr(c, "chave", "")
                rotulo = getattr(c, "rótulo", getattr(c, "rotulo", ""))
                tipo = getattr(c, "tipo", "text")
                tipo_dado = getattr(c, "tipo_dado", "str")
                letras = getattr(c, "apenas_letras", False)
                numeros = getattr(c, "apenas_numeros", False)
                c_max = getattr(c, "cumprimento_máximo", getattr(c, "cumprimento_maximo", None))
                opcoes = getattr(c, "opções", getattr(c, "opcoes", []))
                depende = getattr(c, "depende_de", None)

                style = f"flex: 0 0 calc({flex_pct}% - 12px); max-width: calc({flex_pct}% - 12px);"
                classes = ["campo-box"]
                data_attrs = []

                if depende :
                    classes.append("oculto")
                    pai_id, val_esp = depende
                    data_attrs.append(f'data-depende-de="{pai_id}"')
                    data_attrs.append(f'data-valor-esperado="{val_esp}"')

                class_str = " ".join(classes)
                data_str = " ".join(data_attrs)

                html_buffer.append(f'<div class="{class_str}" id="box_{chave}" style="{style}"'
                                   f" {data_str}>")
                html_buffer.append(f"<label>{rotulo}</label>")

                if tipo in ["select", "radio"] :
                    html_buffer.append(f'<select id="{chave}">')
                    for opt in opcoes :
                        html_buffer.append(f'<option value="{opt}">{opt}</option>')
                    html_buffer.append("</select>")
                else :
                    attrs = [f'id="{chave}"', 'type="text"']
                    if tipo_dado :
                        attrs.append(f'data-tipo="{tipo_dado}"')
                    if letras :
                        attrs.append('data-letras="true"')
                    if numeros :
                        attrs.append('data-numeros="true"')
                    if c_max :
                        attrs.append(f'maxlength="{c_max}"')

                    if tipo_dado == "cpf" :
                        attrs.append('placeholder="000.000.000-00"')
                    elif tipo_dado == "date" :
                        attrs.append('placeholder="DD/MM/AAAA"')
                    elif tipo_dado == "telefone" :
                        attrs.append('placeholder="(00) 00000-0000"')

                    html_buffer.append(f'<input {" ".join(attrs)} />')

                html_buffer.append("</div>")
            html_buffer.append("</div>")

    return "\n".join(html_buffer)



# Localiza o diretório /templates relativo a este ficheiro


def _ler_ficheiro_template(nome_ficheiro: str) -> str:
    DIRETORIO_TEMPLATES = Path(__file__).parent / "templates"
    """Função auxiliar para ler o conteúdo de um ficheiro de template."""
    caminho = DIRETORIO_TEMPLATES / nome_ficheiro
    return caminho.read_text(encoding="utf-8")


def montar_html_completo(corpo_html: str) -> str:
    """
    Carrega os ficheiros HTML, CSS e JS separados e compõe a string
    HTML final para renderização no Streamlit.
    """
    html_base = _ler_ficheiro_template("preenchimento.html")
    styles = _ler_ficheiro_template("styles.css")
    scripts = _ler_ficheiro_template("scripts.js")

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
    corpo_html = gerar_html_corpo_formulario(secoes)
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
