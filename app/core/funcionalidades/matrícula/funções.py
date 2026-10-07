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
        Path(__file__).resolve().parent / "assets",
    ]

    # Filtra apenas os caminhos que realmente existem no disco
    diretorios_validos = [str(p) for p in locais_busca if p.is_dir()]

    if not diretorios_validos:
        raise FileNotFoundError(
            f"Nenhum diretório de assets foi localizado a partir de: {raiz}"
        )

    return Environment(loader=FileSystemLoader(diretorios_validos))


def render_html_template(dados, nome_template="ficha_matricula.html"):
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


def montar_html_completo(corpo_html) :
    """Gera o HTML com validação de dados em tempo real e bloqueio de envio."""
    return f"""<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <style>
    body {{
      font-family: system-ui, -apple-system, sans-serif;
      color: #FAFAFA;
      padding: 10px;
      margin: 0;
      background: transparent;
    }}
    .grid {{
      display: flex;
      flex-wrap: wrap;
      gap: 12px;
      margin-bottom: 12px;
      width: 100%;
      box-sizing: border-box;
    }}
    .campo-box {{
      display: flex;
      flex-direction: column;
      box-sizing: border-box;
      min-width: 0;
      position: relative;
    }}
    label {{
      font-size: 14px;
      font-weight: 500;
      margin-bottom: 4px;
      color: #E0E0E0;
    }}
    input, select {{
      padding: 8px 10px;
      border: 1px solid #464853;
      border-radius: 6px;
      font-size: 14px;
      outline: none;
      box-sizing: border-box;
      width: 100%;
      background: #262730;
      color: #FFFFFF;
      transition: border-color 0.2s;
    }}
    input:focus, select:focus {{
      border-color: #FF4B4B;
      box-shadow: 0 0 0 1px #FF4B4B;
    }}
    /* Estilos de Validação */
    input.invalido, select.invalido {{
      border-color: #FF2B2B !important;
      background-color: #331A1A;
    }}
    .erro-mensagem {{
      color: #FF6B6B;
      font-size: 11px;
      margin-top: 3px;
      display: none;
    }}
    .campo-box.com-erro .erro-mensagem {{
      display: block;
    }}
    .secao-titulo {{
      font-size: 18px;
      font-weight: 600;
      margin: 20px 0 12px 0;
      border-bottom: 2px solid #31333F;
      padding-bottom: 6px;
      color: #FAFAFA;
    }}
    .oculto {{ display: none !important; }}

    button {{
      background-color: #FF4B4B;
      color: white;
      border: none;
      padding: 12px 24px;
      font-size: 16px;
      font-weight: 600;
      border-radius: 6px;
      cursor: pointer;
      margin-top: 20px;
      width: 100%;
    }}
    button:hover {{ background-color: #E03E3E; }}
  </style>
</head>
<body>

  <form id="formMatricula" novalidate>
    {corpo_html}
    <button type="submit">Gerar Ficha de Matrícula</button>
  </form>

  <script>
    function sendToStreamlit(type, data) {{
      window.parent.postMessage(Object.assign({{
        isStreamlitMessage: true,
        type: type
      }}, data), "*");
    }}

    function setFrameHeight() {{
      sendToStreamlit("streamlit:setFrameHeight", {{
        height: document.body.scrollHeight + 30
      }});
    }}

    function setComponentValue(val) {{
      sendToStreamlit("streamlit:setComponentValue", {{ value: val }});
    }}

    // --- REGRAS DE VALIDAÇÃO LOGICA ---

    function validarDataValida(strData, minAno = 1900, maxAno = new Date().getFullYear()) {{
      if (!strData || strData.length < 10) return false;
      const partes = strData.split('/');
      if (partes.length !== 3) return false;

      const dia = parseInt(partes[0], 10);
      const mes = parseInt(partes[1], 10);
      const ano = parseInt(partes[2], 10);

      if (isNaN(dia) || isNaN(mes) || isNaN(ano)) return false;
      if (ano < minAno || ano > maxAno) return false;
      if (mes < 1 || mes > 12) return false;

      // Validação real considerando dias do mês e ano bissexto
      const dataObj = new Date(ano, mes - 1, dia);
      return (
        dataObj.getFullYear() === ano &&
        dataObj.getMonth() === (mes - 1) &&
        dataObj.getDate() === dia
      );
    }}

    function validarCPFValido(cpf) {{
      cpf = cpf.replace(/\\D/g, '');
      if (cpf.length !== 11 || /^(\\d)\\1{{10}}$/.test(cpf)) return false;

      let soma = 0, resto;
      for (let i = 1; i <= 9; i++) soma += parseInt(cpf.substring(i-1, i)) * (11 - i);
      resto = (soma * 10) % 11;
      if (resto === 10 || resto === 11) resto = 0;
      if (resto !== parseInt(cpf.substring(9, 10))) return false;

      soma = 0;
      for (let i = 1; i <= 10; i++) soma += parseInt(cpf.substring(i-1, i)) * (12 - i);
      resto = (soma * 10) % 11;
      if (resto === 10 || resto === 11) resto = 0;
      if (resto !== parseInt(cpf.substring(10, 11))) return false;

      return true;
    }}

    function aplicarErro(el, mensagem) {{
      const box = el.closest('.campo-box');
      el.classList.add('invalido');
      if (box) {{
        box.classList.add('com-erro');
        let msgSpan = box.querySelector('.erro-mensagem');
        if (!msgSpan) {{
          msgSpan = document.createElement('span');
          msgSpan.className = 'erro-mensagem';
          box.appendChild(msgSpan);
        }}
        msgSpan.innerText = mensagem;
      }}
    }}

    function limparErro(el) {{
      const box = el.closest('.campo-box');
      el.classList.remove('invalido');
      if (box) {{
        box.classList.remove('com-erro');
      }}
    }}

    function validarCampo(el) {{
      const tipo = el.getAttribute('data-tipo');
      const valor = el.value.trim();

      // Ignora campos ocultos
      if (el.closest('.oculto')) {{
        limparErro(el);
        return true;
      }}

      if (!valor) {{
        limparErro(el);
        return true; // Deixa o 'required' para validações estritas de preenchimento
      }}

      if (tipo === 'date') {{
        if (!validarDataValida(valor)) {{
          aplicarErro(el, 'Data inválida ou fora do intervalo.');
          return false;
        }}
      }} else if (tipo === 'cpf') {{
        if (!validarCPFValido(valor)) {{
          aplicarErro(el, 'CPF inválido.');
          return false;
        }}
      }} else if (tipo === 'telefone') {{
        const num = valor.replace(/\\D/g, '');
        if (num.length < 10 || num.length > 11) {{
          aplicarErro(el, 'Telefone incompleto.');
          return false;
        }}
      }}

      limparErro(el);
      return true;
    }}

    // --- MÁSCARAS E MUDANÇAS EM TEMPO REAL ---

    document.getElementById('formMatricula').addEventListener('input', (e) => {{
      const el = e.target;
      const tipo = el.getAttribute('data-tipo');
      const soLetras = el.getAttribute('data-letras');
      const soNumeros = el.getAttribute('data-numeros');
      let v = el.value;

      if (soNumeros === 'true') {{
        v = v.replace(/[^0-9]/g, '');
      }} else if (soLetras === 'true') {{
        v = v.replace(/[^a-zA-ZáàâãéèêíïóôõöúçñÁÀÂÃÉÈÊÍÏÓÔÕÖÚÇÑ\\s]/g, '');
      }}

      if (tipo === 'cpf') {{
        v = v.replace(/\\D/g, '').replace(/(\\d{{3}})(\\d)/, '$1.$2').replace(/(\\d{{3}})(\\d)/, '$1.$2').replace(/(\\d{{3}})(\\d{{1,2}})$/, '$1-$2');
      }} else if (tipo === 'date') {{
        v = v.replace(/\\D/g, '').replace(/(\\d{{2}})(\\d)/, '$1/$2').replace(/(\\d{{2}})(\\d)/, '$1/$2').replace(/(\\d{{4}})\\d+?$/, '$1');
      }} else if (tipo === 'telefone') {{
        v = v.replace(/\\D/g, '');
        if (v.length > 10) v = v.replace(/^(\\d{{2}})(\\d{{5}})(\\d{{4}}).*/, '($1) $2-$3');
        else if (v.length > 6) v = v.replace(/^(\\d{{2}})(\\d{{4}})(\\d{{0,4}}).*/, '($1) $2-$3');
        else if (v.length > 2) v = v.replace(/^(\\d{{2}})(\\d{{0,5}})/, '($1) $2');
      }}

      el.value = v;
    }});

    // Valida o campo quando o usuário clica fora dele (blur)
    document.getElementById('formMatricula').addEventListener('focusout', (e) => {{
      if (e.target.tagName === 'INPUT' || e.target.tagName === 'SELECT') {{
        validarCampo(e.target);
      }}
    }});

    // Lógica de dependências condicionais
    function checarDependencias() {{
      const camposCondicionais = document.querySelectorAll('[data-depende-de]');
      camposCondicionais.forEach(box => {{
        const paiId = box.getAttribute('data-depende-de');
        const valorEsperado = box.getAttribute('data-valor-esperado');
        const elPai = document.getElementById(paiId);
        if (elPai) {{
          if (elPai.value === valorEsperado) {{
            box.classList.remove('oculto');
          }} else {{
            box.classList.add('oculto');
            const input = box.querySelector('input, select, textarea');
            if (input) {{
              input.value = '';
              limparErro(input);
            }}
          }}
        }}
      }});
      setFrameHeight();
    }}

    document.getElementById('formMatricula').addEventListener('change', checarDependencias);
    checarDependencias();

    // Envio com validação completa de todos os campos
    document.getElementById('formMatricula').addEventListener('submit', (e) => {{
      e.preventDefault();

      const elementos = e.target.querySelectorAll('input, select, textarea');
      let formularioValido = true;

      elementos.forEach(el => {{
        if (!validarCampo(el)) {{
          formularioValido = false;
        }}
      }});

      if (!formularioValido) {{
        setFrameHeight();
        return;
      }}

      const dados = {{}};
      elementos.forEach(el => {{
        if (el.id && !el.closest('.oculto')) dados[el.id] = el.value;
      }});

      setComponentValue(dados);
    }});

    window.addEventListener("message", (e) => {{
      if (e.data && e.data.type === "streamlit:render") {{
        setFrameHeight();
      }}
    }});

    sendToStreamlit("streamlit:componentReady", {{ apiVersion: 1 }});
    setTimeout(setFrameHeight, 100);
  </script>
</body>
</html>
"""


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
