#TODO: Realocar este módulo para um pacote apropriado.
import os
from pathlib import Path

import pandas as pd

from app.config.app_config import DIRETÓRIO_BASE_PADRÃO, DIRETÓRIO_SECRETARIA

user = 'livia'
path_pasta_estudantes = Path(DIRETÓRIO_SECRETARIA, 'Estudantes')
path_database = Path(DIRETÓRIO_BASE_PADRÃO, 'Database.xksx')
path_cancelados = Path(DIRETÓRIO_SECRETARIA, 'Matrículas canceladas 2026.xlsx')

df_cancelados = pd.read_excel(path_cancelados)
df_cancelados['Matrícula'] = df_cancelados['Matrícula'].replace(['\xa0', '-'], ['', ''], regex=True)

for índice, linha in df_cancelados.iterrows():
    matrícula = linha['Matrícula']
    estudante = linha['Nome']
    série = linha['Série']

    # nome_pasta = f'{série}º ~ {estudante}  - {matrícula}'
    nome_pasta = f'{estudante}   ~   {matrícula}'
    pasta = Path(path_pasta_estudantes, nome_pasta)
    print(pasta)
    if not pasta.exists():
        pasta.mkdir(parents=True, exist_ok=True)
