#todo alocar este módulo de uma forma mais organizada
from os import PathLike
from pathlib import Path

import pandas as pd
from pandas import DataFrame


class RelatórioDeAusências:

    def __init__(
            self,
            path: PathLike,
            # data,
            # período: tuple
    ):

        _path: PathLike = Path(path, 'fonte', 'Compilado Faltas.xlsx')

        self._leitura = self._obter_df_faltas(_path)
        # self._data = data
        # self._período = período


    @property
    def dicionário(self) -> DataFrame:
        if self._leitura is None:
            ausentes = {'Matrícula': None, 'Estudante' : None}
            return DataFrame(ausentes)

        else:
            df = self._leitura.copy()
            df = df[['Estudante', 'Data Falta', 'Matrícula']]
            # df['Data Falta'] = df['Data Falta'].dt.strftime('%d/%m/%Y')
            df['Data canonica'] = df['Data Falta'].dt.strftime('%Y/%m/%d')
            #
            # df = df[df['Data Falta'] == self._data]
            # df = df[df['Data Falta'] in self._período        ]



            # ausentes = dict(zip(df['Matrícula'], df['Estudante']))

            return df



    @property
    def dataframe(self) -> DataFrame:
        if self._leitura is None:
            ausentes = DataFrame({'Matrícula' : None, 'Estudante' : None})
            return ausentes

        else:
            df = self._leitura.copy()
            df = df[['Estudante', 'Data Falta', 'Matrícula']]
            df['Data Falta'] = df['Data Falta'].dt.strftime('%d/%m/%Y')

            return df

    @staticmethod
    def _obter_df_faltas(path):
        # print(f'{path = }')
        try:
            df = pd.read_excel(path, sheet_name='Compilado_Faltas', dtype={'Matrícula' : str})
            return df
        except (FileNotFoundError, KeyError):
            return None

