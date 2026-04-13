import os
from pathlib import Path

import pandas as pd
from pandas import DataFrame

from app.config.parâmetros import parâmetros


class CompiladorDeFaltas :
    NOME_PASTA_REGISTROS = 'Registro de Faltas'
    NOME_CSV_DE_FALTAS = 'Compilado de Faltas'

    def __init__(self, diretório_base: Path) :
        print(f'\n::::::: Compilando faltas :::::::\n')

        self._path = Path(diretório_base, 'fonte', 'Controle de Frequência')

        self._compilado_de_faltas = self._compilar_faltas()
        # print(f'{self._compilado_de_faltas}')

    def compilar_e_exportar(self) :
        destino = Path(self._path, f'{self.NOME_CSV_DE_FALTAS}.csv')
        self._compilado_de_faltas.to_csv(destino, index=False)

    def _compilar_faltas(self) :
        dfs_iniciais = self._ler_dfs()
        compilado = self._gerar_dataframe(dfs_iniciais)
        return compilado

    def _ler_dfs(self) -> DataFrame | dict[int | str, DataFrame] | None :
        for diretório_arquivo in self._paths_de_registros_de_faltas :
            if diretório_arquivo.suffix not in ['.xlsx', '.xlsm'] :  # todo: implementar csv no futuro
                continue

            print(f' - Diretório registro: {diretório_arquivo}')

            try :
                dicionário_dataframes = pd.read_excel(
                    diretório_arquivo,
                    sheet_name=parâmetros.turmas_disponíveis,
                    engine='openpyxl'
                )
                print(f'\n - Dataframes lidos e dicionário de dataframes gerado: {dicionário_dataframes.keys() = }')
                for nome_turma, dataframe in dicionário_dataframes.items():
                    print(f'    -> {nome_turma} : {dataframe.shape}')
                # print(dicionário_dataframes)
                return dicionário_dataframes

            except Exception as e:
                raise e

        raise


    @staticmethod
    def _gerar_dataframe(dicio_dfs: dict[int | str, DataFrame] | None) -> DataFrame | None:
        # print(f'{dicio_dfs = }')
        df_geral = pd.DataFrame()
        lista_dfs = []

        if dicio_dfs is None:
            print(f'  ->  Dicionário vazio na compilação de faltas.')
            return None

        for nome_turma, df_turma in dicio_dfs.items() :
            # print(f'\n{nome_turma = } : {df_turma.head(1)}')
            df_turma = df_turma[['Estudante', 'Data', 'Lançado', 'Matrícula']].copy()
            df_turma = df_turma.dropna(axis=0)
            df_turma['Turma'] = nome_turma
            df_turma['Matrícula'] = df_turma['Matrícula'].astype(int).astype(str)
            df_turma['Lançado'] = df_turma['Lançado'].fillna('')
            print(df_turma.head(1))
            # df_turma = df_turma.dropna(axis=0, subset='Estudante')
            # df_turma['Data'] = df_turma['Data'].dt.strftime('%d/%m/%Y')
            lista_dfs.append(df_turma)
            # print(f'{lista_dfs = }')

        # df_geral = df_geral._append_internal(lista_dfs)
        # print(df_geral)
        return df_geral

    @property
    def _paths_de_registros_de_faltas(self) -> list[Path] :
        path_pasta_registro_de_faltas = Path(self._path, self.NOME_PASTA_REGISTROS)
        lista_itens = os.listdir(path_pasta_registro_de_faltas)
        lista_diretórios = [Path(path_pasta_registro_de_faltas, item) for item in lista_itens]
        return lista_diretórios


if __name__ == '__main__' :
    CompiladorDeFaltas(parâmetros.diretório_base).compilar_e_exportar()
