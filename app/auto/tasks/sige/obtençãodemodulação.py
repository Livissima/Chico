import os.path
import time
from pathlib import Path

import pandas as pd
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By

from app.auto.tasks.taskregistry import TaskRegistry
from app.auto.functions.navegaçãoweb import NavegaçãoWeb
from app.auto.data.sites.propriedadesweb import PropriedadesWeb
from app.config.parâmetros import parâmetros

@TaskRegistry.registrar('obter modulações')
class ObtençãoDeModulação:
    def __init__(
            self,
            navegador: Chrome,
            path: str,
            **kwargs
    ):
        self.master = navegador
        self._path = Path(path, 'fonte', 'modulação.json')

        self._nv = NavegaçãoWeb(navegador, 'sige')
        self._pp = PropriedadesWeb('sige')

        self.executar()

    def _logon(self) -> None:
        self.master.get(self._pp.urls)
        self.master.maximize_window()
        self._nv.digitar_xpath('misc', 'input id', string=self._pp.credenciais['id'])
        self._nv.digitar_xpath('misc', 'input senha', string=self._pp.credenciais['senha'])
        self._nv.clicar('xpath', 'misc', 'entrar')
        self._nv.clicar('xpath', 'misc', 'alerta')

    def executar(self):
        self._logon()
        self._nv.acessar_destino('modulações')

        for cpf in self.professores:
            self._nv.digitar_xpath('lápis docs', 'relatórios', 'dossiê do servidor', 'cpf', string=cpf)
            self._nv.clicar('xpath livre', '//*[@id="gerarRel"]')
            self._nv.aguardar_página()
            self._nv.download_json(
                cpf,
                os.path.join(parâmetros.diretório_base, 'fonte', 'modulações'),
                'sondagem'
            )
            self._nv.clicar('xpath livre', '//*[@id="barraImpressao"]/img[1]')

        time.sleep(10)

    @property
    def professores(self):
        profs = pd.read_excel(os.path.join(parâmetros.diretório_base, 'fonte', 'Profs.xlsx'), sheet_name='profs')
        cpfs = profs['CPF'].tolist()
        return cpfs
