import re
from pandas import DataFrame, Series
import pandas as pd
from typing import Optional

from app.config.tipos.telefone import Telefone
from app.core.query.workflow.formatação import Formatação


class TratamentoContatos :
    def __init__(self, leitura: list[dict[str, str]]) -> None :
        self.df = DataFrame(leitura)
        self.df_tratado = self.tratar(self.df)

    def tratar(self, leitura: DataFrame) -> DataFrame :
        # Verificação defensiva
        if leitura is None or leitura.empty :
            return self._criar_dataframe_vazio()

        df_base = self._definir_df_base(leitura)

        # Verifica se df_base é válido
        if df_base is None or df_base.empty :
            return self._criar_dataframe_vazio()

        df_limpo = self._limpar_e_criar_telefones(df_base)
        df = self._aplicar_funções_telefones(df_limpo)
        return df

    def _criar_dataframe_vazio(self) -> DataFrame :
        """Cria um DataFrame vazio com a estrutura esperada"""
        return DataFrame(columns=self._colunas)

    def _definir_df_base(self, leitura: DataFrame) -> Optional[DataFrame] :
        """Define o DataFrame base com verificações de segurança"""
        try :
            df_base: DataFrame = Formatação.renomear_colunas(leitura, self._map_colunas)
            df_base = Formatação.remover_quebras_de_linhas(df_base)
            df_base = df_base.loc[:, ~df_base.columns.duplicated()]
            df_base = df_base.drop_duplicates()

            # Verifica se há dados suficientes antes de fatiar
            if len(df_base) > 1 :
                df_base = df_base[1 :]
            else :
                # Se não há dados suficientes, retorna DataFrame vazio mas com colunas
                return self._criar_dataframe_vazio()

            # Garante que as colunas existem
            colunas_faltantes = [col for col in self._colunas if col not in df_base.columns]
            for col in colunas_faltantes :
                df_base[col] = pd.NA

            df_base = df_base[self._colunas]
            return df_base

        except Exception as e :
            print(f"Erro em _definir_df_base: {e}")
            return self._criar_dataframe_vazio()

    def _limpar_e_criar_telefones(self, df_base: DataFrame) -> DataFrame :
        """Substitui strings por objetos Telefone com verificação de segurança"""
        # Verificação defensiva
        if df_base is None :
            return self._criar_dataframe_vazio()

        try :
            df = df_base.copy()

            for coluna in self._colunas_telefone :
                if coluna in df.columns :
                    df[coluna] = df[coluna].apply(
                        lambda x : Telefone(x) if pd.notna(x) and str(x).strip() else Telefone(None))

            return df
        except Exception as e :
            print(f"Erro em _limpar_e_criar_telefones: {e}")
            return df_base.copy() if df_base is not None else self._criar_dataframe_vazio()

    def _aplicar_funções_telefones(self, df_pré_tratado: DataFrame) -> DataFrame :
        """Aplica funções de tratamento com verificação de segurança"""
        if df_pré_tratado is None or df_pré_tratado.empty :
            return self._criar_dataframe_vazio()

        try :
            df = df_pré_tratado
            df = df.apply(self._remover_telefones_duplicados, axis=1)
            df = df.apply(self._ordenar_por_coluna, axis=1)
            return df
        except Exception as e :
            print(f"Erro em _aplicar_funções_telefones: {e}")
            return df_pré_tratado

    def _remover_telefones_duplicados(self, linha) :
        try :
            # Extrai os valores dos objetos Telefone
            telefones = []
            for col in self._colunas_telefone :
                if col in linha :
                    tel_obj = linha[col]
                    if isinstance(tel_obj, Telefone) and tel_obj.é_valido :
                        telefones.append(tel_obj.valor)
                    elif pd.notna(tel_obj) and str(tel_obj).strip() :
                        telefones.append(str(tel_obj))

            # Remove duplicados mantendo a ordem
            unique_telefones = list(dict.fromkeys(filter(None, telefones)))

            # Atualiza a linha com os telefones únicos
            for i in range(3) :
                col_name = f'Telefone {i + 1}'
                if i < len(unique_telefones) :
                    linha[col_name] = Telefone(unique_telefones[i])
                else :
                    linha[col_name] = Telefone(None)

            return linha
        except Exception as e :
            print(f"Erro em _remover_telefones_duplicados: {e}")
            return linha

    def _ordenar_por_coluna(self, linha) :
        try :
            colunas_telefone = self._colunas_telefone
            telefones = []

            for coluna in colunas_telefone :
                if coluna in linha :
                    valor = linha.get(coluna)
                    if isinstance(valor, Telefone) :
                        telefones.append(valor.valor if valor.é_valido else '')
                    elif pd.isna(valor) or valor == '' :
                        telefones.append('')
                    else :
                        telefones.append(str(valor))
                else :
                    telefones.append('')

            sorted_telefones = sorted(telefones, key=lambda x : (x == '', x))

            for i, coluna in enumerate(colunas_telefone) :
                linha[coluna] = Telefone(sorted_telefones[i])

            return linha
        except Exception as e :
            print(f"Erro em _ordenar_por_coluna: {e}")
            return linha

    @property
    def _colunas_telefone(self) -> list[str] :
        return ['Telefone 1', 'Telefone 2', 'Telefone 3']

    @property
    def _colunas(self) -> list[str] :
        return ['Matrícula', 'Telefone 1', 'Telefone 2', 'Telefone 3', 'Educacional']

    @property
    def _map_colunas(self) -> dict[str, str] :
        return {
            'Telefone residencial' : 'Telefone 1', 'Telefone responsável' : 'Telefone 2',
            'Telefone celular' : 'Telefone 3', 'E-mail Educacional' : 'Educacional',
            'E-mail Alternativo' : 'Email alternativo'
        }

    def __getattr__(self, item) :
        return getattr(self.df_tratado, item)