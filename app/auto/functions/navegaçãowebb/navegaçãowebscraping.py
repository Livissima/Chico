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


class NavegaçãoWebScraping :

    def __init__(self, master: Chrome, site: str) :
        self.master = master
        self._pp = Propriedades(site)
        self.__timeout = 10
        self.__args_wait = {'driver' : self.master, 'timeout' : self.__timeout}

    def obter_elemento(self, by, tag):
        seletor: tuple[str, str] = (by, tag)
        try :
            elemento_web = WebDriverWait(**self.__args_wait).until(presence_of_element_located(seletor))
            return elemento_web
        except Exception as e:
            print(f'Erro na obtenção de elemento: {seletor}\n{e}')

    def _obter_valor(self, *chaves) -> str :
        xpaths = self._pp.xpaths

        for chave in chaves :
            xpaths = xpaths[chave]
        xpath = xpaths

        elemento: tuple[str, str] = (By.XPATH, xpath)

        try :
            WebDriverWait(**self.__args_wait).until(presence_of_element_located(elemento))
            WebDriverWait(**self.__args_wait).until(visibility_of_element_located(elemento))
            _elemento = WebDriverWait(**self.__args_wait).until(element_to_be_clickable(elemento))
            valor = _elemento.text

            self.aguardar_página()
            return valor

        except ValueError as e :
            caminho = self.__obter_chave_por_valor(self.xpaths, xpath)
            if caminho :
                caminho_str = " > ".join(caminho)
                raise f"Erro: {e}\nMétodo: `obter_valor`\nitem: {caminho_str}\n"
            else :
                raise f"Erro: {e}\nMétodo: `obter_valor`\nxpath: {xpath}"

    def download_json(
            self,
            nome_arquivo,
            pasta_destino,
            tipo: Literal['fichas', 'contatos', 'gêneros', 'situações', 'sondagem'] | str
    ) -> bool:

        inicio = time.time()
        dados = self.__obter_tabelas(tipo)

        if dados:
            path_json = os.path.join(pasta_destino, f'{nome_arquivo}.json')
            os.makedirs(os.path.dirname(path_json), exist_ok=True)

            with open(path_json, 'w', encoding='utf-8') as arquivo :
                json.dump(dados, arquivo, ensure_ascii=False, indent=2)

            tempo = time.time() - inicio
            print(f'✓ {len(dados)} linhas extraídas em {tempo:.2f}s - {path_json}')
            return True
        else :
            print('Nenhum dado extraído')
            return False

    def __obter_tabelas(self, tipo: str) -> list[str] | list[dict[str, str]]:
        tipos_simples = {'contatos', 'situações', 'gêneros', 'sondagem'}
        script = """"""

        if tipo in tipos_simples :
            elemento = (By.CSS_SELECTOR, 'table.tabela')
            WebDriverWait(**self.__args_wait).until(presence_of_element_located(elemento))
            script = SCRIPT_OBTER_TABELAS_SIMPLES

        if tipo == 'fichas' :
            script = SCRIPT_OBTER_TABELAS_FICHAS

        dados = self.master.execute_script(script)
        return dados

    def __obter_chave_por_valor(self, dicionário: dict, valor_procurado: str, caminho=None) :
        if caminho is None :
            caminho = []
        for chave, valor in dicionário.items() :
            if isinstance(valor, dict) :
                resultado = self.__obter_chave_por_valor(valor, valor_procurado, caminho + [chave])
                if resultado :
                    return resultado
            elif valor == valor_procurado :
                return caminho + [chave]
        return None
