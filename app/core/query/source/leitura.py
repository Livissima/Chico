from os import listdir, path
from pandas import DataFrame
from tabula import read_pdf
from typing import Literal


def dbg(self, tipo_de_relatório):
    print(f'Leitura._dataframe.shape: {self._dataframe.shape}')  ###  DBUG ####
    print(f'colunas: {self.dataframe.columns}\n')
    self._dataframe.to_excel(fr'Leitura\{tipo_de_relatório}\{tipo_de_relatório} - '
                             fr'{self.args_leitura[tipo_de_relatório]['guess']} '
                             fr'{self.args_leitura[tipo_de_relatório]['lattice']}, '
                             fr'{self.args_leitura[tipo_de_relatório]['relative_columns']}.xlsx')

class Leitura:

    args_leitura: dict[str, dict[str, bool]] = {
        'fichas':    {'guess': False, 'lattice': False, 'relative_columns': True},
        'contatos':  {
            'guess': False,
            'lattice': True,
            'relative_columns': False,
            'multiple_tables' : False
        },
        'gêneros':   {'guess': True,  'lattice': True,  'relative_columns': True},
        'situações': {'guess': True,  'lattice': True,  'relative_columns': False},
    }

    def __init__(
            self,
            path_pdfs: str,
            tipo_de_relatório: Literal['fichas', 'contatos', 'gêneros', 'situações']
    ):
        print(f'Leitura: {tipo_de_relatório}')


        self._tipo_de_relatório = tipo_de_relatório

        self._lista_arquivos = listdir(path_pdfs)
        self._path_pdfs = path_pdfs
        self._dataframe = self._ler_pdf()


    def _ler_pdf(self) -> DataFrame:
        df_resultante = DataFrame()

        for nome_arquivo in self._lista_arquivos:

            if not nome_arquivo.endswith('.pdf'):
                continue

            caminho_completo = path.join(self._path_pdfs, nome_arquivo)

            try:
                config  = self.args_leitura[self._tipo_de_relatório]
                leitura = read_pdf(caminho_completo, pages='all', **config)
                if not Leitura:
                    print(f'Nenhum dado extraído de {nome_arquivo}, {self._tipo_de_relatório}')

                for pdf_lido in leitura:
                    df_pdf = DataFrame(pdf_lido)
                    df_resultante = df_resultante._append(pdf_lido, ignore_index=True)

            except Exception as e:
                print(f'\nErro ao ler {nome_arquivo}, {self._tipo_de_relatório}: \n{e}\n')
        return df_resultante

    @property
    def dataframe(self):
        return self._dataframe




    # def __getattr__(self, attr):
    #     return getattr(self._dataframe, attr)



