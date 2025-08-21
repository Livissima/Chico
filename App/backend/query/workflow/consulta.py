from App.backend.query.source.tratamentos.tratamento import Tratamento
from App.backend.query.workflow.formatação import Formatação
from App.backend.query.workflow.integração import Integração
from App.backend.query.source.leitura import Leitura
from pandas import DataFrame


class Consulta:

    def __init__(
            self,
            path_fichas: str,
            path_contatos: str,
            path_situações: str,
            path_gêneros: str
    ):
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
            tipo: Leitura(path_pdfs=path, tipo_de_relatório=tipo)
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



