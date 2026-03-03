#TODO: Realocar este módulo para um pacote apropriado.
import os
from pathlib import Path

import pandas as pd

from app.config.settings.app_config import DIRETÓRIO_BASE_PADRÃO, DIRETÓRIO_SECRETARIA



def normalizar_diacrítica(texto):
    import unicodedata

    return ''.join(
        c for c in unicodedata.normalize('NFKD', texto)
        if not unicodedata.combining(c)
    )

path_pasta_estudantes = Path(DIRETÓRIO_SECRETARIA, 'Estudantes')
path_database = Path(DIRETÓRIO_BASE_PADRÃO, 'Database.xlsx')
path_cancelados = Path(DIRETÓRIO_SECRETARIA, 'Matrículas canceladas 2026.xlsx')

df_cancelados = pd.read_excel(path_cancelados)
df_cancelados['Matrícula'] = df_cancelados['Matrícula'].replace(['\xa0', '-'], ['', ''], regex=True)

df_database = pd.read_excel(path_database, sheet_name='Base Ativa')

pasta_de_pastas = os.listdir(path_pasta_estudantes)

alfabeto = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'X', 'W', 'Y', 'Z']

pastas_de_nomes = [pasta for pasta in pasta_de_pastas if len(pasta) > 1]
pastas_de_iniciais = [pasta for pasta in pasta_de_pastas if len(pasta) == 1]


import shutil


def obter_inicial(_nome_pasta: str) -> str | None:
    nome_normalizado = normalizar_diacrítica(_nome_pasta).strip()
    if not nome_normalizado:
        return None
    return nome_normalizado[0].upper()

for nome_pasta in pastas_de_nomes:
    path_origem = path_pasta_estudantes / nome_pasta

    if not path_origem.is_dir():
        continue

    inicial = obter_inicial(nome_pasta)

    if not inicial:
        continue

    path_destino_inicial = path_pasta_estudantes / inicial

    # Garante que a pasta de inicial existe
    if not path_destino_inicial.exists():
        print(f'⚠️ Pasta de inicial não existe: {inicial}')
        continue

    path_destino_final = path_destino_inicial / nome_pasta

    if path_destino_final.exists():
        print(f'⚠️ Já existe: {path_destino_final}')
        continue

    shutil.move(str(path_origem), str(path_destino_final))
