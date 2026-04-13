import os
from pathlib import Path

import pandas as pd
from pandas import DataFrame

from app.config.parâmetros import parâmetros


class CompiladorDeFaltas :
    _NOME_PASTA_REGISTROS = 'Registro de Faltas'
    _NOME_CSV_EXPORTADO = 'Compilado de Faltas'
    _FORMATOS_SUPORTADOS_PARA_LEITURA = ['xlsx', 'xlsm'] 

    def __init__(self, diretório_base: Path) :
        print(f'\n::::::: Compilando faltas :::::::\n')

        self._path = Path(diretório_base, 'fonte', 'Controle de Frequência')
        self._compilado_de_faltas = self._compilar_faltas()

    def exportar(self) :
        destino = Path(self._path, f'{self._NOME_CSV_EXPORTADO}.csv')
        self._compilado_de_faltas.to_csv(destino, index=False)

    def _compilar_faltas(self) :
        dfs_iniciais = self._obter_lista_inicial_de_dataframes()
        compilado = self._gerar_dataframe(dfs_iniciais)
        return compilado

    def _obter_lista_inicial_de_dataframes(self) -> list[DataFrame] :
        lista_df_inicial = []

        for diretório_arquivo in self._paths_de_registros_de_faltas :
            if diretório_arquivo.suffix not in ["."+formato for formato in self._FORMATOS_SUPORTADOS_PARA_LEITURA]:
                continue

            abas_lidas = self._ler_pasta_de_trabalho(diretório_arquivo)
            lista_df_inicial.extend(abas_lidas)

        return lista_df_inicial

    @staticmethod
    def _gerar_dataframe(_lista_dfs: list[DataFrame]) -> DataFrame | None:
        colunas = ['Turma', 'Estudante', 'Data', 'Lançado', 'Matrícula']
        df_geral = pd.DataFrame()
        lista_dataframes_processados = []

        if _lista_dfs is None:
            print(f'  ->  Dicionário vazio na compilação de faltas.')
            return None

        for df_bruto in _lista_dfs:
            df_processado = df_bruto[colunas].copy()
            df_processado = df_processado.dropna(subset=colunas)
            df_processado['Matrícula'] = df_processado['Matrícula'].astype(float).astype(int).astype(str)
            df_processado['Lançado'] = df_processado['Lançado'].fillna('')

            df_processado['Data'] = pd.to_datetime(df_processado['Data'], errors='coerce').dt.strftime('%d/%m/%Y')
            lista_dataframes_processados.append(df_processado)

        df_geral = pd.concat(lista_dataframes_processados, ignore_index=True)
        print(df_geral)
        return df_geral


    @staticmethod
    def _ler_pasta_de_trabalho(path_arquivo: Path) -> list[DataFrame] :
        try :
            dicio_abas = pd.read_excel(path_arquivo, sheet_name=parâmetros.turmas_disponíveis, engine='openpyxl')

            return [df.assign(Turma=nome) for nome, df in dicio_abas.items() if not df.empty]

        except Exception as e :
            print(f'Erro ao processar {path_arquivo.name}: {e}')
            return []

    @property
    def _paths_de_registros_de_faltas(self) -> list[Path] :
        path_pasta_registro_de_faltas = Path(self._path, self._NOME_PASTA_REGISTROS)
        lista_itens = os.listdir(path_pasta_registro_de_faltas)
        lista_diretórios = [Path(path_pasta_registro_de_faltas, item) for item in lista_itens]
        return lista_diretórios
