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
        classe_tratamento = self.tipos.get(tipo)

        self.df_tratado: DataFrame = classe_tratamento(df_leitura).df_tratado

    def __getattr__(self, item):
        return getattr(self.df_tratado, item)







