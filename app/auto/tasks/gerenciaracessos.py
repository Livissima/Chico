import sys
from pandas import DataFrame

from selenium.webdriver import Chrome

from app.auto.functions.navegação import Navegação
from app.auto.info.sites.propriedades import Propriedades
from typing import Literal
import pandas as pd


class GerenciarAcessos:

    def __init__(
            self,
            navegador: Chrome,
            path_database: str,
            tipo: Literal['netescola', 'google'],
            turma: list[str] = None,
    ):
        print(f'class NetEscola instanciada.')
        self.master = navegador
        self.nv = Navegação(navegador, tipo)
        self.pp = Propriedades(site=tipo)
        self.path_db = path_database
        self.df = self.dataframe(path_database)

        self.gerenciar(tipo)

    def dataframe(self, path_db):
        _df = pd.read_excel(self.path_db, 'Base Ativa')
        df: DataFrame = _df[
            ['Turma', 'Matrícula', 'Educacional', 'Estudante', 'Data de Nascimento', 'Senha padrão', 'Nova senha']
        ].copy()
        return df

    def gerenciar(self, tipo):
        self.master.get(self.pp.url)
        tipos = {
            'netescola' : self.gerenciar_netescola,
            'google'    : self.gerenciar_google,
        }
        return tipos[tipo]()

    def gerenciar_netescola(self):
        def anunciar(ind, aluno: str, _turma: str, texto: str):
            sys.stdout.write(f'\r {ind} {aluno} - {_turma}: {texto}.')
            sys.stdout.flush()
        início = 15
        for index, row in self.df.iloc[início:].iterrows():
            estudante  = row['Estudante']
            turma      = row['Turma']
            matrícula  = str(row['Matrícula'])
            email      = row['Educacional']
            dn         = str(row['Data de Nascimento']).replace('/', '')
            nova_senha = row['Nova senha']
            # print(f'Iniciado: {estudante}, {turma}, {matrícula}, {email}, {dn}, {nova_senha}')
            anunciar(index, estudante, turma, 'iniciando')

            self.nv.digitar_xpath('matrícula', string=matrícula)
            self.nv.digitar_xpath('nascimento', string=dn)
            self.nv.clicar('xpath', 'pesquisar')

            self.nv.digitar_xpath('email', string=email)
            self.nv.digitar_xpath('email2', string=email)
            self.nv.digitar_xpath('senha', string=nova_senha)
            self.nv.digitar_xpath('senha2', string=nova_senha)
            self.nv.clicar('xpath', 'concordo')
            self.nv.clicar('xpath', 'salvar')
            # sleep(60)
            self.nv.aguardar()
            anunciar(index, estudante, turma, 'concluído.')
            print('\r')
            # self.master.get(self.pm.url)
            self.master.refresh()
            self.nv.aguardar()

    def gerenciar_google(self):
        print('GOOGLE')
        pass
