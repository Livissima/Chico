import streamlit as st

from app.core.funcionalidades.matrícula.esqueleto import TODAS_AS_SECOES
from app.core.funcionalidades.matrícula.funções import renderizar_formulario_completo, render_html_template
from app.core.funcionalidades.matrícula.validator import FormValidator
from app.core.funcionalidades.matrícula.context_adapter import ContextAdapter

st.set_page_config(page_title='Nova Matrícula', layout='wide')
st.title('Preenchimento da Ficha de Matrícula', text_alignment='center')

# Renderiza todas as seções do formulário
dados_coletados = renderizar_formulario_completo(TODAS_AS_SECOES)

if dados_coletados:
    # Agora dados_coletados é um dicionário Python legítimo
    válido, erros = FormValidator.validar(TODAS_AS_SECOES, dados_coletados)

    if not válido:
        st.error('Corrija os erros abaixo:')
        for erro in erros:
            st.error(f'– {erro}')
    else:
        contexto = ContextAdapter.conextualizar_jinja(dados_coletados)
        html_gerado = render_html_template(contexto)

        st.success('Ficha gerada com sucesso!')
        st.download_button(
            label="📥 Baixar Ficha (HTML)",
            data=html_gerado,
            file_name=f"Ficha_{dados_coletados.get('nome_estudante', 'Estudante')}.html",
            mime="text/html"
        )
