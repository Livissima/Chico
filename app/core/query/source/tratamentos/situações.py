from pandas import DataFrame
from app.core.query.workflow.formatação import Formatação


class TratamentoSituações:

    colunas_drop: list[str] = ['Ord.', 'Aluno', 'Data Nascimento', 'Data Matrícula']

    def __init__(self, leitura: DataFrame):
        self.df = leitura
        self.df_tratado = self.tratar(leitura)

        print(f'TratamentoSituações.df: {leitura.shape}. Colunas: {list(leitura.columns)}')   ### DEBUG  ###
        print(f'TratamentoSituações.df_tratado: {self.df_tratado.shape}. Colunas: {list(self.df_tratado.columns)}\n')

    def tratar(self, leitura):
        df_base = self._definir_df_base(leitura)
        # self._definir_df_base()

        df_tratado = self._pré_filtrar(df_base)

        ### DEBUG  ###
        # dbg_leitura(self)

        # self.df_tratado.to_excel(r'Tratamentos\situações.xlsx')   ### DEBUG  ###

        return df_tratado

    def _definir_df_base(self, leitura: DataFrame) -> DataFrame:
        df = leitura
        df = df.drop(columns=self.colunas_drop)
        df = Formatação.remover_quebras_de_linhas(df)
        df = df.rename({'Código INEP' : 'INEP'}, axis='columns')
        return df

    @staticmethod
    def _pré_filtrar(df_base: DataFrame) -> DataFrame:
        df_ajustado = df_base[df_base['Situação'].notna()]
        df_ajustado = df_base[~df_base['Situação'].fillna('').astype(str).str.startswith('(rem.')]

        df_ajustado = df_ajustado.dropna(axis=0, how='all', ignore_index=True)
        return df_ajustado


    def __getattr__(self, item):
        return getattr(self.df_tratado, item)
