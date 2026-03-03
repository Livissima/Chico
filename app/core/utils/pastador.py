from pathlib import Path

import pandas as pd
from pandas import DataFrame

from app.config.settings.app_config import DIRETÓRIO_SECRETARIA
from app.config.settings.functions import normalizar_diacrítica


class Pastador:
    def __init__(self, diretório_base: str | Path):
        self._path_df = Path(diretório_base, 'Database.xlsx')
        self._path_pasta_estudantes = Path(DIRETÓRIO_SECRETARIA, 'Estudantes')


        self._criar_pastas()



    def _criar_pastas(self):
        for índice, linha in self._dataframe.iterrows() :
            matrícula = linha['Matrícula']
            estudante = linha['Estudante']

            # NÃO MEXA NESSA LÓGICA
            nome_pasta_estudante = f'{estudante}   ~   {matrícula}'

            inicial = self._inicial_da_pasta(nome_pasta_estudante)
            if not inicial :
                continue

            path_pasta_inicial = self._path_pasta_estudantes / inicial
            if not path_pasta_inicial.exists() :
                print(f'Pasta de inicial inexistente: {inicial}')
                continue

            path_final = path_pasta_inicial / nome_pasta_estudante

            try :
                path_final.mkdir()
                print(f'Criada: {path_final}')
            except FileExistsError :
                pass

    @staticmethod
    def _inicial_da_pasta(nome_pasta: str) -> str :
        return normalizar_diacrítica(nome_pasta).strip()[0].upper()

    @property
    def _dataframe(self) -> DataFrame:
        return pd.read_excel(self._path_df, sheet_name='Base Ativa')
