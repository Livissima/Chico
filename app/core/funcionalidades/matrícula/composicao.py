"""Raiz de composição: o único lugar que escolhe e liga as implementações concretas."""
from __future__ import annotations

import streamlit as st

from app.core.funcionalidades.matrícula.infra.renderizador import RenderizadorJinja
from .dominio.contexto import ConstrutorDeContexto
from app.core.funcionalidades.matrícula.dominio.elementos.esquema import ESQUEMA, VARIAVEIS_SEM_CAMPO
from .infra.componente_streamlit import ComponenteFormulário
from .infra.gerador_pdf import GeradorPdfNavegador, GeradorPdfPlaywright
from .servico import FormularioUI, ServicoFicha


@st.cache_resource
def montar_aplicacao() -> tuple[ServicoFicha, FormularioUI]:
    """Criado uma vez por processo. Se mudar os módulos de elementos ou os templates com o app aberto,
    limpe o cache (tecla C no app) para recarregar."""
    renderizador = RenderizadorJinja()

    # Motor de PDF: escolha UM.
    gerador_pdf = GeradorPdfNavegador()  # Edge/Chrome já instalado no Windows: não precisa instalar nada
    # gerador_pdf = GeradorPdfPlaywright()  # Chromium do Playwright: pip install playwright && playwright install chromium

    servico = ServicoFicha(
        ESQUEMA,
        ConstrutorDeContexto(valores_fixos=VARIAVEIS_SEM_CAMPO),
        renderizador,
        gerador_pdf,
    )
    formulario = ComponenteFormulário(ESQUEMA, renderizador)
    return servico, formulario
