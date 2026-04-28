import os
from app.core.query.estudantes.pipeline.processamentoinicial import ProcessamentoInicial
from app.core.query.estudantes.pipeline.formatação import Formatação
from app.core.query.estudantes.pipeline.integraçãodeextras import IntegraçãoDeExtras
from app.core.query.leitura import Leitura
from pandas import DataFrame


class ConsultaEstudantes:

    def __init__(
            self,
            diretório_fonte: str
    ):
        print(f'Class Consulta instanciada: {diretório_fonte = }\n')

        self._paths = {
            tipo_de_relatorio : os.path.join(diretório_fonte, tipo_de_relatorio) for tipo_de_relatorio in
            ("fichas", "contatos", "situações", "gêneros")
        }
        self.dataframe = self._consultar(diretório_fonte)

    def _consultar(self, _path) -> DataFrame:
        dados_brutos = self._ler()
        dados_processados = self._processar(dados_brutos)

        df_integrado = IntegraçãoDeExtras(dados_processados).df_integrado
        df_formatado = Formatação(df_integrado).df_formatado
        return df_formatado

    def _ler(self) -> dict[str, Leitura]:
        return {
            tipo: Leitura(_path=path, tipo_de_relatório=tipo)
            for tipo, path in self._paths.items()
        }

    @staticmethod
    def _processar(dfs_leituras: dict) -> dict:
        return {
            tipo : ProcessamentoInicial(leitura.fluxo_inicial, tipo)
            for tipo, leitura in dfs_leituras.items()
        }


    def __str__(self):
        return f"{self.dataframe}"

    def __getattr__(self, attr):
        return getattr(self.dataframe, attr)

    def __getitem__(self, item):
        return self.dataframe[item]



