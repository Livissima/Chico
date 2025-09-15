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

    def __init__(
            self,
            df_leitura: dict | DataFrame,
            tipo: Literal['fichas', 'contatos', 'gêneros', 'situações']
    ):
        self.tipo = tipo

        classe_tratamento = self.tipos.get(tipo)
        if classe_tratamento is None:
            raise ValueError(f'Tipo de tratamento "{tipo}" não reconhecido')

        self.df_tratado = classe_tratamento(df_leitura).df_tratado

    def __getattr__(self, item):
        return getattr(self.df_tratado, item)





