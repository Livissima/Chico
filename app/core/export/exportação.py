from pathlib import Path

from app.core import ConsultaEstudantes
from app.core.export.exportações.exportaçãocsv import ExportaçãoCSV
from app.core.export.exportações.exportaçãojson import ExportaçãoJSON
from app.core.export.exportações.exportaçãoxlsx import ExportaçãoXLSX
from app.core.query.servidores.consultaservidores import ConsultaServidores


class Exportação:
    def __init__(
            self,
            consulta: ConsultaEstudantes | ConsultaServidores,
            path_destino: Path
    ):
        self._consulta = consulta
        self._path_destino = path_destino

        print(f'=> Dataframe final para exportação: {consulta.shape = }')

        self.exportar_tudo()

    def exportar_tudo(self):
        if isinstance(self._consulta, ConsultaEstudantes):
            ExportaçãoCSV(self._consulta, self._path_destino)
            ExportaçãoJSON(self._consulta, self._path_destino)
        ExportaçãoXLSX(self._consulta, self._path_destino)
