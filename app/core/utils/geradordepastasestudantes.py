import os
from pathlib import Path

import pandas as pd
from pandas import DataFrame

from app.config.settings.functions import normalizar_diacrítica


class GeradorDePastasEstudantes:
    def __init__(self, diretório_base: Path, diretório_secretaria: Path):
        self._path_df = Path(diretório_base, 'Database.xlsx')
        self._path_pasta_estudantes = Path(diretório_secretaria, 'Estudantes')
        self._dataframe = pd.read_excel(self._path_df, sheet_name='Base Ativa')

    def criar_pastas(self) :
        df = self._dataframe

        for índice, linha in df.iterrows() :
            matrícula = str(linha['Matrícula']).strip()
            estudante = linha['Estudante']

            nome_pasta_estudante = f'{estudante}   ~   {matrícula}'

            inicial = normalizar_diacrítica(nome_pasta_estudante).strip()[0].upper()
            if not inicial :
                continue

            path_pasta_inicial = self._path_pasta_estudantes / inicial

            path_pasta_inicial.mkdir(parents=True, exist_ok=True)

            pastas_de_estudantes = os.listdir(path_pasta_inicial)
            matrículas = [pasta[-11:] for pasta in pastas_de_estudantes]
            pastas_repetidas = [pasta for pasta in pastas_de_estudantes if matrícula in matrículas]

            if pastas_repetidas :
                plural = ('m', 's') if len(pastas_repetidas) > 1 else ('', '')
                print(
                    f'Já existe{plural[0]} pasta{plural[1]} para a seguinte matrícula: `{matrícula}`\n→ {pastas_repetidas}')

            path_final = path_pasta_inicial / nome_pasta_estudante

            try :
                path_final.mkdir(exist_ok=True)
                print(f'\nCriada nova pasta: {path_final}')
            except Exception as e :
                print(f"Erro ao criar a pasta {path_final}: {e}")


