import os

from app.core.query.source.tratamentos.tratamento import Tratamento
from app.core.query.workflow.formatação import Formatação
from app.core.query.workflow.integração import Integração
from app.core.query.source.leitura import Leitura
from pandas import DataFrame


class Consulta:

    def __init__(
            self,
            diretório_fonte: str
    ):
        path_fichas: str = os.path.join(diretório_fonte, 'fichas')
        path_contatos: str = os.path.join(diretório_fonte, 'contatos')
        path_situações: str = os.path.join(diretório_fonte, 'situações')
        path_gêneros: str = os.path.join(diretório_fonte, 'gêneros')

        print('class Consulta instanciada.\n')

        self.paths = {
            'fichas'   : path_fichas,
            'contatos' : path_contatos,
            'situações': path_situações,
            'gêneros'  : path_gêneros
        }

        self.dfs_leitura   = self._ler()
        self.dfs_tratados  = self._tratar(self.dfs_leitura)
        self.df_integrado  = self._integrar(self.dfs_tratados)
        self.dataframe     = self._formatar(self.df_integrado)


    def _ler(self) -> dict[str, Leitura]:
        return {
            tipo: Leitura(_path=path, tipo_de_relatório=tipo)
            for tipo, path in self.paths.items()
        }

    @staticmethod
    def _tratar(dfs_leituras: dict) -> dict:
        return {
            tipo : Tratamento(leitura.dataframe, tipo)
            for tipo, leitura in dfs_leituras.items()
        }

    @staticmethod
    def _integrar(dfs_tratados: dict) -> DataFrame:
        df = Integração(dfs_tratados)
        return df.integração

    @staticmethod
    def _formatar(df_integrado: DataFrame) -> DataFrame:
        df_formatado = Formatação(df_integrado)
        return df_formatado

    def __str__(self):
        return f"{self.dataframe}"

    def __getattr__(self, attr):
        return getattr(self.dataframe, attr)

    def __getitem__(self, item):
        return self.dataframe[item]



