from typing import Iterable, Generator

from pandas import DataFrame, Series
import pandas as pd

from app.config.classes.telefone import Telefone


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

    def __init__(self, fluxo_leitura: Iterable[str]) -> None:
        self.fluxo = self.processar_pipeline(fluxo_leitura)

    def _processar_pipeline(self, fluxo: Iterable[dict]) -> Generator:
        vistos = set()

        for item in fluxo:
            token = item.get('Matrícula')
            if token in vistos:
                continue
            vistos.add(token)

            telefones = self._limpar_e_ordenar_telefones(item)

            yield {
                'Matrícula' : item.get('Matrícula'),
                **telefones,
                'Educacional' : item.get('E-mail educacional')
            }


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
        df = df_limpo.apply(self._processar_linha_telefones, axis=1)
        return df

    def _processar_linha_telefones(self, linha) :
        # 1. Extração e Normalização imediata para comparação
        telefones_brutos = []
        for col in self._colunas_telefone :
            valor = linha[col]
            # Converte para string e limpa. Se for NaN, vira string vazia.
            val_str = str(valor).strip() if pd.notna(valor) else ""
            telefones_brutos.append(val_str)

        # 2. Unicidade (Onde a mágica acontece)
        # Filtramos strings vazias e duplicatas de uma vez
        telefones_unicos = []
        for t in telefones_brutos :
            if t != "" and t not in telefones_unicos :
                telefones_unicos.append(t)

        # 3. Ordenação
        def definir_prioridade(valor_tel) :
            instancia = Telefone(valor_tel)
            if instancia.tipo == 'Móvel' : return 0
            if instancia.tipo == 'Fixo' : return 1
            return 2

        telefones_ordenados = sorted(telefones_unicos, key=definir_prioridade)

        # 4. Escrita Limpa
        for i, coluna in enumerate(self._colunas_telefone) :
            if i < len(telefones_ordenados) :
                linha[coluna] = telefones_ordenados[i]
            else :
                linha[coluna] = ""

        return linha

    # def __getattr__(self, item):
    #     return getattr(self.df_tratado, item)
