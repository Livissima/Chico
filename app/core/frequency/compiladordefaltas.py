import os
from os import PathLike
from pathlib import Path
import pandas as pd
from pandas import DataFrame
from app.config.parâmetros import parâmetros
import warnings
from openpyxl import __name__ as openpyxl_name

pd.set_option('display.max_columns', None)
warnings.filterwarnings('ignore', category=UserWarning, module=openpyxl_name)
PATH_TEST = R'C:\Users\meren\PycharmProjects\Chico\tests\Compilado Faltas.csv'


class CompiladorDeFaltas:
    def __init__(self, diretório_base: PathLike | Path):
        self._path_pasta_registros = Path(diretório_base, 'fonte', 'Controle de Frequência', 'Registro de Faltas')
        self.compilado_nominal_de_faltas = self._compilar_faltas()




    def _compilar_faltas(self):
        df_inicial = self._ler_dfs()
        compilado = self._tratar(df_inicial)
        return compilado

    @staticmethod
    def _tratar(df_inicial: DataFrame):
        df = df_inicial.copy()
        df['Lançado'] = df['Lançado'].fillna('')
        df['Lançado'] = df['Lançado'].replace([0.0, '',  'Lançado'], ['False', 'False', 'True'])
        df['Data'] = df['Data'].dt.strftime('%d/%m/%Y')
        return df

    def _ler_dfs(self):
        dataframe_total = pd.DataFrame()
        for diretório_arquivo in self._diretórios_registros:
            if diretório_arquivo.suffix not in ['.xlsx', '.xlsm'] :  #todo: implementar csv no futuro
                continue

            try :
                dicionário_dataframes = pd.read_excel(
                    diretório_arquivo, sheet_name=parâmetros.turmas_disponíveis, engine='openpyxl')

                for turma, dataframe in dicionário_dataframes.items() :
                    dataframe = dataframe[['Estudante', 'Data', 'Lançado']].copy()
                    dataframe = dataframe.dropna(axis=0)
                    dataframe['Turma'] = turma
                    dataframe_total = dataframe_total._append(dataframe, ignore_index=True)

            except ValueError as e:
                pass

        return dataframe_total

    # def exportar(self):
    #     self.compilado_nominal_de_faltas.





    @property
    def _diretórios_registros(self) -> list[Path]:
        lista_itens = os.listdir(self._path_pasta_registros)
        lista_diretórios = [Path(self._path_pasta_registros, item) for item in lista_itens]
        return lista_diretórios

if __name__ == '__main__' :
    CompiladorDeFaltas(parâmetros.diretório_base)
