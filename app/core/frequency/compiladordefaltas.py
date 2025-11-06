import os
from os import PathLike
from pathlib import Path
import pandas as pd
from pandas import DataFrame
from app.config.parâmetros import parâmetros
import warnings
from openpyxl import __name__ as openpyxl_name

pd.set_option('display.max_columns', None)
pd.set_option('display.expand_frame_repr', False)  # Evita quebra do DataFrame em múltiplas linhas
pd.set_option('display.width', None)  # Ajusta automaticamente à largura do terminal
warnings.filterwarnings('ignore', category=UserWarning, module=openpyxl_name)
PATH_TEST = R'C:\Users\meren\PycharmProjects\Chico\tests\Compilado de Faltas.csv'


class CompiladorDeFaltas:
    def __init__(self, diretório_base: PathLike | Path):
        self._path = Path(diretório_base, 'fonte', 'Controle de Frequência')
        self._compilado_nominal_de_faltas = self._compilar_faltas()
        print(f'{self._compilado_nominal_de_faltas}')


    def exportar_compilado(self):
        destino = Path(self._path, 'Compilado de Faltas.csv')
        self._compilado_nominal_de_faltas.to_csv(destino, sep=',', index=False)


    def _compilar_faltas(self):
        df_inicial = self._ler_dfs()
        compilado = self._tratar(df_inicial)
        return compilado


    @staticmethod
    def _tratar(df_inicial: DataFrame):
        df = df_inicial.copy()
        df['Lançado'] = df['Lançado'].fillna('')
        df['Data']    = df['Data'].dt.strftime('%d/%m/%Y')
        return df


    def _ler_dfs(self):
        dataframe_total = pd.DataFrame()
        for diretório_arquivo in self._diretórios_registros:
            if diretório_arquivo.suffix not in ['.xlsx', '.xlsm'] :  #todo: implementar csv no futuro
                continue

            try :
                dicionário_dataframes = pd.read_excel(
                    diretório_arquivo, sheet_name=parâmetros.turmas_disponíveis, engine='openpyxl')

                print(f'_________{diretório_arquivo = }')
                for turma, dataframe in dicionário_dataframes.items() :
                    # print(f'{turma}:\n{list(dataframe.columns)}')
                    dataframe = dataframe[['Estudante', 'Data', 'Lançado', 'Matrícula']].copy()
                    dataframe = dataframe.dropna(axis=0)
                    dataframe['Turma'] = turma
                    dataframe['Matrícula'] = dataframe['Matrícula'].astype(int).astype(str)
                    dataframe_total = dataframe_total._append(dataframe, ignore_index=True)

            except ValueError:
                pass

        return dataframe_total


    @property
    def _diretórios_registros(self) -> list[Path]:
        path_pasta_registro_de_faltas = Path(self._path, 'Registro de Faltas')
        lista_itens = os.listdir(path_pasta_registro_de_faltas)
        lista_diretórios = [Path(path_pasta_registro_de_faltas, item) for item in lista_itens]
        return lista_diretórios


if __name__ == '__main__' :
    CompiladorDeFaltas(parâmetros.diretório_base).exportar_compilado()
