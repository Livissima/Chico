from pathlib import Path

from app.core.query.leitura import Leitura


class ConsultaServidores:

    def __init__(
            self,
            diretório_fonte: str | Path
    ):
        print(f'class ConsultaServidores instanciada: {diretório_fonte = }')

        self.dataframe = self._consultar(diretório_fonte)

    def _consultar(self, path: Path):

        df_leitura = Leitura(path, 'servidores').dataframe
        print(f'{path = }')
        print(f'\n{df_leitura = }\n')
        return df_leitura
