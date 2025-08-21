import os
from typing import Literal

from App.backend.query.workflow.variáveis import Variáveis
from pandas import DataFrame, ExcelWriter

#todo: Adicionar método para definir path de output pela UI
#todo: adicionar método para salvar os paths selecionados

class ExportaçãoXLSX:
    def __init__(self, consulta, path):
        self.consulta = consulta
        self.path = path
        self._exportar_xlsx()

    def _exportar_xlsx(self):
        with ExcelWriter(
                path=os.path.join(self.path, 'Database.xlsx'),
                engine='xlsxwriter',
                date_format='DD/MM/YYYY'
        ) as self.writer:
            self._planilhar(nome='Base Ativa', situação='Cursando')
            self._planilhar(nome='Base Bruta')
            self._planilhar(nome='Transferidos', situação='(transferido)')


    def _planilhar(self, nome: str, situação: Literal['Cursando', '(transferido)'] | None = None):
        df = DataFrame()

        if situação is None:
            df: DataFrame = self.consulta
            # df_integrado = df_integrado.reset_index(drop=True)
            # df_integrado.index = df_integrado.index + 1
            df.to_excel(self.writer, sheet_name=nome)

        elif situação == 'Cursando':
            df: DataFrame = self.consulta[self.consulta['Situação'] == 'Cursando']
            df: DataFrame = df[~df['Matrícula'].isin(Variáveis().fantasmas)]
#             df_integrado = df_integrado.reset_index(drop=True)
#             df_integrado.index = df_integrado.index + 1
            df.to_excel(self.writer, sheet_name=nome)

        elif situação == '(transferido)':
            df: DataFrame = self.consulta[self.consulta['Situação'] == '(transferido)']
#             df_integrado = df_integrado.reset_index(drop=True)
#             df_integrado.index = df_integrado.index + 1
            df.to_excel(self.writer, sheet_name=nome)


        self._formatar_planilha(df=df, nome_planilha=nome)

    def _formatar_planilha(self, df, nome_planilha):
        # TODO: Organizar e modular essa merda aqui

        fonte_dict = {
            "font_name": "Times New Roman",
            "font_size": 12
        }
        formato_tabela = {
            'name': nome_planilha.replace(' ', '_'),
            'columns': [{'header': 'Índice'}] + [{'header': col} for col in self.consulta.columns],
            'style': 'Table Style Medium 2',
            'autofilter': True
        }

        pasta_de_trabalho = self.writer.book
        planilha = self.writer.sheets[nome_planilha]

        fonte_geral = pasta_de_trabalho.add_format(fonte_dict)
        sem_borda = pasta_de_trabalho.add_format({'border': 0})

        planilha.set_column(0, df.shape[1], None, fonte_geral)
        planilha.set_row(0, None, sem_borda)

        linhas = df.shape[0]
        colunas = df.shape[1] + 1
        planilha.add_table(0, 0, linhas, colunas - 1, formato_tabela)
        planilha.hide_gridlines(2)

        for linha in range(1, linhas, + 1):
            planilha.write(linha, 0, df.index[linha - 1], sem_borda)

    def _localizar_coluna(self, coluna: str):
        i = self.consulta.columns.get_loc(coluna) + 1
        return i
