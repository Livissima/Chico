import streamlit as st

from app.core.funcionalidades.matrícula.composicao import montar_aplicacao

st.set_page_config(page_title='Nova Matrícula', layout='wide')
st.title('Preenchimento da Ficha de Matrícula', text_alignment='center')

servico, formulario = montar_aplicacao()

# Última geração desta sessão: `envio` identifica a última submissão já processada,
# e `erros` (campo -> mensagem) é devolvido ao formulário para destacar os campos com problema.
estado = st.session_state.setdefault('estado_matricula', {'envio': None, 'erros': {}, 'resultado': None})

dados = formulario.coletar(erros=estado['erros'], envio=estado['envio'])

if dados and dados.get('_envio') != estado['envio']:
    with st.spinner('Gerando a ficha...'):
        resultado = servico.gerar(dados)
    estado.update(envio=dados.get('_envio'), erros=resultado.erros_por_campo, resultado=resultado)
    st.rerun()  # reexecuta para o formulário receber os erros (ou limpar os antigos)

resultado = estado['resultado']

if resultado is not None:
    if not resultado.valido:
        st.error('Corrija os erros abaixo:')
        for mensagem in resultado.mensagens:
            st.error(f'– {mensagem}')
    else:
        st.success('Ficha gerada com sucesso!')
        coluna_pdf, coluna_json = st.columns(2)
        coluna_pdf.download_button(
            label='📥 Baixar Ficha (PDF)',
            data=resultado.pdf,
            file_name=f'{resultado.nome_base}.pdf',
            mime='application/pdf',
            on_click='ignore',
        )
        coluna_json.download_button(
            label='📥 Baixar Dados (JSON)',
            data=resultado.json,
            file_name=f'{resultado.nome_base}.json',
            mime='application/json',
            on_click='ignore',
        )
