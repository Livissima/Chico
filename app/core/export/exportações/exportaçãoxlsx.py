import os
from os import PathLike
from pathlib import Path
from typing import Literal, Any
from pandas import DataFrame, ExcelWriter

from app.core import ConsultaEstudantes


class ExportaçãoXLSX :
    NOME_XLSX = 'Database'

    def __init__(self, consulta: ConsultaEstudantes, path: Path) -> None :
        self._executar(consulta, path)

    def _executar(self, consulta, path):
        _path = Path(path, f'{self.NOME_XLSX}.xlsx')

        df_ativa = consulta[consulta['Situação'] == 'Cursando'].copy()
        df_bruta = consulta.copy()
        df_transferidos = consulta[consulta['Situação'] == '(transferido)'].copy()

        self._gerar_xlsx(_path, [df_ativa, df_bruta, df_transferidos])


    def _gerar_xlsx(self, path: Path, dfs: list[DataFrame]) -> None :
        with ExcelWriter(path=path, engine='xlsxwriter', date_format='DD/MM/YYYY') as writer :
            self._planilhar_dataframe(writer, dfs[0], 'Base Ativa')
            self._planilhar_dataframe(writer, dfs[1], 'Base Bruta')
            self._planilhar_dataframe(writer, dfs[2], 'Transferidos')


    def _planilhar_dataframe(self, writer: ExcelWriter, dataframe: DataFrame, nome_planilha: str) :
        dataframe.to_excel(writer, sheet_name=nome_planilha, index=False)
        pasta_de_trabalho = writer.book
        planilha = writer.sheets[nome_planilha]

        formato_fonte = self.__formatar_fonte(pasta_de_trabalho)
        formato_cabeçalho = self.__formatar_cabeçalho(pasta_de_trabalho)

        planilha.set_column(0, dataframe.shape[1] - 1, None, formato_fonte)

        for col_num, valor in enumerate(dataframe.columns.values) :
            planilha.write(0, col_num, valor, formato_cabeçalho)

        self.__formatar_como_tabela(dataframe, planilha, nome_planilha)

    @staticmethod
    def __formatar_como_tabela(df, planilha, nome) -> None :
        linhas = df.shape[0]
        colunas = df.shape[1]

        # Configurar a tabela
        planilha.add_table(0, 0, linhas, colunas - 1, {
            'name' : nome.replace(' ', '_'),
            'columns' : [{'header' : col} for col in df.columns],
            'style' : 'Table Style Medium 2',
            'autofilter' : True
        })
        planilha.hide_gridlines(2)

    @staticmethod
    def __formatar_cabeçalho(pasta_de_trabalho) -> dict[str, str | int | bool] :
        return pasta_de_trabalho.add_format({
            "font_name" : "Times New Roman",
            "font_size" : 12,
            "bold" : True,
            "bg_color" : "#D3D3D3",
            "border" : 1
        })

    @staticmethod
    def __formatar_fonte(pasta_de_trabalho) -> dict[str, str | int] :
        return pasta_de_trabalho.add_format({
            "font_name" : "Times New Roman",
            "font_size" : 12
        })
