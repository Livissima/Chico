import os.path
import time

import pandas as pd
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By

from app.auto.functions.navegaçãoweb import NavegaçãoWeb
from app.auto.data.sites.propriedades import Propriedades
from app.config.parâmetros import parâmetros


class ObtençãoDeModulação:
    def __init__(
            self,
            navegador: Chrome,
            path: str,
            **kwargs
    ):
        self.master = navegador
        self.path = os.path.join(path, 'fonte', 'modulação.json')

        self.nv = NavegaçãoWeb(navegador, 'sige')
        self.pp = Propriedades('sige')

        self.executar()

    def _logon(self) -> None:
        self.master.get(self.pp.url)
        self.master.maximize_window()
        self.nv.digitar_xpath('misc', 'input id', string=self.pp.credenciais['id'])
        self.nv.digitar_xpath('misc', 'input senha', string=self.pp.credenciais['senha'])
        self.nv.clicar('xpath', 'misc', 'entrar')
        self.nv.clicar('xpath', 'misc', 'alerta')

    def executar(self):
        self._logon()
        self.nv.caminhar('modulações')

        for cpf in self.professores:
            self.nv.digitar_xpath('lápis docs', 'relatórios', 'dossiê do servidor', 'cpf', string=cpf)
            self.nv.clicar('xpath livre', '//*[@id="gerarRel"]')
            self.nv.aguardar_página()
            self.nv.download_json(
                cpf,
                os.path.join(parâmetros.novo_diretório, 'fonte', 'modulações'),
                'sondagem'
            )
            self.nv.clicar('xpath livre', '//*[@id="barraImpressao"]/img[1]')

        time.sleep(10)

    @property
    def professores(self):
        profs = pd.read_excel(os.path.join(parâmetros.novo_diretório, 'fonte', 'Profs.xlsx'), sheet_name='profs')
        cpfs = profs['CPF'].tolist()
        return cpfs
