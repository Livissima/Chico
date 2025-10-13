import sys
from pandas import DataFrame
from selenium.common import NoSuchElementException
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

from app.auto.functions.navegaçãoweb import NavegaçãoWeb
from app.auto.data.sites.propriedades import Propriedades
from typing import Literal
import pandas as pd
import unicodedata

class CredenciadorNetescola:

    def __init__(
            self,
            navegador,
            path_database: str,
            tipo: Literal['netescola', 'google'],
            turmas: list[str] = None,
            **kwargs
    ):
        print(f'class GerenciadorDeCredenciais instanciada.')

        self.master = navegador
        self.nv = NavegaçãoWeb(navegador, tipo)
        self.pp = Propriedades(site=tipo)
        self.turmas = turmas
        print(f'{self.turmas = }')

        self.df = self.dataframe(path_database)
        self.gerenciar(tipo)
        # self.master.quit()


    def gerenciar(self, matrícula, dn, email, nova_senha):

        self.nv.digitar_xpath('matrícula', string=matrícula)
        self.nv.digitar_xpath('nascimento', string=dn)
        self.nv.clicar('xpath', 'pesquisar')
        self.nv.digitar_xpath('email', string=email)
        self.nv.digitar_xpath('email2', string=email)
        self.nv.digitar_xpath('senha', string=nova_senha)
        self.nv.digitar_xpath('senha2', string=nova_senha)
        self.nv.clicar('xpath', 'concordo')
        self.nv.clicar('xpath', 'salvar')
        self.nv.aguardar_página()

        self.master.refresh()
        self.nv.aguardar_página()



    def dataframe(self, path):
        _df = pd.read_excel(path, 'Base Ativa')
        colunas = ['Turma', 'Matrícula', 'Educacional', 'Estudante', 'Data de Nascimento', 'Senha padrão', 'Nova senha']
        df: DataFrame = _df[colunas].copy()

        df['Turma'] = df['Turma'].astype(str).str.strip()

        df['Estudante'] = df['Estudante'].astype(str).str.normalize('NFKD').str.encode('ASCII', errors='ignore').str.decode('ASCII').str.strip()

        print(f'{df['Turma'].unique().tolist() = }')
        print(df.head())
        df = df[df['Turma'].isin(self.turmas)]

        return df

    @staticmethod
    def anunciar(ind, aluno: str, _turma: str, texto: str):
        sys.stdout.write(f'\r {ind} {aluno} - {_turma}: {texto}.')
        sys.stdout.flush()
