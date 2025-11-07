#todo alocar este módulo de uma forma mais organizada
from os import PathLike
from pathlib import Path

import numpy as np
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
    def dataframe(self) -> DataFrame:
        if self._leitura is None:
            ausentes = DataFrame({'Estudante' : None, 'Data' : None, 'Matrícula' : None, 'Lançado': None})
            return ausentes

        else:
            df = self._leitura.copy()
            df = df[['Estudante', 'Data', 'Matrícula', 'Lançado']]
            df = df[df['Lançado'] == np.True_]
            print(f'{list(df['Lançado'].unique()) = }')
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

