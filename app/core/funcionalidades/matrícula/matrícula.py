import streamlit as st
import streamlit.components.v1 as components

from estrutura_dados import TODAS_AS_SECOES
from form_builder import StreamLitFormRenderer
from validator import FormValidator
from context_adapter import ContextAdapter
from funções import render_html_template

st.set_page_config(page_title='Nova matrícula', page_icon='🟢', layout='wide')
st.title('Preenchimento da Ficha de Matrícula')

renderer = StreamLitFormRenderer()
dados_coletados = {}

with st.form(key='form_matrícula'):
    for seção in TODAS_AS_SECOES:
        respostas_seção = renderer.renderizar_seção(seção)
        dados_coletados.update(respostas_seção)

    btn_submit = st.form_submit_button(label='Gerar ficha de matrícula')


if btn_submit:
    válido, erros = FormValidator.validar(TODAS_AS_SECOES, dados_coletados)

    if not válido:
        st.error('Por favor, corrija os erros abaixo antes de gerar a ficha')
        for erro in erros:
            st.error(f'– {erro}')

    else:
        contexto = ContextAdapter.para_jinja_contexto(dados_coletados)
        html_gerado = render_html_template(contexto)

        st.success(f'Ficha gerada com sucesso')

        st.download_button(
            label="📥 Baixar Ficha Preenchida (HTML)",
            data=html_gerado,
            file_name=f"Ficha_Matricula_{dados_coletados.get('nome_estudante', 'Estudante')}.html",
            mime="text/html"
        )

        st.subheader('Pré-visualização da Ficha Renderizada')

        components.html(html_gerado, height=1200, scrolling=True)