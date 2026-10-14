import streamlit as st

from app.core.funcionalidades.matrícula.composicao import montar_aplicacao

st.set_page_config(page_title='Nova Matrícula', layout='wide')
st.title('Preenchimento da Ficha de Matrícula', text_alignment='center')

servico, formulario = montar_aplicacao()
dados = formulario.coletar()

if dados:
    resultado = servico.gerar(dados)

    if not resultado.valido:
        st.error('Corrija os erros abaixo:')
        for erro in resultado.erros:
            st.error(f'– {erro}')
    else:
        st.success('Ficha gerada com sucesso!')
        st.download_button(
            label="📥 Baixar Ficha (HTML)",
            data=resultado.html,
            file_name=servico.nome_arquivo(dados),
            mime="text/html",
        )
