import numpy as np
import pandas as pd
from pandas import DataFrame


class Formatação:
    #todo adicionar método para reordenar as colunas

    _colunas_datas: list[str] = [
        'Data de Nascimento', 'Data Matrícula', 'Data Situação'
    ]
    _colunas_title: list[str] = [
        'Estudante', 'Nome Responsável', 'Filiação 1', 'Filiação 2', 'Município de Naturalidade', 'Nacionalidade',
        'Endereço: Logradouro', 'Endereço: Bairro', 'Endereço: Município', 'Irmão 1'
    ]
    _colunas_num: list[str] = [
        'Certidão de Nascimento: Folha', 'Certidão de Nascimento: Livro', 'Certidão de Nascimento: Termo'
    ]
    _colunas_num_string: list[str] = [
        'Matrícula', 'CPF Aluno', 'Filiação 1 - CPF', 'Filiação 2 - CPF', 'INEP'
    ]

    _colunas_ordenadas = [
        'Turma', 'Matrícula', 'Data Matrícula', 'Número pra chamada', 'Estudante', 'Nome Social', 'Gênero', 'Idade',
        'Data de Nascimento', 'CPF Aluno', 'Nome Responsável', 'Município de Naturalidade', 'UF de Naturalidade',
        'Nacionalidade', 'País de origem',  'Endereço: Logradouro', 'Endereço: Complemento', 'Endereço: Número',
        'Endereço: Bairro', 'Endereço: Município', 'Endereço: CEP', 'Filiação 1', 'Filiação 1 - Prof', 'Filiação 1 - CPF',
        'Filiação 1 - RG', 'Filiação 2', 'Filiação 2 - Prof', 'Filiação 2 - CPF', 'Filiação 2 - RG', 'Irmão 1',
        'Certidão de Nascimento: Termo', 'Certidão de Nascimento: Livro', 'Certidão de Nascimento: Folha', 'RG',
        'RG - Emissor', 'RG - Expedição', 'Telefone 1', 'Telefone 2', 'Telefone 3', 'Educacional', 'Senha padrão',
        'Nova senha', 'Senha educa',  'Curso', 'Série', 'Turno', 'INEP', 'Situação', 'Data Situação'
    ]

    def __init__(self, df_integrado: DataFrame):
        print(f'\nFormatação instanciada.\n')
        self._df = df_integrado

        print(f'Chegou como: {self._df.shape}')
        self.df_formatado: DataFrame = self._formatar(df_integrado)
        print(f'Resultado: {self.df_formatado.shape}\n')



    def _formatar(self, df_integrado: DataFrame) -> DataFrame:
        df_base = df_integrado
        df = self._formatar_case_title(df_base)
        df = self._formatar_como_número(df_base)
        df = self._formatar_como_data(df_base)
        df = self._formatar_como_string(df_base)

        df = self._remover_duplicatas(df)
        df = self._reordenar_colunas(df)
        return df


    def _formatar_case_title(self, df):
        dataframe = df
        for coluna in self._colunas_title:
            dataframe[coluna] = dataframe[coluna].astype(str).str.title()
            continue
        return dataframe

    def _formatar_como_número(self, df) :
        dataframe = df.copy()
        for coluna in self._colunas_num :
            extracted = dataframe[coluna].astype(str).str.extract(r'(\d+)')[0]
            numeric_series = pd.to_numeric(extracted, errors='coerce')
            numeric_series = numeric_series.replace([np.inf, -np.inf], np.nan)
            mask = numeric_series.notna()
            dataframe[coluna] = pd.Series([pd.NA] * len(numeric_series), dtype='Int64')
            dataframe.loc[mask, coluna] = numeric_series[mask].astype(np.int64)

        return dataframe

    def _formatar_como_data(self, df):
        dataframe = df
        for coluna in self._colunas_datas:
            dataframe[coluna] = pd.to_datetime(
                dataframe[coluna],
                format = 'mixed',
                dayfirst=True
            )
            dataframe[coluna] = dataframe[coluna].dt.strftime('%d/%m/%Y')
            continue
        return dataframe

    def _formatar_como_string(self, df):
        dataframe = df
        dataframe[self._colunas_num_string] = dataframe[self._colunas_num_string].astype(str)
        for coluna in self._colunas_num_string:
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
    def _remover_duplicatas(df):
        return df.drop_duplicates(subset= 'Matrícula', keep= 'first', ignore_index = True)

    def _reordenar_colunas(self, dataframe: pd.DataFrame) -> pd.DataFrame :
        return dataframe[self._colunas_ordenadas]

    #todo repensar a relevância desta método
    @staticmethod
    def remover_quebras_de_linhas(df: DataFrame) -> DataFrame:

        df = df.replace(to_replace = ['\r', '\n', '\t', '\xa0'], value = [' ', ' ', ' ', ' '], regex = True)
        df.columns = [str(coluna).replace('\r', ' ').replace('\n', ' ') for coluna in df.columns]
        return df


    # def __getattr__(self, item):
    #     return getattr(self.df_formatado, item)

    def __getitem__(self, item):
        return self.df_formatado[item]

    def __str__(self):
        return f'{self.df_formatado}'
