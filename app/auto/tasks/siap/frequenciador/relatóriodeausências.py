#todo alocar este módulo de uma forma mais organizada
from os import PathLike
from pathlib import Path

import pandas as pd
from pandas import DataFrame


class RelatórioDeAusências:

    def __init__(
            self,
            path: PathLike,
    ):

        _path: PathLike = Path(path, 'fonte', 'Controle de Frequência', 'Compilado de Faltas.csv')
        self._leitura = self._obter_df_faltas(_path)

    @property
    def dicionário(self) -> DataFrame:
        if self._leitura is None:
            ausentes = {'Matrícula': None, 'Estudante' : None}
            return DataFrame(ausentes)

        else:
            df = self._leitura.copy()
            df = df[['Estudante', 'Data', 'Matrícula']]
            df['Data canonica'] = df['Data'].dt.strftime('%Y/%m/%d')
            return df

    @property
    def dataframe(self) -> DataFrame:
        if self._leitura is None:
            ausentes = DataFrame({'Matrícula' : None, 'Estudante' : None})
            return ausentes

        else:
            df = self._leitura.copy()
            df = df[['Estudante', 'Data', 'Matrícula']]
            # df['Data'] = df['Data'].dt.strftime('%d/%m/%Y')

            return df

    @staticmethod
    def _obter_df_faltas(path):
        try:
            df = pd.read_csv(
                path,
                dtype={'Matrícula' : str}
            )
            return df

        except (FileNotFoundError, KeyError):
            return None

