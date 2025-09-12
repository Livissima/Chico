from os import listdir, path
from pandas import DataFrame, concat
from tabula import read_pdf
from typing import Literal
import json
import pandas as pd

class Leitura :

    def __init__(
            self,
            _path: str,
            tipo_de_relatório: Literal['fichas', 'contatos', 'gêneros', 'situações']
    ) :
        print(f'Leitura: {tipo_de_relatório}')
        self._tipo_de_relatório = tipo_de_relatório
        self._path_dados = _path
        self.df_leitura = self._ler(_path, tipo_de_relatório)

    @staticmethod
    def _ler(_path, tipo) -> list | DataFrame :
        #todo: talvez usar método de leitura de json do pandas.
        tipos = {'fichas', 'contatos', 'situações', 'gêneros'}
        tipos_simples = {'contatos', 'situações', 'gêneros'}
        leitura = None

        for nome_arquivo in listdir(_path):

            if not nome_arquivo.endswith('.json'):
                continue

            caminho_completo = path.join(_path, nome_arquivo)

            try:
                with open(caminho_completo, 'r', encoding='utf-8') as arquivo:
                    dados = json.load(arquivo)
            except Exception as e:
                print(f'Erro ao ler {nome_arquivo}: {e}')

            if tipo == 'fichas':
                if dados:
                    leitura = dados
                    print(f'✓ {len(dados)} linhas de {nome_arquivo}')


            if tipo in tipos_simples:
                leitura = DataFrame()
                if dados :
                    df_arquivo = pd.DataFrame(dados)
                    leitura = concat([leitura, df_arquivo], ignore_index=True)
                    print(f'✓ {len(dados)} linhas de {nome_arquivo}')

        return leitura

    @property
    def dataframe(self) :
        return self.df_leitura

