from typing import Literal
from pandas import DataFrame
from app.core.query.estudantes.tratamentos.fichas import TratamentoFichas
from app.core.query.estudantes.tratamentos.contatos import TratamentoContatos
from app.core.query.estudantes.tratamentos.situações import TratamentoSituações
from app.core.query.estudantes.tratamentos.gêneros import TratamentoGêneros


class ProcessamentoInicial:
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







