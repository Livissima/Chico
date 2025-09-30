import json
import os
import time
from os import PathLike

import pandas as pd
from selenium.webdriver.common.by import By
from app.auto.data.sites.propriedades import Propriedades
from app.auto.functions.javascript import SCRIPT_MARCAR_FALTA_COMO_ADM, SCRIPT_JUSTIFICAR, SCRIPT_IR_PARA_DATA
from app.auto.functions.navegaçãoweb import NavegaçãoWeb
from selenium.webdriver import Chrome

from app.auto.tasks.frequência import FrequenciadorAdm, FrequenciadorProf
from app.config.parâmetros import parâmetros


class Frequenciador :

    def __init__(
            self,
            navegador: Chrome,
            path: PathLike,
            data = None,
            **kwargs
    ):
        _path = os.path.join(path, 'fonte', 'Compilado Faltas.xlsx')
        self.df = self.__obter_df_faltas(_path)
        self.data = data
        self.master = navegador
        self.nv = NavegaçãoWeb(navegador, 'siap')
        self.pp = Propriedades(site='siap')
        self._executar()

    def _logon(self, usuário, _id, senha) :
        #credenciais = self.pp.credenciais
        print(f'Fazendo login para: {usuário}')
        self.nv.digitar_xpath('input login', string=_id)
        self.nv.digitar_xpath('input senha', string=senha)
        self.__resolver_captcha()
        self.nv.clicar('xpath', 'botão login')
        self.nv.aguardar_página()

    def _executar(self):
        self.master.get(self.pp.url)
        self.master.maximize_window()

        for usuário, credenciais in self.pp.credenciais.items():
            print(f'Iterando sobre {usuário}')
            id_cpf_prof = credenciais['id']
            senha = credenciais['senha']
            tipo = credenciais['tipo']

            self._logon(usuário, id_cpf_prof, senha)

            self._execução_por_usuário(tipo, id_cpf_prof)
            self.master.delete_all_cookies()
            time.sleep(2)
            self.master.get(self.pp.url)

    def _execução_por_usuário(self, tipo, cpf_prof) :

        if tipo == 'adm':
            FrequenciadorAdm(self.master, self.ausentes_na_data)
        if tipo == 'prof':
            FrequenciadorProf(self.master, cpf_prof, self.ausentes_na_data)

    @property
    def ausentes_na_data(self) -> dict :
        if self.df is None:
            ausentes = {'Matrícula': None, 'Estudante' : None}
            return ausentes

        else:
            df = self.df.copy()
            df = df[['Turma Real', 'Estudante', 'Data Falta', 'Lançado', 'Matrícula']]
            df['Data Falta'] = df['Data Falta'].dt.strftime('%d/%m/%Y')
            df = df[df['Data Falta'] == self.data]
            ausentes = dict(zip(df['Matrícula'], df['Estudante']))
            return ausentes

    @staticmethod
    def __obter_df_faltas(path):
        try:
            df = pd.read_excel(path, sheet_name='Compilado Faltas', dtype={'Matrícula' : str})
            return df
        except (FileNotFoundError, KeyError):
            return None

    def __resolver_captcha(self) :
        captcha = self.master.find_element(By.XPATH, self.pp.xpaths['captcha'])
        self.nv.digitar_xpath('input captcha', string=captcha.text)


