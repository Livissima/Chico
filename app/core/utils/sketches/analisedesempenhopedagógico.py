import os

import pandas as pd
from pathlib import Path

from pandas import DataFrame

class AnáliseDesempenho:
    path_caed_2026_1 = Path(r'C:\Users\meren\OneDrive - Secretaria de Estado da Educação\Pedagógico\CAED 2026-1')

    def __init__(self):
        self.export()

    def export(self):
        dfs_estudante = self._elaborar_df('estudante')
        dfs_escola = self._elaborar_df('escola')
        dfs_turma = self._elaborar_df('turma')
        dfs_série = self._elaborar_df('série')

        path = Path(self.path_caed_2026_1, 'Desempenho CAED 2026.xlsx')

        with pd.ExcelWriter(path, 'xlsxwriter') as writer:
            dfs_estudante['MT'].to_excel(writer, 'Estudante - MT')
            dfs_estudante['PT'].to_excel(writer, 'Estudante - PT')
            dfs_escola['MT'].to_excel(writer, 'Escola - MT')
            dfs_escola['PT'].to_excel(writer, 'Escola - PT')
            dfs_turma['MT'].to_excel(writer, 'Turma - MT')
            dfs_turma['PT'].to_excel(writer, 'Turma - PT')
            dfs_série['MT'].to_excel(writer, 'Série - MT')
            dfs_série['PT'].to_excel(writer, 'Série - PT')

    def _elaborar_df(self, alvo: str) -> dict[str, DataFrame] :
        pasta = self._sub_pasta(alvo)
        arquivos = [Path(pasta, arquivo) for arquivo in os.listdir(pasta)]

        lista_mt = []
        lista_pt = []

        for arquivo in arquivos :
            # Tente ler com detecção de separador
            try :
                df_temp = pd.read_csv(arquivo, sep=None, engine='python', encoding='utf-8')
            except UnicodeDecodeError :
                df_temp = pd.read_csv(arquivo, sep=None, engine='python', encoding='latin-1')

            if self._disc(arquivo) == 'MT' :
                lista_mt.append(df_temp)
            elif self._disc(arquivo) == 'PT' :
                lista_pt.append(df_temp)

        # Concatena tudo de uma vez no final
        return {
            'MT' : pd.concat(lista_mt, ignore_index=True) if lista_mt else DataFrame(),
            'PT' : pd.concat(lista_pt, ignore_index=True) if lista_pt else DataFrame()
        }



    @staticmethod
    def _disc(nome: Path):
        return str(nome.name).split('.')[0].split()[1]

    def _sub_pasta(self, alvo: str) -> Path:
        return Path(self.path_caed_2026_1, str(alvo).title())

AnáliseDesempenho()
