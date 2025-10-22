import sys
from pandas import DataFrame
from selenium.common import NoSuchElementException
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from app.auto.functions.navegaçãoweb import NavegaçãoWeb
from app.auto.data.sites.propriedades import Propriedades
from typing import Literal
import pandas as pd
import unicodedata


class GerenciadorDeCredenciais :

    def __init__(self, navegador: Chrome, path_database: str, tipo: Literal['netescola', 'google'],
                 turmas: list[str] = None, **kwargs) :
        print(f'class NetEscola instanciada.')

        self.master = navegador
        self.nv = NavegaçãoWeb(navegador, tipo)
        self.pp = Propriedades(site=tipo)
        self.turmas = turmas
        print(f'{self.turmas = }')

        self.df = self.dataframe(path_database)
        self.gerenciar(tipo)  # self.master.quit()

    def gerenciar(self, tipo) :

        início = 0
        if tipo not in ('netescola', 'google') :
            raise Exception(f'Tipo desconhecido: {tipo}')

        for índice, linha in self.df.iloc[início :].iterrows() :
            estudante = str(linha['Estudante'])
            turma = str(linha['Turma'])
            matrícula = str(linha['Matrícula'])
            email = str(linha['Educacional'])
            dn = str(linha['Data de Nascimento']).replace('/', '')
            nova_senha = str(linha['Nova senha'])
            senha_padrão = str(linha['Senha padrão'])
            senha_padrão2 = str(f'go2025{linha['Estudante'].lower().split()[0]}')

            print(estudante, turma, matrícula, email, dn, nova_senha, senha_padrão, senha_padrão2)

            # self.anunciar(índice, estudante, turma, 'iniciando')
            #
            # if tipo == 'netescola':
            #     self.gerenciar_netescola(matrícula, dn, email, nova_senha)
            #
            #     anunciar(índice, estudante, turma, 'concluído.')
            #     print('\r')
            #     self.master.refresh()
            #     self.nv.aguardar_página()
            #
            if tipo == 'google' :
                self.master.get(self.pp.url)
                self.gerenciar_google(estudante, email, senha_padrão, senha_padrão2, dn, nova_senha)

    def gerenciar_netescola(self, matrícula, dn, email, nova_senha) :
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

    def gerenciar_google(self, estudante, email, senha_padrão, senha_padrão2, dn, nova_senha) :
        self.nv.digitar_xpath('input email', string=email),
        self.nv.clicar('xpath', 'avançar email')

        print("Tentando 'senha_padrão'")
        self.nv.digitar_xpath('input senha', string=senha_padrão)
        self.nv.clicar('xpath', 'avançar senha')

        self.nv.aguardar_página()

        alerta = None

        try :

            alerta = self.master.find_element(By.XPATH, '//*[@id="c0"]/div[2]/span')

        except NoSuchElementException :
            self.nv.aguardar_página()
            pass

        if alerta is None :
            print('Acertamos. Seguindo....')
            self.nv.clicar('xpath', 'avançar senha')
        else :
            print("Erramos. Tentando 'senha_padrão2'")  # Elemento foi encontrado
            self.nv.digitar_xpath('input senha', string=senha_padrão2)
            self.nv.clicar('xpath', 'avançar senha')
            alerta = None

        try :

            alerta = self.master.find_element(By.XPATH, '//*[@id="c0"]/div[2]/span')
        except NoSuchElementException :
            self.nv.aguardar_página()
            pass

        if alerta is None :
            print('Acertamos. Seguindo....')
            self.nv.clicar('xpath', 'avançar senha')
        else :
            print("Erramos. Tentando 'dn'")  # Elemento foi encontrado
            self.nv.digitar_xpath('input senha', string=dn)
            self.nv.clicar('xpath', 'avançar senha')
            alerta = None

        try :

            alerta = self.master.find_element(By.XPATH, '//*[@id="c0"]/div[2]/span')
        except NoSuchElementException :
            self.nv.aguardar_página()
            pass

        if alerta is None :
            print('Acertamos. Seguindo....')
            self.nv.clicar('xpath', 'avançar senha')
        else :
            print("Erramos. Tentando 'nova_senha'")  # Elemento foi encontrado
            self.nv.digitar_xpath('input senha', string=nova_senha)
            self.nv.clicar('xpath', 'avançar senha')
            alerta = None

        try :

            alerta = self.master.find_element(By.XPATH, '//*[@id="c0"]/div[2]/span')
        except NoSuchElementException :
            self.nv.aguardar_página()
            pass

        if alerta is None :
            print('Acertamos. Seguindo....')
            self.nv.clicar('xpath', 'avançar senha')

        else :
            print('Não conseguimos acertar a senha desta pessoa')

        #################################################

        alerta = None
        senhas = dict(enumerate([senha_padrão, senha_padrão2, dn, nova_senha]))
        self._tentar_senha(senhas)

        try :
            alerta = self.master.find_element(By.XPATH, '//*[@id="c0"]/div[2]/span')
        except NoSuchElementException :
            pass

        if alerta :
            print(f'Erramos. tentando {senhas[índice + 1]}')

    def _tentar_senha(self, senhas) :
        for índice, senha in senhas.items() :
            # alerta = None
            print(f'Tentando {senha}')
            self.nv.digitar_xpath('input senha', string=senha)
            self.nv.clicar('xpath', 'avançar senha')

    def dataframe(self, path) :
        _df = pd.read_excel(path, 'Base Ativa')
        colunas = ['Turma', 'Matrícula', 'Educacional', 'Estudante', 'Data de Nascimento', 'Senha padrão', 'Nova senha']
        df: DataFrame = _df[colunas].copy()

        df['Turma'] = df['Turma'].astype(str).str.strip()

        df['Estudante'] = df['Estudante'].astype(str).str.normalize('NFKD').str.encode('ASCII',
                                                                                       errors='ignore').str.decode(
            'ASCII').str.strip()

        print(f'{df['Turma'].unique().tolist() = }')
        print(df.head())
        df = df[df['Turma'].isin(self.turmas)]

        return df

    @staticmethod
    def anunciar(ind, aluno: str, _turma: str, texto: str) :
        sys.stdout.write(f'\r {ind} {aluno} - {_turma}: {texto}.')
        sys.stdout.flush()
