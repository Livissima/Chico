import pandas as pd
from pandas import DataFrame, Series
from selenium.webdriver.common.by import By
from app.auto.data.sites.propriedades import Propriedades
from app.auto.functions.navegação import Navegação
from selenium.webdriver import Chrome

class Presenciamento:

    def __init__(self, navegador: Chrome, path, **kwargs):
        self.path_xlsx = path
        self.master = navegador
        self.nv = Navegação(navegador, 'siap')
        self.pp = Propriedades(site='siap')
        self.faltosos_de_hoje
        # self.executar()
        # self.master.quit()

    def executar(self):
        self.master.get(self.pp.url)
        self.master.maximize_window()
        self._logon()
        self._ir_painel_frequência()
        self._presenciar_todos()

    def _logon(self):
        credenciais = self.pp.credenciais
        self.nv.digitar_xpath('input login', string=credenciais['id'])
        self.nv.digitar_xpath('input senha', string=credenciais['senha'])
        self._passar_captcha()
        self.nv.clicar('xpath', 'botão login')
        self.nv.aguardar_página()

    def _passar_captcha(self):
        captcha = self.master.find_element(By.XPATH, self.pp.xpaths['captcha'])
        self.nv.digitar_xpath('input captcha', string=captcha.text)

    def _ir_painel_frequência(self):
        self.nv.clicar('xpath', 'menu sistema')
        self.nv.clicar('xpath', 'menu frequência')
        self.nv.aguardar_página()

    def _presenciar_todos(self):
        turmas = self.nv.obter_turmas_siap()
        # print(turmas)
        for turma in turmas:
            self.nv.clicar('xpath livre', turma)
            self.nv.aguardar_página()
            self.nv.clicar('xpath', 'salvar e próximo')

    @property
    def faltosos_de_hoje(self) -> list:
        df = pd.read_excel(self.path_xlsx, sheet_name='Compilado Faltas')

        df = df[['Turma Real', 'Estudante', 'Data Falta', 'Lançado']]
        df = df[df['Lançado'] == 'Lançado']

        df['Data Falta'] = df['Data Falta'].dt.strftime('%d/%m/%Y')

        df_hoje = df[df['Data Falta'] == self.pp.hoje]
        faltosos_de_hoje = list(df_hoje['Estudante'])
        print(f'{faltosos_de_hoje = }')
        return faltosos_de_hoje


