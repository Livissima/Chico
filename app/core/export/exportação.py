from pathlib import Path

from pandas import DataFrame

from app.core import Consulta
from app.core.export.exportaçãocsv import ExportaçãoCSV
from app.core.export.exportaçãoxlsx import ExportaçãoXLSX


class Exportação:
    #todo exportar um ATALHO para área de trabalho. Path(user_desktop_dir())
    def __init__(
            self,
            consulta: Consulta,
            path_destino: Path
    ):

        print(f'df_formatado chegando na exportação: {consulta.shape}')

        self.consulta = consulta
        self.path = path_destino
        self._exportar_ambos()

    def _exportar_ambos(self):
        ExportaçãoXLSX(self.consulta, self.path)
        ExportaçãoCSV(self.consulta, self.path)







