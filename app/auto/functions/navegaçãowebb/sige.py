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

class NavegaçãoWebSige:
    def __init__(self, master: Chrome) :
        self.master = master
        self._pp = Propriedades('sige')

        self.__timeout = 10
        self.__args_wait = {'driver' : self.master, 'timeout' : self.__timeout}

    def iterar_turmas_sige(self) -> Generator[tuple[Any, Any], Any, None]:
        for série in parâmetros.séries_selecionadas :
            self._selecionar_série(série)
            turmas_correspoentes = parâmetros.turmas_selecionadas_por_série[série]
            for turma in turmas_correspoentes :
                self._selecionar_turma_sige(turma)
                yield série, turma

    def _selecionar_turma_sige(self, turma) -> None :
        self.__selecionar_opção('composição', valor='199')
        self.__selecionar_opção('turno', valor='1')
        self.__selecionar_opção('turma', texto=turma)

    def _selecionar_série(self, série) -> None :
        self.__selecionar_opção('composição', valor='199')
        self.__selecionar_opção('série', texto=f'{série}º Ano')
        self.__selecionar_opção('turno', valor='1')

    def __selecionar_opção(self, alvo, valor=None, texto=None) -> None:

        id_element = self._pp.ids[alvo]

        elemento: tuple[str, str] = (By.ID, id_element)

        selecionar_elemento = WebDriverWait(**self.__args_wait).until(presence_of_element_located(elemento))

        selecionar = Select(selecionar_elemento)

        if valor is None and texto is None or valor is not None and texto is not None :
            raise ValueError(f"Nenhum argumento inserido para preenchimento de '{alvo}'")

        if valor :
            selecionar.select_by_value(valor)

        if texto :
            selecionar.select_by_visible_text(texto)