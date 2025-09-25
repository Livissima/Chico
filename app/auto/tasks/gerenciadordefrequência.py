import pandas as pd
from pandas import DataFrame, Series
from selenium.webdriver.common.by import By
from app.auto.data.sites.propriedades import Propriedades
from app.auto.functions.navegação import Navegação
from selenium.webdriver import Chrome

class GerenciadorDeFrequência:

    def __init__(self, navegador: Chrome, path, **kwargs):
        self.path_xlsx = path
        self.master = navegador
        self.nv = Navegação(navegador, 'siap')
        self.pp = Propriedades(site='siap')
        self.executar()
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

        for turma in turmas:
            self.nv.clicar('xpath livre', turma)
            self.nv.aguardar_página()


            elemento_coluna_pontinhos = self.master.find_element(By.CLASS_NAME, 'listaDeFrequencias')
            sub_elemento_pontinhos = elemento_coluna_pontinhos.find_element(By.CLASS_NAME, 'itens')
            lista_pontinhos = sub_elemento_pontinhos.find_elements(By.CSS_SELECTOR, 'div[data-matricula]')
            alvos = [alvo.click() for alvo in lista_pontinhos if alvo in self.faltosos_de_hoje]

            elemento_coluna_justificativas = self.master.find_element(By.CLASS_NAME, 'listaMotivoAusencia')
            sub_elemento_justificativas = elemento_coluna_justificativas.find_element(By.CLASS_NAME, 'itens')
            lista_divs = sub_elemento_justificativas.find_elements(By.CSS_SELECTOR, )
            justis = [div.find_element(By.TAG_NAME, 'select') for div in lista_divs if div.get_attribute('data-matrícula') in self.faltosos_de_hoje['Matrícula'] ]
            #Não testado






            self.nv.clicar('xpath', 'salvar e próximo')






    @property
    def faltosos_de_hoje(self) -> DataFrame:
        df = pd.read_excel(self.path_xlsx, sheet_name='Compilado Faltas')

        df = df[['Turma Real', 'Estudante', 'Data Falta', 'Lançado', 'Matrícula']]

        df = df[df['Lançado'] == 'Lançado']

        df['Data Falta'] = df['Data Falta'].dt.strftime('%d/%m/%Y')

        faltosos_de_hoje = df[df['Data Falta'] == self.pp.hoje]

        # faltosos_de_hoje = list(df_hoje['Estudante'])

        print(f'{type(faltosos_de_hoje) = }')

        return faltosos_de_hoje



