import pandas as pd
from pandas import DataFrame


class Formatação:
    #todo adicionar método para reordenar as colunas

    colunas_datas: list[str] = [
        'Data de Nascimento', 'Data Matrícula', 'Data Situação'
    ]
    colunas_title: list[str] = [
        'Estudante', 'Nome Responsável', 'Filiação 1', 'Filiação 2', 'Município de Naturalidade', 'Nacionalidade',
        'Endereço: Logradouro', 'Endereço: Bairro', 'Endereço: Município', 'Irmão 1'
    ]
    colunas_num: list[str] = [
        'Certidão de Nascimento: Folha', 'Certidão de Nascimento: Livro', 'Certidão de Nascimento: Termo'
    ]
    colunas_num_string: list[str] = [
        'Matrícula', 'CPF Aluno', 'Filiação 1 - CPF', 'Filiação 2 - CPF', 'INEP', 'Certidão de Nascimento - Modelo novo'
    ]

    def __init__(self, df_integrado: DataFrame):
        print(f'\nFormatação instanciada.\n')
        self.df = df_integrado

        print(f'Chegou como: {self.df.shape}')
        self.df_formatado: DataFrame = self._formatar(df_integrado)
        print(f'Resultado: {self.df_formatado.shape}\n')



    def _formatar(self, df_integrado: DataFrame) -> DataFrame:
        df_base = df_integrado
        df = self._title(df_base)
        df = self._numerizar(df_base)
        df = self._datar(df_base)
        df = self._stringzar_números(df_base)

        df = df.drop_duplicates(subset= 'Matrícula', keep= 'first', ignore_index = True)

        return df


    def _title(self, df):
        dataframe = df
        for coluna in self.colunas_title:
            dataframe[coluna] = dataframe[coluna].astype(str).str.title()
            continue
        return dataframe

    def _numerizar(self, df):
        dataframe = df
        for coluna in self.colunas_num:
            dataframe[coluna] = dataframe[coluna].astype(str).str.extract(r'(\d+)')[0]
            dataframe[coluna] = pd.to_numeric(self.df[coluna], errors = 'coerce')
            dataframe[coluna] = dataframe[coluna].astype('Int64')
            continue
        return dataframe

    def _datar(self, df):
        dataframe = df
        for coluna in self.colunas_datas:
            dataframe[coluna] = pd.to_datetime(dataframe[coluna], format = '%d/%m/%Y')
            dataframe[coluna] = dataframe[coluna].dt.strftime('%d/%m/%Y')
            continue
        return dataframe

    def _stringzar_números(self, df):
        dataframe = df
        dataframe[self.colunas_num_string] = dataframe[self.colunas_num_string].astype(str)
        for coluna in self.colunas_num_string:
            dataframe[coluna] = dataframe[coluna].str.replace(
                '.', '', regex = False).str.replace(
                '-', '', regex = False).str.replace(
                'nan', '', regex=False).str.replace(
                'None', ''
            )
            dataframe[coluna] = dataframe[coluna].astype(str)
            dataframe[coluna] = dataframe[coluna].fillna('')  #todo considerar a possibilidade de um método de fillsna
            continue
        return dataframe

    @staticmethod
    def remover_quebras_de_linhas(df: DataFrame) -> DataFrame:
        df = df.replace(to_replace = ['\r', '\n'], value = [' ', ' '], regex = True)
        df.columns = [coluna.replace('\r', ' ').replace('\n', ' ') for coluna in df.columns]
        return df

    @staticmethod
    def renomear_colunas(df: DataFrame, dicionário: dict[str, str]) -> DataFrame:
        df.rename(columns = dicionário, inplace = True)
        return df

    def __getattr__(self, item):
        return getattr(self.df_formatado, item)

    def __getitem__(self, item):
        return self.df_formatado[item]

    def __str__(self):
        return f'{self.df_formatado}'
