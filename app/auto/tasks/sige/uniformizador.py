import time

import pandas as pd
from pandas import DataFrame
from selenium.webdriver.common.by import By

from app.auto.data.sites.propriedadesweb import PropriedadesWeb
from app.auto.functions.navegaçãoweb import NavegaçãoWeb



class Uniformizador:
    xpaths = {

    }



    def __init__(self,
                 navegador,
                 path,
                 **kwargs
                 ):
        self.master = navegador
        self._path = path
        self._pp = PropriedadesWeb('sige')
        self._nv = NavegaçãoWeb(navegador, 'sige')
        self._executar(path)

    def _executar(self, path):
        self._logon()
        SÉRIES = ['6', '7', '8', '9']
        TURMAS = {
            '6' : ['6A', '6B', '6C'],
            '7' : ['7A', '7B'],
            '8' : ['8A', '8B'],
            '9' : ['9A']
        }
        for série, turma in self._nv.iterar_turmas_sige(SÉRIES, TURMAS):
            self._percorrer_turma(turma)

    def _percorrer_turma(self, turma):
        self._nv.clicar('xpath livre', '//*[@id="cmdConsultar"]')
        self._nv.aguardar_página()

        tabela = self._nv.obter_elemento(By.ID, 'tblAlunos')
        print(f'{tabela = }')

        linhas_tabela = tabela.find_elements(By.TAG_NAME, 'tr')[1:]
        print(f'{linhas_tabela = }')

        matrículas = [(str(linha.get_attribute('onclick')).split("','")[0]).strip("editar('") for linha in linhas_tabela]
        print(f'{len(matrículas) = } __ {matrículas = }')

        # elementos_botões = [linha.find_elements(By.TAG_NAME, 'td')[-1] for linha in linhas_tabela]
        elementos_botões = [linha for linha in linhas_tabela]
        print(f'{len(elementos_botões) = } __ {elementos_botões = }')

        dicionário = dict(zip(matrículas, elementos_botões))
        for _matrícula, _botão in dicionário.items():
            # icone_disponível = None
            #
            # try:
            #     icone_disponível = _botão.find_element(By.TAG_NAME, 'img').get_attribute('src') == '../../imagens/edit_disabled.png'
            #
            # except:
            #     pass
            #
            # if not icone_disponível:
            #     continue

            # Instead of _botão.click(), use:
            print(f'Clicando em {_matrícula}')
            try:
                self.master.execute_script("arguments[0].click();", _botão)
                self._nv.aguardar_página(1)
                self._preencher_indivíduo(_matrícula)
            except:
                continue

        print(f'Turma {turma} finalizada.')

    def _preencher_indivíduo(self, matrícula):
        print(f'Preenchendo indivíduo: {matrícula}')
        df = self.dataframe()
        df = df[df['Matrícula'] == matrícula]
        tamanho_roupa = df['Tamanho roupa']
        tamanho_pé = df['Tamanho pé']
        tamanho_meia = df['Tamanho meia']

        self._nv.selecionar_dropdown('xpath', 'uniformes', 'camiseta', texto=tamanho_roupa)
        self._nv.selecionar_dropdown('xpath', 'uniformes', 'calça', texto=tamanho_roupa)
        self._nv.selecionar_dropdown('xpath', 'uniformes', 'regata', texto=tamanho_roupa)

        indicador_bt = ''
        indicador_dd = ''
        if df['Gênero'] == 'M' :
            indicador_bt = 'bt bermuda'
            indicador_dd = 'bermuda'
        if df['Gênero'] == 'F' :
            indicador_bt = 'bt saia'
            indicador_dd = 'saia'

        self._nv.clicar('xpath', 'uniformes', indicador_bt)
        self._nv.selecionar_dropdown('xpath', 'uniforme', indicador_dd, texto=tamanho_roupa)
        self._nv.selecionar_dropdown('xpath', 'uniforme', 'jaqueta', texto=tamanho_roupa)
        self._nv.selecionar_dropdown('xpath', 'uniforme', 'tênis', texto=tamanho_pé)
        self._nv.selecionar_dropdown('xpath', 'uniforme', 'meias', texto=tamanho_meia)

    def dataframe(self) -> DataFrame:
        return pd.read_excel(self._path)



    def _logon(self) :
        self.master.get(self._pp.url)
        self.master.maximize_window()
        self._nv.digitar_xpath('misc', 'input id', string=self._pp.credenciais['id'])
        self._nv.digitar_xpath('misc', 'input senha', string=self._pp.credenciais['senha'])
        self._nv.clicar('xpath', 'misc', 'entrar')
        self._nv.clicar('xpath', 'misc', 'alerta')
        self._nv.clicar('xpath livre', '//*[@id="smoothmenu1"]/ul/li[5]/h4/a')
        self._nv.clicar('xpath livre', '//*[@id="smoothmenu1"]/ul/li[5]/ul/li[20]/a')

