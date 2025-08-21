import pathlib

from pandas import DataFrame
from app.backend.export.exportaçãocsv import ExportaçãoCSV
from app.backend.export.exportaçãoxlsx import ExportaçãoXLSX


class Exportação:

    def __init__(
            self,
            consulta: DataFrame,
            path_destino: str
    ):

        print(f'df_formatado chegando na exportação: {consulta.shape}')

        self.consulta = consulta
        self.path = path_destino
        self._exportar_ambos()

    def _exportar_ambos(self):
        ExportaçãoXLSX(self.consulta, self.path)
        ExportaçãoCSV(self.consulta, self.path)







