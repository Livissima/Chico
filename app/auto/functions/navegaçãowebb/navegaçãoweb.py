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
from app.auto.functions.navegaçãowebb.geral import Mobilidade
from app.auto.functions.navegaçãowebb.navegaçãowebscraping import NavegaçãoWebScraping
from app.auto.functions.navegaçãowebb.siap import NavegaçãoWebSiap
from app.auto.functions.navegaçãowebb.sige import NavegaçãoWebSige
from app.config.parâmetros import parâmetros


class NavegaçãoWeb :
    #todo distribuir responsabilidades para sub módulos

    def __init__(self, master: Chrome, site: str) :
        self.master = master
        self._pp = Propriedades(site)

        self.mobilidade = Mobilidade()

        #todo parei aqui. A instância de mobilidade deve alimentar as instâncias de navegação diversas.
        self.nv_web_sige = NavegaçãoWebSige()
        self.nv_web_siap = NavegaçãoWebSiap()
        self.nv_web_scraping = NavegaçãoWebScraping()

        self.__timeout = 10
        self.__args_wait = {'driver' : self.master, 'timeout' : self.__timeout}

