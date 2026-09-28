from pathlib import Path

from app.core import ConsultaEstudantes
from app.core.export.exportações.exportaçãocontatoscsv import ExportaçãoContatosCSV
from app.core.export.exportações.exportaçãodatabasejson import ExportaçãoDatabaseJSON
from app.core.export.exportações.exportaçãodatabasexlsx import ExportaçãoDatabaseXLSX
from app.core.query.servidores.consultaservidores import ConsultaServidores


class Exportação:
    def __init__(
            self,
            consulta: ConsultaEstudantes | ConsultaServidores,
            path_destino: Path
    ):
        print(f'=> Dataframe final para exportação: {type(consulta) = }{consulta.shape = }')
        self._path = path_destino
        self._consulta = consulta

        self.exportar_tudo()


    def exportar_tudo(self):
        if isinstance(self._consulta, ConsultaEstudantes):
            ExportaçãoContatosCSV(self._consulta, self._path)
            ExportaçãoDatabaseJSON(self._consulta, self._path)
        ExportaçãoDatabaseXLSX(self._consulta, self._path)
