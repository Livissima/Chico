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

class Mobilidade:
    def __init__(self, master: Chrome, site: str) :
        self.master = master
        self._pp = Propriedades(site)
        self.__timeout = 10
        self.__args_wait = {'driver' : self.master, 'timeout' : self.__timeout}

    def clicar(
            self,
            by: Literal['xpath', 'id', 'css', 'css livre', 'xpath livre', 'id livre'] = 'xpath',
            *chaves: str,
            elemento_espera = None
    ) -> None :

        tag = None
        if 'livre' not in by:
            by_dict_de_dicts = {
                'xpath' : self._pp.xpaths, 'id' : self._pp.ids, 'css' : self._pp.css_selectors
            }

            tags = by_dict_de_dicts[by.lower()]

            for chave in chaves :
                tags = tags[chave]
            tag = tags

        if 'livre' in by:
            tag = chaves[0]

        by_dict = {
            'xpath'       : By.XPATH, 'id'       : By.ID, 'css'       : By.CSS_SELECTOR,
            'xpath livre' : By.XPATH, 'id livre' : By.ID, 'css livre' : By.CSS_SELECTOR
        }

        _BY = by_dict[by.lower()]
        elemento: tuple[str, str] = (_BY, tag)

        try :
            elemento_web = WebDriverWait(**self.__args_wait).until(presence_of_element_located(elemento))

            self.master.execute_script(
                "arguments[0].scrollIntoView({block: 'center', behavior: 'smooth'});",
                elemento_web
            )
            WebDriverWait(**self.__args_wait).until(visibility_of_element_located(elemento))
            WebDriverWait(**self.__args_wait).until(element_to_be_clickable(elemento)).click()

            self._esperar_por_carregamento()

            if elemento_espera:
                self._esperar_por_elemento_dependente(elemento_espera)

            self.aguardar_página()

        except KeyError as e :
            caminho = self.__obter_chave_por_valor(tags, tag)
            if caminho :
                caminho_str = " > ".join(caminho)
                raise f"Erro: {e}\nMétodo: `clicar`\nitem: '{caminho_str}'\n"
            else :
                raise f"Erro: {e}\nMétodo: `clicar`\ntag: '{tag}'"

        except ElementClickInterceptedException:
            try :
                self.master.execute_script("arguments[0].click();", elemento_web)
                # print(f"Clique via JavaScript em: {str(*chaves[-1 :])}")
                self.aguardar_página()
            except Exception as js_error :
                raise f"Falha no clique via JavaScript: {js_error}"

    def caminhar(self, destino: str) -> None :
        print(f'    Caminhando para {destino}')
        destinos = self._pp.caminhos
        for tupla in destinos[destino] :
            self.clicar('xpath', *tupla)

    def acessar_página(self, url):
        self.master.get(url)
        self.master.maximize_window()
        self.aguardar_página()

    def digitar_xpath(self, *chaves, string: str) -> None:
        xpaths = self._pp.xpaths

        for chave in chaves :
            xpaths = xpaths[chave]
        xpath = xpaths

        elemento: tuple[str, str] = (By.XPATH, xpath)

        try :
            WebDriverWait(**self.__args_wait).until(presence_of_element_located(elemento))
            WebDriverWait(**self.__args_wait).until(visibility_of_element_located(elemento))
            el = WebDriverWait(**self.__args_wait).until(element_to_be_clickable(elemento))
            el.clear()  # limpa antes de digitar
            el.send_keys(string)
            self.aguardar_página()

        except ValueError as e :
            caminho = self.__obter_chave_por_valor(self._pp.xpaths, xpath)
            if caminho :
                caminho_str = " > ".join(caminho)
                raise f"Erro: {e}\nMétodo: `digitar_xpath`\nstring: {string}'\nitem: {caminho_str}\n"
            else :
                raise f"Erro: {e}\nMétodo: `digitar_xpath`\nstring: '{string}'\nxpath: {xpath}"

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

    def aguardar_página(self, tempo_adicional: float | None = None) -> None :
        elemento = (By.TAG_NAME, 'body')
        WebDriverWait(**self.__args_wait).until(presence_of_element_located(elemento))
        WebDriverWait(**self.__args_wait).until(visibility_of_element_located(elemento))

        if tempo_adicional:
            time.sleep(tempo_adicional)

    def aguardar_preenchimento(self, elemento: str) -> None:
        def _predicate(driver) :
            try :
                elem = driver.find_element(By.ID, elemento)
                value = elem.get_attribute("value")
                return value.strip() != ""
            except StaleElementReferenceException:
                return False

        WebDriverWait(**self.__args_wait).until(_predicate)

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


    def selecionar_dropdown(self, *chaves, valor = None, texto = None, elemento_espera = None) :
        script = SCRIPT_SELECIONAR_DISPARANDO_EVENTO
        xpaths = self._pp.xpaths

        for chave in chaves :
            xpaths = xpaths[chave]
        xpath = xpaths

        seletor: tuple[str, str] = (By.XPATH, xpath)

        try :
            WebDriverWait(**self.__args_wait).until(presence_of_element_located(seletor))
            WebDriverWait(**self.__args_wait).until(visibility_of_element_located(seletor))
            WebDriverWait(**self.__args_wait).until(element_to_be_clickable(seletor))
            elemento = self.master.find_element(*seletor)
            if valor:
                self.master.execute_script(script, elemento, valor)
            if texto:
                Select(elemento).select_by_visible_text(texto)

            try:
                WebDriverWait(self.master, 2).until(staleness_of(elemento))
            except Exception():
                pass

            self._esperar_por_carregamento()

            if elemento_espera:
                self._esperar_por_elemento_dependente(elemento_espera)

            self.aguardar_página()

        except Exception as e:
            print(f'Problema na seleção disparando evento: {e}')

    def _esperar_por_carregamento(self) :
        try:
            WebDriverWait(**self.__args_wait).until(lambda driver : len(
                driver.find_elements(By.CSS_SELECTOR, ".loading, .spinner, [aria-busy='true']")) == 0)
        except:
            pass
        try:
            WebDriverWait(**self.__args_wait).until(
                lambda driver : driver.execute_script("return jQuery.active == 0"))
        except:
            pass

        try:
            WebDriverWait(**self.__args_wait).until(
                lambda driver : driver.execute_script("return document.readyState") == "complete")
        except:
            pass

    def _esperar_por_elemento_dependente(self, elemento_espera: tuple[str, str]) :
        try:
            WebDriverWait(**self.__args_wait).until(element_to_be_clickable(elemento_espera))
        except:
            print(f"Elemento dependente não carregou: {elemento_espera}")

    def _esperar_por_mudanca_estado(self, elemento, atributo, valor_antigo) :
        WebDriverWait(**self.__args_wait).until(lambda driver : elemento.get_attribute(atributo) != valor_antigo)

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

    def _selecionar_opção(self, alvo, valor=None, texto=None) -> None:
        #todo aprimorar os dependentes deste método para que consigam lidar com outras composições e turnos.

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

    # def selecionar(self, div, valor = '1'):
    #
    #     selecionar_elemento = WebDriverWait(**self.__args_wait).until(presence_of_element_located(div))
    #     selecionar = Select(selecionar_elemento)
    #     selecionar.select_by_value(valor)

    @staticmethod
    def __extrair_dados_tabela(tabela, cabeçalhos) :
        dados = []

        try :
            linhas = tabela.find_elements(By.CSS_SELECTOR, 'tbody tr')

            for linha in linhas :
                try :
                    ths = linha.find_elements(By.CSS_SELECTOR, 'th')
                    if ths :
                        continue

                    texto_linha = linha.text.lower()
                    texto_cabeçalhos = ' '.join(cabeçalhos).lower()

                    correspondências = sum(1 for cabeçalho in cabeçalhos if cabeçalho.lower() in texto_linha)
                    if correspondências > 3 :
                        continue
                except :
                    pass

                células = linha.find_elements(By.CSS_SELECTOR, 'td')
                if not células :
                    continue

                linha_dados = {}

                for índice, célula in enumerate(células) :
                    if índice < len(cabeçalhos) :
                        nome_coluna = cabeçalhos[índice]
                        linha_dados[nome_coluna] = célula.text.strip()
                    else :
                        linha_dados[f'Coluna_extra_{índice}'] = célula.text.strip()

                if any(linha_dados.values()) :
                    dados.append(linha_dados)

        except Exception as e :
            print(f'Erro ao extrair dados da tabela: {e}')

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
