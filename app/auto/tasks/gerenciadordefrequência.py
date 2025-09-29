import os
import time
from os import PathLike

import pandas as pd
from selenium.webdriver.common.by import By
from app.auto.data.sites.propriedades import Propriedades
from app.auto.functions.javascript import SCRIPT_MARCAR_FALTA, SCRIPT_JUSTIFICAR, SCRIPT_IR_PARA_DATA
from app.auto.functions.navegaçãoweb import NavegaçãoWeb
from selenium.webdriver import Chrome


class GerenciadorDeFrequência :

    def __init__(
            self,
            navegador: Chrome,
            path: PathLike,
            data,
            **kwargs
    ):
        _path = os.path.join(path, 'fonte', 'Compilado Faltas.xlsx')
        self.df = self.__obter_df(_path)
        self.data = data
        self.master = navegador
        self.nv = NavegaçãoWeb(navegador, 'siap')
        self.pp = Propriedades(site='siap')

        self.executar()


    def executar(self) :
        self.master.get(self.pp.url)
        self.master.maximize_window()
        self._logon()
        self._acessar_painel_frequência()
        self._lançar_faltas()
        self.master.quit()

    def _logon(self) :
        credenciais = self.pp.credenciais
        self.nv.digitar_xpath('input login', string=credenciais['id'])
        self.nv.digitar_xpath('input senha', string=credenciais['senha'])
        self._resolver_captcha()
        self.nv.clicar('xpath', 'botão login')
        self.nv.aguardar_página()

    def _resolver_captcha(self) :
        captcha = self.master.find_element(By.XPATH, self.pp.xpaths['captcha'])
        self.nv.digitar_xpath('input captcha', string=captcha.text)

    def _acessar_painel_frequência(self) :
        self.nv.clicar('xpath', 'menu sistema')
        self.nv.clicar('xpath', 'menu frequência')
        self.nv.aguardar_página()

    def _lançar_faltas(self) :
        turmas = self.nv.obter_turmas_siap()
        for turma in turmas :
            self.nv.clicar('xpath livre', turma)

            nome_turma = self.master.find_element(By.XPATH, turma).text

            self.nv.aguardar_página()

            faltas_marcadas = self.__marcar_falta_individual()

            self.__justificar_falta_individual()

            self.__anunciar_faltas_lançadas(faltas_marcadas, nome_turma)

            self.__avançar_turma()


    def __justificar_falta_individual(self):
        ausentes = list(self._ausentes_na_data.keys())
        return self.master.execute_script(SCRIPT_JUSTIFICAR, ausentes)

    def __marcar_falta_individual(self):
        ausentes = list(self._ausentes_na_data.keys())
        return self.master.execute_script(SCRIPT_MARCAR_FALTA, ausentes)

    def __anunciar_faltas_lançadas(self, matrículas_clicadas, nome_turma):
        for matrícula in matrículas_clicadas:
            estudante = self._ausentes_na_data.get(matrícula, 'Não identificado')

            print(f'Falta lançada para: {estudante} - {matrícula}')
        print(f'Faltas lançadas na turma {nome_turma}: {len(matrículas_clicadas)}')


    @property
    def _ausentes_na_data(self) -> dict :
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


    def __ir_para_data(self, data_desejada):
        alteração_de_data = self.master.execute_script(SCRIPT_IR_PARA_DATA, data_desejada)
        print(f'{alteração_de_data = }')
        self.nv.aguardar_página()

    def __avançar_turma(self) :
        self.nv.clicar('xpath', 'salvar e próximo')

    @staticmethod
    def __obter_df(path):
        try:
            df = pd.read_excel(path, sheet_name='Compilado Faltas', dtype={'Matrícula' : str})
            return df
        except (FileNotFoundError, KeyError):
            return None
