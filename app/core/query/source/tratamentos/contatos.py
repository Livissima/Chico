import re
from pandas import DataFrame, Series
import pandas as pd

from app.config.tipos.telefone import Telefone
from app.core.query.workflow.formatação import Formatação


class TratamentoContatos:
    _colunas_finais: list[str] = [
        'Matrícula', 'Telefone 1', 'Telefone 2', 'Telefone 3', 'Educacional'
    ]
    _map_colunas: dict[str, str] = {
            'Telefone residencial' : 'Telefone 1', 'Telefone responsável' : 'Telefone 2',
            'Telefone celular' : 'Telefone 3', 'E-mail Educacional' : 'Educacional',
            'E-mail Alternativo' : 'Email alternativo'
        }
    _colunas_telefone: list[str] = [
        'Telefone 1', 'Telefone 2', 'Telefone 3'
    ]

    def __init__(self, leitura: list[dict[str, str]]) -> None:
        self._df = DataFrame(leitura)
        self.df_tratado = self._tratar(self._df)
        # print(f'{self.df_tratado}')

    def _tratar(self, leitura: DataFrame) -> Series:
        estrutura_base = self._estruturar_df_base(leitura)
        df_tipado = self._tipar_com_telefone(estrutura_base)
        df = self._aplicar_funções_telefones(df_tipado)
        return df

    def _estruturar_df_base(self, leitura: DataFrame) -> DataFrame:
        df_base = leitura.rename(columns=self._map_colunas)
        df_base = df_base.drop_duplicates()
        df_base = df_base[1:]
        df_base = df_base[self._colunas_finais]
        return df_base

    def _tipar_com_telefone(self, df: DataFrame) -> DataFrame :
        for coluna in self._colunas_telefone :
            df[coluna] = df[coluna].apply(lambda x : Telefone(x).valor)
        return df

    def _aplicar_funções_telefones(self, df_limpo: DataFrame) -> Series :
        df = df_limpo
        df = df.apply(self._remover_telefones_duplicados, axis=1)
        df = df.apply(self._ordenar_por_coluna, axis=1)  # Ordenação por prioridade
        return df

    def _remover_telefones_duplicados(self, linha):
        telephones = list(linha.loc[self._colunas_telefone])
        unique_telephones = list(dict.fromkeys(filter(pd.notna, telephones)))
        for i in range(3):
            linha[f'Telefone {i + 1}'] = unique_telephones[i] if i < len(unique_telephones) else '-'
        return linha

    def _ordenar_por_coluna(self, linha) :
        colunas_telefone = self._colunas_telefone

        telefones_info = []
        for i, coluna in enumerate(colunas_telefone) :
            valor = linha.get(coluna)

            if pd.isna(valor) or valor == '' :
                # Vazio: prioridade baixa
                prioridade = (1, 2, i)  # (não_preenchido, tipo_prioridade, ordem_original)
            else :
                instância_telefone = Telefone(valor)
                tipo_prioridade = 0 if instância_telefone.tipo == 'Móvel' else 1 if instância_telefone.tipo == 'Fixo' else 2
                prioridade = (0, tipo_prioridade, i)  # (preenchido, tipo_prioridade, ordem_original)

            telefones_info.append((prioridade, valor))

        # Ordenar e extrair valores
        telefones_ordenados = [valor for _, valor in sorted(telefones_info, key=lambda x : x[0])]

        # Atualizar linha
        for i, coluna in enumerate(colunas_telefone) :
            linha[coluna] = telefones_ordenados[i]

        return linha

    # def __getattr__(self, item):
    #     return getattr(self.df_tratado, item)
