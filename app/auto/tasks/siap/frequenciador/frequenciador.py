import time
from os import PathLike
from typing import Literal

from selenium.webdriver.common.by import By

from app.auto.tasks.registrotasks import RegistroTasks
from app.auto.data.sites.propriedadesweb import PropriedadesWeb
from app.auto.functions.navegaçãoweb import NavegaçãoWeb
from selenium.webdriver import Chrome

from app.auto.tasks.siap.frequenciador import FrequenciadorAdm, FrequenciadorProf
from app.auto.tasks.siap.frequenciador.relatóriodeausências import RelatórioDeAusências

@RegistroTasks.registrar('siap')
class Frequenciador :

    def __init__(
            self,
            navegador: Chrome,
            path: PathLike,
            periodo: list[str],
            # data = None,
            **kwargs
    ):
        # print(f'{data = }')
        print(f'frequenciador: {path = }')
        print(f'frequenciador: {periodo = }')
        self._período = periodo
        # _path: PathLike = Path(path, 'fonte', 'Compilado Faltas.xlsx')
        self._ausências = RelatórioDeAusências(path)
        self._master = navegador
        self._nv = NavegaçãoWeb(navegador, 'siap')
        self._pp = PropriedadesWeb(site='siap')
        self._executar()



    def _executar(self):
        self._nv.acessar_destino(self._pp.urls)

        for usuário, credenciais in self._pp.credenciais.items():
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
            'adm' : lambda: FrequenciadorAdm(
                navegador=self._master,
                período=self._período,
                relatório_de_ausências=self._ausências.dataframe
            ),
            'prof' : lambda: FrequenciadorProf(
                navegador=self._master,
                professor=cpf_prof,
                ausentes_na_data=self._ausências.dataframe
            )
        }
        executar[tipo_de_usuário]()


    def _logon(self, usuário, _id, senha) :
        print(f'Fazendo login para: {usuário}')
        self.__inserir_credenciais(_id, senha)
        self.__resolver_captcha()
        self._nv.clicar('xpath', 'botão login')
        self._nv.aguardar_página()

    def __resolver_captcha(self) :
        captcha = self._master.find_element(By.XPATH, self._pp.xpaths['captcha'])
        self._nv.digitar_xpath('input captcha', string=captcha.text)

    def __inserir_credenciais(self, _id, senha):
        self._nv.digitar_xpath('input login', string=_id)
        self._nv.digitar_xpath('input senha', string=senha)

    def __recomeçar(self):
        self._master.delete_all_cookies()
        time.sleep(2)
        self._master.get(self._pp.urls)
