from pathlib import Path

from app.core import ConsultaEstudantes
from app.core.export.exportações.exportaçãocsv import ExportaçãoCSV
from app.core.export.exportações.exportaçãojson import ExportaçãoJSON
from app.core.export.exportações.exportaçãoxlsx import ExportaçãoXLSX
from app.core.query.servidores.consultaservidores import ConsultaServidores


class Exportação:
    #todo: Bolar uma forma de organizar subclasses para distinguir as exportações de estudantes e servidores

    def __init__(
            self,
            consulta: ConsultaEstudantes | ConsultaServidores,
            path_destino: Path
    ):

        print(f'=> Dataframe final para exportação: {consulta.shape = }')

        self.exportar_tudo(consulta, path_destino)

    @staticmethod
    def exportar_tudo(consulta, path):
        if consulta.shape[1] > 30:
            ExportaçãoCSV(consulta, path)
            ExportaçãoJSON(consulta, path)
        ExportaçãoXLSX(consulta, path)
