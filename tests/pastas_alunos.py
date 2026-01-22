#TODO: Realocar este módulo para um pacote apropriado.
import os
from pathlib import Path

import pandas as pd
from pandas import DataFrame

from app.config.app_config import DIRETÓRIO_BASE_PADRÃO, DIRETÓRIO_SECRETARIA

path_pasta_estudantes = Path(DIRETÓRIO_SECRETARIA, 'Estudantes')
path_database = Path(DIRETÓRIO_BASE_PADRÃO, 'Database.xlsx')
path_cancelados = Path(DIRETÓRIO_SECRETARIA, 'Matrículas canceladas 2026.xlsx')

df_cancelados = pd.read_excel(path_cancelados)
df_cancelados['Matrícula'] = df_cancelados['Matrícula'].replace(['\xa0', '-'], ['', ''], regex=True)

df_database = pd.read_excel(path_database, sheet_name='Base Ativa')


def criar_pastas(df: DataFrame):

    for índice, linha in df.iterrows():
        matrícula = linha['Matrícula']
        estudante = linha['Estudante']
        série = linha['Série']

        nome_pasta = f'{estudante}   ~   {matrícula}'
        pasta = Path(path_pasta_estudantes, nome_pasta)

        #NÃO MEXA NESSA LÓGICA
        if not pasta.exists():
            print(pasta)
            pasta.mkdir(parents=True, exist_ok=True)


criar_pastas(df_database)
