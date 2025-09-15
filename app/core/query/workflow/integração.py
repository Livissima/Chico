import pandas as pd
from pandas import DataFrame, Series

from .extra import *
from .extra.acessos import Acessos


class Integração:
    #todo: Importar a responsabilidade de chamada de filtrar excls. Assim, a classe vai resultar em
    # dataframes que serão transferidos para a exportação

    def __init__(self, dfs_tratados: dict[str, DataFrame]):
        self.df = dfs_tratados
        self.path_df_social: str = r'C:\Users\meren\OneDrive - Secretaria de Estado da Educação\Secretaria\2025\Dados\Estudantes\Base de dados\Etnia e religião.xlsx'  #temporário. Preciso que esta variável seja mais flexível e adiquirida dinamicamente.
        self.integração = self.integrar(dfs_tratados)

    def integrar(self, dict_dfs):
        df_base = DataFrame()
        df_base = self._integrar_tratamentos(dict_dfs)

        df_base['Irmão 1']   = self._integrar_irmão(df_base)
        df_base['Idade']     = self._integrar_idade(df_base)
        df_base['Senha padrão'] = self._integrar_senha_padrão(df_base)
        df_base['Nova senha'] = self._integrar_nova_senha(df_base)

        try:
            df_base = self._integrar_sociais(df_base, self.path_df_social)
        except FileNotFoundError as exception:
            print(f'Séries não puderam ser carregadas: {exception}')

        finally:
            return df_base


    @staticmethod
    def _integrar_senha_padrão(df_base: DataFrame) -> Series:
        acessos = Acessos()
        return df_base.apply(acessos.extrair_senha_padrão, axis=1)

    @staticmethod
    def _integrar_nova_senha(df_base: DataFrame) -> Series:
        acessos = Acessos()
        return df_base.apply(acessos.gerar_nova_senha, axis=1)

    @staticmethod
    def _integrar_tratamentos(df: dict[str, DataFrame]) -> DataFrame:
        fichas = df['fichas'].df_tratado
        contatos = df['contatos'].df_tratado
        situações = df['situações'].df_tratado
        gêneros = df['gêneros'].df_tratado

        for df_tratado in (fichas, contatos, situações, gêneros):
            df_tratado['Matrícula'] = df_tratado['Matrícula'].astype(str).str.strip()

        eixo = 'Matrícula'

        df_tratamentos_integrados = (fichas.merge(contatos, on=eixo, how='left'
                                                  ).merge(gêneros, on=eixo, how='left'
                                                          ).merge(situações, on=eixo, how='left'))

        return df_tratamentos_integrados

    @staticmethod
    def _integrar_irmão(df_base: DataFrame) -> Series:
        irmão = Irmão.localizar_irmãos(df_base)
        return Series(data=irmão)

    @staticmethod
    def _integrar_idade(df_base: DataFrame):
        df_base['Data de Nascimento'] = pd.to_datetime(df_base['Data de Nascimento'], format='%d/%m/%Y')
        _idade = Idade.calcular_idade(df_base['Data de Nascimento'])
        return _idade


    @staticmethod
    def _integrar_sociais(df_base: DataFrame, path_df_social: str) -> DataFrame:
        df_social = Social(path_df_social).df_social

        for df in [df_base, df_social]:
            df['Matrícula'] = df['Matrícula'].astype(str).str.strip()
            df['Matrícula'] = df['Matrícula'].replace('-', '', regex=True)

        df_mergido_com_sociais = df_base.merge(df_social, on=['Matrícula'], how='left')
        return df_mergido_com_sociais

    # def __getattr__(self, item):
    #     return getattr(self.integração, item)

    def __getitem__(self, item):
        return self.df[item]
