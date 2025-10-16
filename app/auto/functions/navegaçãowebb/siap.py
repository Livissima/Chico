import json
import os.path
import time
from typing import Literal, Generator, Any
from selenium.common import ElementClickInterceptedException, StaleElementReferenceException
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import presence_of_element_located, visibility_of_element_located, \
    element_to_be_clickable, staleness_of

from app.auto.data.sites.propriedades import Propriedades
from app.auto.functions.javascript import SCRIPT_OBTER_TABELAS_SIMPLES, SCRIPT_OBTER_TABELAS_FICHAS, \
    SCRIPT_SELECIONAR_DISPARANDO_EVENTO
from app.config.parâmetros import parâmetros

class NavegaçãoWebSiap:
    def __init__(self, master: Chrome) :
        self.master = master
        self._pp = Propriedades('siap')

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
