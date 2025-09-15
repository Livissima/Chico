import re
from pandas import DataFrame, Series
import pandas as pd
from app.core.query.workflow.formatação import Formatação


class TratamentoContatos:

    def __init__(self, leitura: list[dict[str, str]]) -> None:
        self.df = DataFrame(leitura)
        self.df_tratado = self.tratar(self.df)

    def tratar(self, leitura: DataFrame) -> Series:
        df_base = self._definir_df_base(leitura)
        df_limpo = self._limpar_strings_telefones(df_base)
        df = self._aplicar_funções_telefones(df_limpo)
        return df

    def _definir_df_base(self, leitura: DataFrame) -> DataFrame:

        df_base: DataFrame = Formatação.renomear_colunas(leitura, self.map_colunas)
        df_base = Formatação.remover_quebras_de_linhas(df_base)
        df_base = df_base.loc[:, ~df_base.columns.duplicated()]
        df_base = df_base.drop_duplicates()
        df_base = df_base[1:]
        df_base = df_base[self.colunas]
        return df_base

    def _limpar_strings_telefones(self, df_base: DataFrame) -> DataFrame:
        def clean_phone_number(x) :
            return re.sub('[^0-9]+', '', str(x)) if isinstance(x, str) else x

        df = df_base
        df[self.colunas_telefone] = df[self.colunas_telefone].applymap(clean_phone_number)
        return df

    def _aplicar_funções_telefones(self, df_limpo: DataFrame) -> Series:
        df = df_limpo
        df = df.apply(self._remover_telefones_duplicados, axis=1)
        df = df.apply(self._ordenar_por_coluna, axis=1)
        for col in self.colunas_telefone:
            df[col] = df[col].apply(self._normalizar_cumprimento)
        return df

    def _remover_telefones_duplicados(self, linha):
        telephones = list(linha.loc[self.colunas_telefone])
        unique_telephones = list(dict.fromkeys(filter(pd.notna, telephones)))
        for i in range(3):
            linha[f'Telefone {i + 1}'] = (
                unique_telephones)[i] if i < len(unique_telephones) \
                else pd.NA
        return linha

    def _ordenar_por_coluna(self, linha):
        colunas_telefone = self.colunas_telefone
        telefones = []
        for coluna in colunas_telefone:
            valor = linha.get(coluna)
            if pd.isna(valor) or valor == '':
                telefones.append('')
            else:
                telefones.append(valor)

        sorted_telefones = sorted(telefones, key=lambda x: (x == '', x))

        for i, coluna in enumerate(colunas_telefone):
            linha[coluna] = sorted_telefones[i]

        return linha

    @staticmethod
    def _normalizar_cumprimento(telefone) -> str:
        if pd.isna(telefone) or telefone == '':
            return telefone

        telefone = str(telefone).strip()

        if len(telefone) == 10:
            ddd = telefone[:2]
            numero = telefone[2:]
            if numero[0] in '6789':
                return f"{ddd}9{numero}"
            else:
                return telefone

        elif len(telefone) == 11:
            ddd = telefone[:2]
            numero = telefone[2:]
            if numero[0] == '9':
                return telefone
            elif numero[0] in '6789':
                return telefone
            else:
                return f"{ddd}9{numero}"

        return telefone

    @property
    def colunas_telefone(self) -> list[str]:
        return ['Telefone 1', 'Telefone 2', 'Telefone 3']

    @property
    def colunas(self) -> list[str]:
        return ['Matrícula', 'Telefone 1', 'Telefone 2', 'Telefone 3', 'Educacional']

    @property
    def map_colunas(self) -> dict[str, str]:
        return {
            'Telefone residencial' : 'Telefone 1', 'Telefone responsável' : 'Telefone 2',
            'Telefone celular' : 'Telefone 3', 'E-mail Educacional' : 'Educacional',
            'E-mail Alternativo' : 'Email alternativo'
        }

    def __getattr__(self, item):
        return getattr(self.df_tratado, item)
