from os import listdir, path
from pandas import DataFrame, concat
from typing import Literal
import json

class Leitura :

    def __init__(
            self,
            _path: str,
            tipo_de_relatório: Literal['fichas', 'contatos', 'gêneros', 'situações']
    ) :
        print(f'Leitura: {tipo_de_relatório}')

        self._tipo_de_relatório = tipo_de_relatório
        self._path_dados = _path
        self.df_leitura = self._ler(_path)


    def _ler(self, _path) -> list[str | dict] :
        lista_dirs = listdir(_path)
        # print(f'___________LISTA_DIRS{lista_dirs}')
        leitura = []
        for nome_arquivo in lista_dirs:
            dados = self.ler_json(nome_arquivo, _path)
            leitura.extend(dados)

        return leitura

    @property
    def dataframe(self) :
        return self.df_leitura

    @staticmethod
    def ler_json(_nome_arquivo: str, _path):

        caminho_completo = path.join(_path, _nome_arquivo)
        try :
            with open(caminho_completo, 'r', encoding='utf-8') as arquivo :
                return json.load(arquivo)
        except Exception as e :
            print(f'Erro ao ler {_nome_arquivo}: {e}')
            return []


