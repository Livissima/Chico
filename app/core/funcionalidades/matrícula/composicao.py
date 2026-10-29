"""Raiz de composição: o único lugar que escolhe e liga as implementações concretas."""
from __future__ import annotations

import streamlit as st

from .apresentacao.jinja import RenderizadorJinja
from .dominio.contexto import ConstrutorDeContexto
from .dominio.definicao import ESQUEMA
from .infra.componente_streamlit import ComponenteFormulário
from .servico import FormularioUI, ServicoFicha


@st.cache_resource
def montar_aplicacao() -> tuple[ServicoFicha, FormularioUI]:
    """Criado uma vez por processo. Se mudar definicao.py ou os templates com o app aberto,
    limpe o cache (tecla C no app) para recarregar."""
    renderizador = RenderizadorJinja()
    servico = ServicoFicha(ESQUEMA, ConstrutorDeContexto(), renderizador)
    formulario = ComponenteFormulário(ESQUEMA, renderizador)
    return servico, formulario
