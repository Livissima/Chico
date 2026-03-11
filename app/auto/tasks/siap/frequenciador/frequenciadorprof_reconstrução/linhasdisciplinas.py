import time

from selenium.common import StaleElementReferenceException
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

from app.auto import NavegaçãoWeb
from app.config.parâmetros.getters.tempo import tempo

class LinhasDisciplinas:
    def __init__(self, master: Chrome, navegação):
        self._master = master
        self._nv = navegação

        self.elemento = self.elementar()

    def elementar(self) -> list[WebElement]:
        seletor_tabela_update = (By.ID, 'cphFuncionalidade_UpdatePanel1')
        self._nv.reiniciar_disciplinas_diário(tempo.ano_atual)
        tabela_linhas = self._master.find_element(*seletor_tabela_update)
        tabela_calendário = tabela_linhas.find_element(By.TAG_NAME, 'tbody')
        linhas_gerais = tabela_calendário.find_elements(By.TAG_NAME, 'tr')
        linhas_resultado = [linha for linha in linhas_gerais if linha.get_attribute('class') != 'topo']

        return linhas_resultado
