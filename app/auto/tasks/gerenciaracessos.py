import sys
from pandas import DataFrame
from selenium.webdriver import Chrome
from app.auto.functions.navegação import Navegação
from app.auto.data.sites.propriedades import Propriedades
from typing import Literal
import pandas as pd


class GerenciarAcessos:

    def __init__(
            self,
            navegador: Chrome,
            path_database: str,
            tipo: Literal['netescola', 'google'],
            turmas: list[str] = None,
            **kwargs
    ):
        print(f'class NetEscola instanciada.')
        self.master = navegador
        self.nv = Navegação(navegador, tipo)
        self.pp = Propriedades(site=tipo)
        self.path_db = path_database
        self.turmas = turmas

        self.df = self.dataframe()
        self.gerenciar(tipo)
        self.master.quit()


    def dataframe(self):
        _df = pd.read_excel(self.path_db, 'Base Ativa')
        df: DataFrame = _df[
            ['Turma', 'Matrícula', 'Educacional', 'Estudante', 'Data de Nascimento', 'Senha padrão', 'Nova senha']
        ].copy()
        df = df[df['Turma'].isin(self.turmas)]
        print(f'turmas {df['Turma'].unique().tolist()}')
        return df

    def gerenciar(self, plataforma):
        self.master.get(self.pp.url)
        plataformas = {
            'netescola' : self.gerenciar_netescola,
            'google'    : self.gerenciar_google,
        }
        return plataformas[plataforma]()

    def gerenciar_netescola(self):
        def anunciar(ind, aluno: str, _turma: str, texto: str):
            sys.stdout.write(f'\r {ind} {aluno} - {_turma}: {texto}.')
            sys.stdout.flush()
        início = 0

        for índice, linha in self.df.iloc[início:].iterrows():
            estudante  = str(linha['Estudante'])
            turma      = str(linha['Turma'])
            matrícula  = str(linha['Matrícula'])
            email      = str(linha['Educacional'])
            dn         = str(linha['Data de Nascimento']).replace('/', '')
            nova_senha = str(linha['Nova senha'])

            anunciar(índice, estudante, turma, 'iniciando')

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
            anunciar(índice, estudante, turma, 'concluído.')
            print('\r')
            self.master.refresh()
            self.nv.aguardar_página()

    @staticmethod
    def gerenciar_google():
        print('GOOGLE')
        pass
