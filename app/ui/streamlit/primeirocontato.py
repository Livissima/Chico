from datetime import timedelta
from pathlib import Path

import pandas as pd
import streamlit as st
import yfinance

path = Path(r'C:\Users\meren\OneDrive - Secretaria de Estado da Educação\SIGE\Database.xlsx')


@st.cache_data
def carregar_dados(empresas):
    texto_tickers = ' '.join(empresas)
    dados_ação = yfinance.Tickers(texto_tickers)
    cotação = dados_ação.history(start='2010-01-01', end='2024-07-01')
    cotação = cotação['Close']
    return cotação

@st.cache_data
def carregar_tickers_ações():
    base_tickers = pd.read_csv('IBOV.csv', sep=';')
    tickers = list(base_tickers['Código'])
    tickers = [item + '.SA' for item in tickers]
    return tickers

ações = carregar_tickers_ações()
dados = carregar_dados(ações)

st.write(
    """
    # Database:
    Base ativa
    """
)

st.sidebar.header('Filtros')


lista_ações_selecionadas = st.sidebar.multiselect('Selecione', dados.columns)
if lista_ações_selecionadas:
    dados = dados[lista_ações_selecionadas]
    if len(lista_ações_selecionadas) == 1:
        ação_única = lista_ações_selecionadas[0]
        dados = dados.rename(columns={ação_única : 'close'})


data_inicial = dados.index.min().to_pydatetime()
data_final = dados.index.max().to_pydatetime()
slider_intervalo_datas = st.sidebar.slider(
    'Selecione o período',
    min_value=data_inicial,
    max_value=data_final,
    value=(data_inicial, data_final),
    step=timedelta(days=365)
)

print(f'{slider_intervalo_datas = }')

dados = dados.loc[slider_intervalo_datas[0]:slider_intervalo_datas[1]]

st.line_chart(dados)

