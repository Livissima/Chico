import os
from os import PathLike
from pathlib import Path
from typing import Literal, Any
from pandas import DataFrame, ExcelWriter


#todo: adicionar método para salvar os paths selecionados

class ExportaçãoXLSX:
    NOME_XLSX = 'Database'

    def __init__(self, consulta: DataFrame, path: Path | PathLike) -> None:
        self._consulta = consulta

        self._gerar_xlsx(path)

    def _gerar_xlsx(self, path: Path) -> None:
        _path = Path(path, f'{self.NOME_XLSX}.xlsx')
        with ExcelWriter(path=_path, engine='xlsxwriter',  date_format='DD/MM/YYYY') as writer:
            self._gerar_planilha(writer, self._df_ativa, 'Base Ativa')
            self._gerar_planilha(writer, self._df_bruta, 'Base Bruta')
            self._gerar_planilha(writer, self._df_transferidos, 'Transferidos')


    def _gerar_planilha(self, writer: ExcelWriter, df: DataFrame, nome_planilha: str):
        df.to_excel(writer, sheet_name=nome_planilha)
        pasta_de_trabalho = writer.book
        planilha = writer.sheets[nome_planilha]
        formato_fonte = self._formatos(pasta_de_trabalho)['fonte']
        sem_borda = self._formatos(pasta_de_trabalho)['borderless']
        planilha.set_column(0, df.shape[1], None, formato_fonte)
        planilha.set_row(0, None, sem_borda)

        self._gerar_tabela(df, pasta_de_trabalho, planilha, nome_planilha)


    def _gerar_tabela(self, df, pasta, planilha, nome) -> None:
        formato = self._formatos(pasta)
        linhas = df.shape[0]
        colunas = df.shape[1] + 1
        planilha.add_table(0, 0, linhas, colunas - 1, self._formato_tabela(nome))
        planilha.hide_gridlines(2)

        for linha in range(1, linhas, + 1):
            planilha.write(linha, 0, df.index[linha - 1], formato)


    def _formatos(self, pasta_) -> dict[Literal['fonte', 'borderless'], Any]:
        formato_fonte = pasta_.add_format(self._fontes)
        formato_sem_borda = pasta_.add_format({'border': 0})
        return {'fonte' : formato_fonte, 'borderless' : formato_sem_borda}

    def _formato_tabela(self, nome):
        return {
            'name': nome.replace(' ', '_'),
            'columns': [{'header': 'Índice'}] + [{'header': col} for col in self._consulta.columns],
            'style': 'Table Style Medium 2',
            'autofilter': True
        }


    @property
    def _fontes(self):
        return {
            "font_name": "Times New Roman",
            "font_size": 12
        }

    # def _localizar_coluna(self, coluna: str):
    #     i = self._consulta.columns.get_loc(coluna) + 1
    #     return i

    @property
    def _df_ativa(self) -> DataFrame :
        df = DataFrame()
        df: DataFrame = self._consulta[self._consulta['Situação'] == 'Cursando']
        return df

    @property
    def _df_bruta(self) -> DataFrame :
        df: DataFrame = DataFrame(self._consulta)
        return df

    @property
    def _df_transferidos(self) -> DataFrame :
        df = DataFrame()
        df: DataFrame = self._consulta[self._consulta['Situação'] == '(transferido)']
        return df
