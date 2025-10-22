import json
import os
import time
from os import PathLike
from pathlib import Path
from typing import Literal

import pandas as pd
from pandas import DataFrame
from selenium.webdriver.common.by import By
from app.auto.data.sites.propriedades import Propriedades
from app.auto.functions.navegaçãoweb import NavegaçãoWeb
from selenium.webdriver import Chrome

from app.auto.tasks.frequenciador import FrequenciadorAdm, FrequenciadorProf
from app.auto.tasks.frequenciador.relatóriodeausências import RelatórioDeAusências
from app.config.parâmetros import parâmetros


class Frequenciador :

    def __init__(
            self,
            navegador: Chrome,
            path: PathLike,
            data = None,
            **kwargs
    ):
        # _path: PathLike = Path(path, 'fonte', 'Compilado Faltas.xlsx')
        self.ausências = RelatórioDeAusências(path, data)
        self.master = navegador
        self.nv = NavegaçãoWeb(navegador, 'siap')
        self.pp = Propriedades(site='siap')
        self._executar()



    def _executar(self):
        self.nv.acessar_página(self.pp.url)

        for usuário, credenciais in self.pp.credenciais.items():
            print(f'\n → Iterando sobre {usuário}')

            id_cpf_prof = credenciais['id']
            senha = credenciais['senha']
            tipo = credenciais['tipo']

            self._logon(usuário, id_cpf_prof, senha)
            self._executar_usuário(tipo, id_cpf_prof)
            self.__recomeçar()

            print(f'Frequenciamento finalizado para {usuário}\n')


    def _executar_usuário(self, tipo_de_usuário: Literal['adm', 'prof'], cpf_prof) :
        executar = {
            'adm' : lambda: FrequenciadorAdm(self.master, self.ausências.dicionário),
            'prof' : lambda: FrequenciadorProf(self.master, cpf_prof, self.ausências.dataframe)
        }
        executar[tipo_de_usuário]()


    def _logon(self, usuário, _id, senha) :
        print(f'Fazendo login para: {usuário}')
        self.__inserir_credenciais(_id, senha)
        self.__resolver_captcha()
        self.nv.clicar('xpath', 'botão login')
        self.nv.aguardar_página()

    def __resolver_captcha(self) :
        captcha = self.master.find_element(By.XPATH, self.pp.xpaths['captcha'])
        self.nv.digitar_xpath('input captcha', string=captcha.text)

    def __inserir_credenciais(self, _id, senha):
        self.nv.digitar_xpath('input login', string=_id)
        self.nv.digitar_xpath('input senha', string=senha)

    def __recomeçar(self):
        self.master.delete_all_cookies()
        time.sleep(2)
        self.master.get(self.pp.url)
