import streamlit as st
from typing import Dict, Any
from app.core.funcionalidades.matrícula.schemas import SeçãoFormulário, CampoSchema

class StreamLitFormRenderer:

    @staticmethod
    def renderizar_campo(container, campo: CampoSchema) -> Any:
        if campo.tipo == 'text':
            return container.text_input(
                label=campo.rótulo,
                value=campo.valor_padrão,
                max_chars=campo.cumprimento_máximo,
                key=campo.chave
            )

        elif campo.tipo == 'select':
            return container.selectbox(
                label=campo.rótulo,
                options=campo.opções,
                key=campo.chave
            )

        elif campo.tipo == 'radio':
            return container.multiselect(
                label=campo.rótulo,
                options=campo.opções,
                key=campo.chave
            )

        return None

    def renderizar_seção(self, seção: SeçãoFormulário) -> Dict[str, Any]:
        st.subheader(seção.título)
        respostas = {}

        for linha in seção.linhas:
            colunas = st.columns(linha.proporções)
            for coluna, campo in zip(colunas, linha.campos):
                respostas[campo.chave] = self.renderizar_campo(coluna, campo)

        return respostas