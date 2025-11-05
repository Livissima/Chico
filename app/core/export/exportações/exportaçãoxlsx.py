import os
from os import PathLike
from pathlib import Path
from typing import Literal, Any
from pandas import DataFrame, ExcelWriter

from app.core import Consulta


class ExportaçãoXLSX :
    NOME_XLSX = 'Database'

    def __init__(self, consulta: Consulta, path: Path | PathLike) -> None :
        self._consulta = consulta
        self._gerar_xlsx(path)

    def _gerar_xlsx(self, path: Path) -> None :
        _path = Path(path, f'{self.NOME_XLSX}.xlsx')
        with ExcelWriter(path=_path, engine='xlsxwriter', date_format='DD/MM/YYYY') as writer :
            self._gerar_planilha(writer, self._df_ativa, 'Base Ativa')
            self._gerar_planilha(writer, self._df_bruta, 'Base Bruta')
            self._gerar_planilha(writer, self._df_transferidos, 'Transferidos')

    def _gerar_planilha(self, writer: ExcelWriter, df: DataFrame, nome_planilha: str) :
        df.to_excel(writer, sheet_name=nome_planilha, index=False)
        pasta_de_trabalho = writer.book
        planilha = writer.sheets[nome_planilha]

        formatos = self._formatos(pasta_de_trabalho)
        formato_fonte = formatos['fonte']
        formato_cabeçalho = formatos['cabeçalho']

        planilha.set_column(0, df.shape[1] - 1, None, formato_fonte)

        for col_num, valor in enumerate(df.columns.values) :
            planilha.write(0, col_num, valor, formato_cabeçalho)

        self._gerar_tabela(df, pasta_de_trabalho, planilha, nome_planilha)

    @staticmethod
    def _gerar_tabela(df, pasta, planilha, nome) -> None :
        linhas = df.shape[0]
        colunas = df.shape[1]

        # Configurar a tabela
        planilha.add_table(0, 0, linhas, colunas - 1, {
            'name' : nome.replace(' ', '_'), 'columns' : [{'header' : col} for col in df.columns],
            'style' : 'Table Style Medium 2', 'autofilter' : True
        })
        planilha.hide_gridlines(2)

    def _formatos(self, pasta_) -> dict[str, Any] :
        formato_fonte = pasta_.add_format({
            "font_name" : "Times New Roman", "font_size" : 12
        })

        formato_cabeçalho = pasta_.add_format({
            "font_name" : "Times New Roman", "font_size" : 12, "bold" : True, "bg_color" : "#D3D3D3", "border" : 1
        })

        return {
            'fonte' : formato_fonte, 'cabeçalho' : formato_cabeçalho
        }

    @property
    def _df_ativa(self) -> DataFrame :
        return self._consulta[self._consulta['Situação'] == 'Cursando'].copy()

    @property
    def _df_bruta(self) -> DataFrame :
        return self._consulta.copy()

    @property
    def _df_transferidos(self) -> DataFrame :
        return self._consulta[self._consulta['Situação'] == '(transferido)'].copy()
