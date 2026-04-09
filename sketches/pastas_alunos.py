#TODO: Realocar este módulo para um pacote apropriado.
from pathlib import Path

import pandas as pd
from pandas import DataFrame

from app.config.settings.app_config import DIRETÓRIO_BASE_PADRÃO, DIRETÓRIO_SECRETARIA
from app.config.settings.functions import normalizar_diacrítica

path_pasta_estudantes = Path(DIRETÓRIO_SECRETARIA, 'Estudantes')
path_database = Path(DIRETÓRIO_BASE_PADRÃO, 'Database.xlsx')
df_database = pd.read_excel(path_database, sheet_name='Base Ativa')

def inicial_da_pasta(nome_pasta: str) -> str:
    return normalizar_diacrítica(nome_pasta).strip()[0].upper()

def criar_pastas(df: DataFrame):
    for índice, linha in df.iterrows():
        matrícula = linha['Matrícula']
        estudante = linha['Estudante']

        # NÃO MEXA NESSA LÓGICA
        nome_pasta_estudante = f'{estudante}   ~   {matrícula}'

        inicial = inicial_da_pasta(nome_pasta_estudante)
        if not inicial:
            continue

        path_pasta_inicial = path_pasta_estudantes / inicial
        if not path_pasta_inicial.exists():
            print(f'Pasta de inicial inexistente: {inicial}')
            continue

        path_final = path_pasta_inicial / nome_pasta_estudante

        try:
            path_final.mkdir()
            print(f'Criada: {path_final}')
        except FileExistsError:
            pass


criar_pastas(df_database)
