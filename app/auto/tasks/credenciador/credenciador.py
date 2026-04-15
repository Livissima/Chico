import sys
from pandas import DataFrame
from selenium.common import NoSuchElementException
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

from app.auto.tasks.registrotasks import RegistroTasks
from app.auto.functions.navegaçãoweb import NavegaçãoWeb
from app.auto.data.sites.propriedadesweb import PropriedadesWeb
from typing import Literal
import pandas as pd
import unicodedata


@RegistroTasks.registrar('credenciar')
class Credenciador:

    def __init__(self, navegador, path_database: str, turmas: list[str] = None, **kwargs) :
        print(f'class {__class__.__name__} instanciada.\n'
              f'    •{self = }\n'
              f'    •{path_database = }\n'
              # f'    •{tipo = }\n'
              f'    •{turmas = }\n'
              f'    •{kwargs = }\n'
              )

        self.master = navegador
        self.nv = NavegaçãoWeb(navegador, 'netescola')
        self.pp = PropriedadesWeb(site='netescola')
        self.turmas = turmas
        self._path_database = path_database
        print(f'{self.turmas = }')
        self._logon()
        self._gerenciar_selecionados()
        # self.df = self._dataframe(path_database)
        # self.master.quit()

    def _gerenciar_selecionados(self):
        início = 0

        for índice, linha in self._dataframe().iloc[início:].iterrows():
            estudante     = str(linha['Estudante'])
            turma         = str(linha['Turma'])
            matrícula     = str(linha['Matrícula'])
            email         = str(linha['Educacional'])
            dn            = str(linha['Data de Nascimento']).replace('/', '')
            nova_senha    = str(linha['Nova senha'])
            senha_padrão  = str(linha['Senha padrão'])
            senha_padrão2 = str(f'go2025{linha['Estudante'].lower().split()[0]}')

            # print(estudante, turma, matrícula, email, dn, nova_senha, senha_padrão, senha_padrão2)

            self.anunciar(índice, estudante, turma, 'Processando...')

            self._gerenciar_indivíduo(matrícula, dn, email, nova_senha)

            self.anunciar(índice, estudante, turma, 'Ok.', ok=True)



    def _gerenciar_indivíduo(self, matrícula, dn, email, nova_senha):

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



    def _dataframe(self) -> DataFrame:
        _df             = pd.read_excel(self._path_database, 'Base Ativa')
        colunas         = ['Turma', 'Matrícula', 'Educacional', 'Estudante', 'Data de Nascimento', 'Senha padrão', 'Nova senha']
        df: DataFrame   = _df[colunas].copy()
        df['Turma']     = df['Turma'].astype(str).str.strip()
        df['Estudante'] = df['Estudante'].astype(str).str.normalize('NFKD').str.encode('ASCII', errors='ignore').str.decode('ASCII').str.strip()

        df = df[df['Turma'].isin(self.turmas)]

        print(f'{df['Turma'].unique().tolist() = }')
        print(df.head())

        return df

    @staticmethod
    def anunciar(ind, aluno: str, _turma: str, texto: str, ok=False):

        sys.stdout.write(f'\r {ind} - {aluno} - {_turma}: {texto}.')
        if ok:
            sys.stdout.write('\n')
        sys.stdout.flush()

    def _logon(self) -> None:
        self.master.get(self.pp.urls)
        self.master.maximize_window()
