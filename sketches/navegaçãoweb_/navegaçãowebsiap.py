from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By

from app.auto.data.dataclasses.propriedadesweb import PropriedadesWeb
from app.auto.functions.javascript import SCRIPT_OBTER_TABELAS_SIMPLES, SCRIPT_OBTER_TABELAS_FICHAS, \
    SCRIPT_SELECIONAR_DISPARANDO_EVENTO


class NavegaçãoWebSiap:
    def __init__(
            self,
            # mobilidade,
            master: Chrome = None
    ):
        # self.__mobilidade = mobilidade
        self.master = master
        self._pp = PropriedadesWeb('siap')

        self.__timeout = 10
        self.__args_wait = {'driver' : self.master, 'timeout' : self.__timeout}

    def obter_turmas_siap(self) -> list[str]:
        container_turmas = self.master.find_element(By.CLASS_NAME, 'containerTurmaTurno')
        # print(container_turmas)
        lista_xpath = []
        elementos_turmas = container_turmas.find_elements(By.CLASS_NAME, 'listaTurmas ')

        for índice, elemento in enumerate(elementos_turmas, start=1) :
            xpath_turma = f'/html/body/form/div[4]/div[2]/div/div/div/div[1]/div[{índice}]'
            lista_xpath.append(xpath_turma)

        print(f'{lista_xpath = }')
        return lista_xpath

    # def __getattr__(self, item):
    #     return getattr(self.__mobilidade, item)

