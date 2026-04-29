from pandas import DataFrame


class TratamentoGêneros:

    def __init__(self, leitura: DataFrame):

        self.leitura = DataFrame(leitura)
        print(f'{list(self.leitura.columns) = }')
        self.df_tratado = self.tratar(self.leitura)
        print(f'df_tratado_\n{self.df_tratado.head()}')

    @staticmethod
    def tratar(leitura: DataFrame):
        df_base = leitura.copy()[['Matrícula', 'Sexo']][1:]
        df_base = df_base.rename(columns={'Sexo' : 'Gênero'})
        df_base = df_base.dropna(axis=0, how='all', ignore_index=True)
        return df_base

    def __getattr__(self, item):
        return getattr(self.df_tratado, item)
