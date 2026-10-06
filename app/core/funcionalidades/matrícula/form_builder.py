# from typing import Dict, Any
# import streamlit as st
#
# from estrutura_de_dados.estrutura import SeçãoFormulário, Campo
# from app.core.funcionalidades.matrícula.funções import input_mascarado
#
#
# class StreamLitFormRenderer:
#
#     @staticmethod
#     def renderizar_campo(container, campo: Campo) -> Any:
#         # Exibição condicional (ex: NEE)
#         if campo.depende_de:
#             chave_pai, valor_esperado = campo.depende_de
#             if st.session_state.get(chave_pai) != valor_esperado:
#                 return None
#
#         # Campos com mascara ou restrição em tempo real
#         if campo.tipo == 'text' and (
#             campo.tipo_dado in ['cpf', 'date', 'telefone']
#             or campo.apenas_letras
#             or campo.apenas_numeros
#         ):
#             with container:
#                 # O próprio componente já atualiza st.session_state[campo.chave] por causa do parâmetro key
#                 return input_mascarado(
#                     label=campo.rótulo,
#                     chave=campo.chave,
#                     tipo_dado=campo.tipo_dado,
#                     apenas_letras=campo.apenas_letras,
#                     apenas_numeros=campo.apenas_numeros,
#                     max_chars=campo.cumprimento_máximo or 50,
#                 )
#
#         # Campos padrão do Streamlit
#         kwargs_base = {"label": campo.rótulo, "key": campo.chave}
#
#         if campo.tipo == 'text':
#             return container.text_input(
#                 max_chars=campo.cumprimento_máximo, **kwargs_base
#             )
#
#         elif campo.tipo == 'select':
#             return container.selectbox(options=campo.opções, **kwargs_base)
#
#         elif campo.tipo == 'radio':
#             return container.radio(
#                 options=campo.opções, horizontal=True, **kwargs_base
#             )
#
#         elif campo.tipo == 'multiselect':
#             return container.multiselect(options=campo.opções, **kwargs_base)
#
#         return None
#
#     def renderizar_seção(self, seção: SeçãoFormulário) -> Dict[str, Any]:
#         st.subheader(seção.título)
#         respostas = {}
#
#         for linha in seção.linhas:
#             colunas = st.columns(linha.proporções)
#             for coluna, campo in zip(colunas, linha.campos):
#                 self.renderizar_campo(coluna, campo)
#                 # Resgata o valor diretamente do session_state
#                 respostas[campo.chave] = st.session_state.get(campo.chave)
#
#         return respostas
#
#