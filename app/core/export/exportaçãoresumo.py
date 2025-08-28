import os
from typing import Literal
from pandas import DataFrame, ExcelWriter

class ExportaçãoResumo:
    def __init__(self, consulta, path):
        self.consulta: DataFrame = consulta
        self.path = path
        self.exportar_resumo()

    def exportar_resumo(self):
        resumo = self.elaborar_resumo()
        resumo.to_csv(
            os.path.join(self.path, 'Resumo.csv'),
            index=False)
        # with ExcelWriter(
        #         path=os.path.join(self.path, 'Resumo.xlsx'),
        #         engine='xlsxwriter'
        # ) as self.writer:
        #     resumo.to_excel(
        #         self.writer,
        #         sheet_name='Resumo',
        #     )

    def elaborar_resumo(self):
        consulta = self.consulta
        resumo = DataFrame()


        turmas = consulta['Turma'].unique().tolist()
        resumo['Turmas'] = turmas

        return resumo


