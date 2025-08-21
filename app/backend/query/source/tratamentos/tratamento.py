from typing import Literal

from pandas import DataFrame

from .fichas import TratamentoFichas
from .contatos import TratamentoContatos
from .situações import TratamentoSituações
from .gêneros import TratamentoGêneros


class Tratamento:
    tipos = {
        'fichas'    : TratamentoFichas,
        'contatos'  : TratamentoContatos,
        'situações' : TratamentoSituações,
        'gêneros'   : TratamentoGêneros
    }

    def __init__(self, df_leitura: DataFrame, tipo: Literal['fichas', 'contatos', 'gêneros', 'situações']):
        self.tipo = tipo

        print(f'\nTratamento{tipo.title()}: {df_leitura.shape}. Colunas iniciais: {list(df_leitura.columns)}')

        classe_tratamento = self.tipos.get(tipo)
        if classe_tratamento is None:
            raise ValueError(f'Tipo de tratamento "{tipo}" não reconhecido')

        self.df_tratado = classe_tratamento(df_leitura).df_tratado

        print(f'Tratamento{tipo.title()}.df_tratado: {df_leitura.shape}. Colunas: {list(df_leitura.columns)}')

    # @property
    # def dataframe(self):



    # def tratar(self):
    #     return self.df_tratado.tratar()

    def __getattr__(self, item):
        return getattr(self.df_tratado, item)

    # def __getitem__(self, item):
    #     return self.df_tratado[item]

    # def __str__(self):
    #     return self.df_tratado





