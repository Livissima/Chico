import re
from pandas import DataFrame
import pandas as pd
from app.backend.query.workflow.formatação import Formatação


class TratamentoContatos:
    #Parâmetros
    colunas_para_dropar = [
        'Aluno', 'Data de Nascimento', 'Nome da Mãe', 'CPF do Responsável', 'Nome do Responsável', 'E-mail Institucional',
        'Ponto ID', 'Email alternativo']
    column_mapping = {
        'Telefone\rresidencial' : 'Telefone 1',
        'Telefone\rresponsável' : 'Telefone 2',
        'Telefone\rcelular'     : 'Telefone 3',
        'Telefone celular'      : 'Telefone 3',
        'E-mail Educacional'   : 'Educacional',
        'E-mail Alternativo'   : 'Email alternativo'
    }
    telefones = [
        'Telefone 1', 'Telefone 2', 'Telefone 3']

    def __init__(self, leitura: DataFrame):

        self.df = leitura
        self.df_tratado = self.tratar(leitura)

        # print(f'TratamentoContatos.df: {leitura.shape}. Colunas: {list(leitura.columns)}')
        # print(f'TratamentoContatos.df_tratado: {self.df_tratado.shape}. Colunas: {list(self.df_tratado.columns)}\n')


    def tratar(self, leitura):
        df_base = self._definir_df_base(leitura)
        # self._definir_df_base()
        # self._dropar_colunas()

        df_limpo = self._limpar_strings_telefones(df_base)
        df = self._aplicar_funções_telefones(df_limpo)

        # self.df.to_excel(r'Tratamentos\contatos.xlsx')
        return df


    def _definir_df_base(self, leitura):
        df_base = Formatação.renomear_colunas(leitura, self.column_mapping)
        df_base = Formatação.remover_quebras_de_linhas(df_base)
        df_base = df_base.loc[:, ~df_base.columns.duplicated()]
        # df_base = self.fm.renomear_colunas(df_integrado=df_base, dicionário=self.column_mapping)
        df_base = df_base.drop(columns=self.colunas_para_dropar)
        return df_base

    # def _dropar_colunas(self):


    def _limpar_strings_telefones(self, df_base):
        def clean_phone_number(x) :
            return re.sub('[^0-9]+', '', str(x)) if isinstance(x, str) else x

        df = df_base
        df[self.telefones] = df[self.telefones].applymap(clean_phone_number)
        # self.df_integrado['Matrícula'].replace(to_replace='-', value='', regex=True, inplace=True)
        return df


    def _aplicar_funções_telefones(self, df_limpo):
        df = df_limpo
        df = df.apply(self._remover_telefones_duplicados, axis=1)
        df = df.apply(self._ordenar_telefones, axis=1)
        for col in self.telefones:
            df[col] = df[col].apply(self._ajustar_telefones)
        return df


    @staticmethod
    def _remover_telefones_duplicados(row):
        telephones = list(row.loc[['Telefone 1', 'Telefone 2', 'Telefone 3']])
        # Remove duplicates by converting to a set and back to a list
        unique_telephones = list(dict.fromkeys(filter(pd.notna, telephones)))
        # Fill the original columns with unique values and NaN for the rest
        for i in range(3):
            row[f'Telefone {i + 1}'] = (
                unique_telephones)[i] if i < len(unique_telephones) \
                else pd.NA
        return row

    @staticmethod
    def _ordenar_telefones(row):
        colunas_telefone = ['Telefone 1', 'Telefone 2', 'Telefone 3']
        telefones = []
        for coluna in colunas_telefone:
            valor = row.get(coluna)
            if pd.isna(valor) or valor == '':
                telefones.append('')
            else:
                telefones.append(valor)

        # numéricos (não vazios) primeiro, depois vazios:
        sorted_telefones = sorted(telefones, key=lambda x: (x == '', x))

        # reatribui em cada coluna pelo índice correto
        for i, coluna in enumerate(colunas_telefone):
            row[coluna] = sorted_telefones[i]

        return row


    @staticmethod
    def _ajustar_telefones(telefone):
        """
        Função para ajustar ao formato de telefone xx xxxxx xxxx
        """
        if pd.isna(telefone) or telefone == '':
            return telefone  # Retorna vazio se o telefone for NaN ou vazio

        telefone = str(telefone).strip()  # Remove espaços em branco

        if len(telefone) == 10:  # Telefone fixo
            ddd = telefone[:2]
            numero = telefone[2:]
            if numero[0] in '6789':
                return f"{ddd}9{numero}"
            else:
                return telefone  # Retorna o telefone fixo como está

        elif len(telefone) == 11:  # Telefone móvel
            ddd = telefone[:2]
            numero = telefone[2:]
            if numero[0] == '9':
                return telefone
            elif numero[0] in '6789':
                return telefone
            else:
                return f"{ddd}9{numero}"  # Adiciona '9' se necessário

        return telefone

    def __getattr__(self, item):
        return getattr(self.df_tratado, item)