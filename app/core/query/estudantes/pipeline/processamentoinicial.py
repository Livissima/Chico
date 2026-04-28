from typing import Literal, Iterable
from pandas import DataFrame
from app.core.query.estudantes.processamento.fichas import TratamentoFichas
from app.core.query.estudantes.processamento.contatos import TratamentoContatos
from app.core.query.estudantes.processamento.situações import TratamentoSituações
from app.core.query.estudantes.processamento.gêneros import TratamentoGêneros


class ProcessamentoInicial:
    tipos = {
        'fichas'    : TratamentoFichas,
        'contatos'  : TratamentoContatos,
        'situações' : TratamentoSituações,
        'gêneros'   : TratamentoGêneros
    }

    def __init__(
            self,
            fluxo_leitura: Iterable,
            tipo: Literal['fichas', 'contatos', 'gêneros', 'situações']
    ):
        classe_tratamento = self.tipos.get(tipo)

        tratamento = classe_tratamento(fluxo_leitura)

        self.fluxo = tratamento.fluxo

    def __getattr__(self, item):
        return getattr(self.fluxo, item)







