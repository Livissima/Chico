from pandas import DataFrame
from app.core.query.workflow.formatação import Formatação


class TratamentoSituações:

    def __init__(self, leitura: list[dict[str, str]]):

        self.df = DataFrame(leitura)
        self.df_tratado = self.tratar(self.df)

    def tratar(self, leitura: DataFrame) -> DataFrame:
        df_base = self._definir_df_base(leitura)
        df_tratado = self._pré_filtrar(df_base)
        return df_tratado

    def _definir_df_base(self, leitura: DataFrame) -> DataFrame:
        df = leitura[self.colunas]
        df = Formatação.remover_quebras_de_linhas(df)
        df = df.rename({'Código INEP' : 'INEP'}, axis='columns')
        return df

    @staticmethod
    def _pré_filtrar(df_base: DataFrame) -> DataFrame:
        df_ajustado = df_base[df_base['Situação'].notna()]
        df_ajustado = df_base[~df_base['Situação'].fillna('').astype(str).str.startswith('(rem.')]

        df_ajustado = df_ajustado.dropna(axis=0, how='all', ignore_index=True)
        return df_ajustado

    @property
    def colunas(self) -> list[str]:
        return ['Data Situação', 'Matrícula', 'Situação', 'Código INEP']

    def __getattr__(self, item):
        return getattr(self.df_tratado, item)