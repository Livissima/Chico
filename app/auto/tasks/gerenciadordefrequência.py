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

from app.config.parâmetros import parâmetros


class GerenciadorDeFrequência :

    def __init__(
            self,
            navegador: Chrome,
            path: PathLike,
            data = None,
            **kwargs
    ):
        self._obter_modulações()
        # _path = os.path.join(path, 'fonte', 'Compilado Faltas.xlsx')
        # self.df = self.__obter_df_faltas(_path)
        # self.data = data
        # self.master = navegador
        # self.nv = NavegaçãoWeb(navegador, 'siap')
        # self.pp = Propriedades(site='siap')
        # self._executar()


    def _executar(self):
        for usuário, credenciais in self.pp.credenciais.items():
            _id = credenciais['id']
            senha = credenciais['senha']
            tipo = credenciais['tipo']
            self._execução_por_usuário(usuário, _id, senha, tipo)
            time.sleep(5)


    def _execução_por_usuário(self, usuário, _id, senha, tipo) :
        self.master.get(self.pp.url)
        self.master.maximize_window()

        self._logon(usuário, _id, senha)
        self.nv.aguardar_página()

        self._acessar_painel_frequência(tipo)
        self._lançar_faltas()
        self.master.quit()

    def _logon(self, usuário, _id, senha) :
        #credenciais = self.pp.credenciais
        print(f'Fazendo login para: {usuário}')
        self.nv.digitar_xpath('input login', string=_id)
        self.nv.digitar_xpath('input senha', string=senha)
        self._resolver_captcha()
        self.nv.clicar('xpath', 'botão login')
        self.nv.aguardar_página()

    def _resolver_captcha(self) :
        captcha = self.master.find_element(By.XPATH, self.pp.xpaths['captcha'])
        self.nv.digitar_xpath('input captcha', string=captcha.text)

    def _acessar_painel_frequência(self, tipo) :
        if tipo == 'Professor':
            self.nv.clicar('xpath', 'menu sistema')
            self.nv.clicar('xpath', 'menu frequência')
        if tipo == 'ADM':
            self.nv.clicar('xpath', 'menu sistema')
            # self.nv.clicar('xpath', 'menu frequência')
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
        return self.master.execute_script(SCRIPT_MARCAR_FALTA_COMO_ADM, ausentes)

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
    def __obter_df_faltas(path):
        try:
            df = pd.read_excel(path, sheet_name='Compilado Faltas', dtype={'Matrícula' : str})
            return df
        except (FileNotFoundError, KeyError):
            return None

    def _obter_modulações(self):
        dados = []
        lista_jsons = os.listdir(os.path.join(parâmetros.novo_diretório, 'fonte', 'modulações'))
        print(f'{lista_jsons = }')
        lista_dicionarios = []


        for arquivo in lista_jsons :
            if arquivo.endswith('.json') :
                caminho = os.path.join(parâmetros.novo_diretório, 'fonte', 'modulações', arquivo)
                with open(caminho, 'r', encoding='utf-8') as f :
                    lista_dicionarios.append(json.load(f))

        for i in lista_dicionarios:
            cpf = i[1]['coluna_1']
            nome = i[1]['coluna_3']
            print(cpf, nome)
            print(f'{i[3:] = }')




        # return df_final

        pass