from os import listdir, path
from pandas import DataFrame, concat
from tabula import read_pdf
from typing import Literal
import json
import pandas as pd


def dbg(self, tipo_de_relatório) :
    print(f'Leitura._dataframe.shape: {self._dataframe.shape}')  ###  DBUG ####
    print(f'colunas: {self.dataframe.columns}\n')
    self._dataframe.to_excel(fr'Leitura\{tipo_de_relatório}\{tipo_de_relatório} - '
                             fr'{self.args_leitura[tipo_de_relatório]["guess"]} '
                             fr'{self.args_leitura[tipo_de_relatório]["lattice"]}, '
                             fr'{self.args_leitura[tipo_de_relatório]["relative_columns"]}.xlsx')


class Leitura :
    args_leitura: dict[str, dict[str, bool]] = {
        'fichas' : {'guess' : False, 'lattice' : False, 'relative_columns' : True}, 'contatos' : {
            'guess' : False, 'lattice' : True, 'relative_columns' : False, 'multiple_tables' : False
        }, 'gêneros' : {'guess' : True, 'lattice' : True, 'relative_columns' : True},
        'situações' : {'guess' : True, 'lattice' : True, 'relative_columns' : False},
    }

    def __init__(self, _path: str, tipo_de_relatório: Literal['fichas', 'contatos', 'gêneros', 'situações']) :
        print(f'Leitura: {tipo_de_relatório}')
        self._tipo_de_relatório = tipo_de_relatório
        self._path_dados = _path

        # Determina o método de leitura baseado no tipo
        if tipo_de_relatório == 'fichas' :
            self._dataframe = self._ler_pdfs()
        else :
            self._dataframe = self._ler_jsons()

    def _ler_pdfs(self) -> DataFrame :
        """Lê PDFs - mantido para compatibilidade com fichas"""
        df_resultante = DataFrame()
        path_pdfs = self._path_dados

        for nome_arquivo in listdir(path_pdfs) :
            if not nome_arquivo.endswith('.pdf') :
                continue

            caminho_completo = path.join(path_pdfs, nome_arquivo)

            try :
                config = self.args_leitura[self._tipo_de_relatório]
                leitura = read_pdf(caminho_completo, pages='all', **config)

                if not leitura :
                    print(f'Nenhum dado extraído de {nome_arquivo}, {self._tipo_de_relatório}')
                    continue

                for pdf_lido in leitura :
                    df_pdf = DataFrame(pdf_lido)
                    df_resultante = concat([df_resultante, df_pdf], ignore_index=True)

            except Exception as e :
                print(f'\nErro ao ler {nome_arquivo}, {self._tipo_de_relatório}: \n{e}\n')

        return df_resultante

    def _ler_jsons(self) -> DataFrame :
        """Lê JSONs - novo método para tabelas extraídas via Selenium"""
        df_resultante = DataFrame()
        path_jsons = self._path_dados

        for nome_arquivo in listdir(path_jsons) :
            if not nome_arquivo.endswith('.json') :
                continue

            caminho_completo = path.join(path_jsons, nome_arquivo)

            try :
                with open(caminho_completo, 'r', encoding='utf-8') as f :
                    dados = json.load(f)

                if dados :
                    df_arquivo = pd.DataFrame(dados)
                    df_resultante = concat([df_resultante, df_arquivo], ignore_index=True)
                    print(f'✓ {len(dados)} linhas de {nome_arquivo}')

            except Exception as e :
                print(f'Erro ao ler {nome_arquivo}: {e}')

        return df_resultante

    @property
    def dataframe(self) :
        return self._dataframe
