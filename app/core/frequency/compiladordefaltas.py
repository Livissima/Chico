import os
from os import PathLike
from pathlib import Path
import pandas as pd

from app.config.parâmetros import parâmetros
import warnings
from openpyxl import __name__ as openpyxl_name

warnings.filterwarnings('ignore', category=UserWarning, module=openpyxl_name)
PATH_TEST = R'C:\Users\meren\PycharmProjects\Chico\tests\Compilado Faltas.csv'



class CompiladorDeFaltas:
    def __init__(self, diretório_base: PathLike | Path):
        self._diretório_fonte = Path(diretório_base, 'fonte')
        self._diretório_dfs = Path(diretório_base, 'fonte', 'Registro de Faltas')
        self.dataframes = self._ler_dfs()
        self.dataframes.to_csv(PATH_TEST)
        print(f'{self.dataframes = }')
        print(f'{self.dataframes.shape = }')

    # def _executar(self):
    #     self._ler_dfs()

    def _ler_dfs(self):
        lista_itens = os.listdir(self._diretório_dfs)
        lista_diretórios = [str(Path(self._diretório_dfs, item)) for item in lista_itens]

        dataframe_total = pd.DataFrame()
        for diretório_arquivo in lista_diretórios:

            if not diretório_arquivo.endswith('.xlsx') :
                print(f"O arquivo '{diretório_arquivo}' não é uma planilha válida.\n")
                continue

            try :
                df = pd.read_excel(diretório_arquivo, sheet_name='Compilado de Faltas', engine='openpyxl')
                dataframe_total = dataframe_total._append(df)
                print(f"O arquivo em '{diretório_arquivo}' é válido.")
                print(f'{list(df.columns) = }')

            except ValueError as e:
                print(f"A pasta de trabalho '{diretório_arquivo}' não contém uma planilha 'Compilado de Faltas': \n{e}.\n")

        return dataframe_total




if __name__ == '__main__' :
    CompiladorDeFaltas(parâmetros.diretório_base)
