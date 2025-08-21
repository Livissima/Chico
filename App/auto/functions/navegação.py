from typing import Literal

from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import presence_of_element_located, visibility_of_element_located, element_to_be_clickable

from App.auto.info.sites.propriedades import Propriedades
from App.auto.info.misc.escola import Escola


class Navegação:
    def __init__(self, master: Chrome, site: str):
        self._master = master
        self._pp = Propriedades(site)
        self._ue = Escola()
        self._timeout = 10
        self._args_wait = {'driver': self._master, 'timeout': self._timeout}


    def clicar(self, by: Literal['xpath', 'id', 'css'], *chaves: str):
        by_dict_de_dicts = {
            'xpath' : self._pp.xpaths, 'id' : self._pp.ids, 'css' : self._pp.css_selectors
        }

        tags = by_dict_de_dicts[by.lower()]

        for chave in chaves:
            tags = tags[chave]
        tag = tags

        by_dict = {
            'xpath' : By.XPATH, 'id' : By.ID, 'css' : By.CSS_SELECTOR
        }

        _BY = by_dict[by.lower()]

        elemento: tuple[str, str] = (_BY, tag)

        try:
            WebDriverWait(**self._args_wait).until(presence_of_element_located(elemento))
            WebDriverWait(**self._args_wait).until(visibility_of_element_located(elemento))
            WebDriverWait(**self._args_wait).until(element_to_be_clickable(elemento)).click()
            # print(f'Click em: {str(*chaves[-1:])}')
            self.aguardar()

        except KeyError as e:
            caminho = self._obter_chave_por_valor(tags, tag)
            if caminho:
                caminho_str = " > ".join(caminho)
                raise f"Erro: {e}\nMétodo: `clicar`\nitem: '{caminho_str}'\n"
            else:
                raise f"Erro: {e}\nMétodo: `clicar`\ntag: '{tag}'"


    def caminhar(self, destino: Literal['fichas', 'contatos', 'situações', 'gêneros']):
        # uma recursão seria melhor
        if destino not in ['fichas', 'contatos', 'situações', 'gêneros']:
            raise KeyError(f"Tipo inválido chamado no método de ir para menu: '{destino}'")

        print(f'    Caminhando para {destino}')
        destinos = self._pp.caminhos
        for tupla in destinos[destino]:
            # print('Click em: ', end='')
            # print(f'{str(tupla[-1:])}', end=', ')
            self.clicar('xpath', *tupla)

    def digitar_xpath(self, *chaves, string: str):
        xpaths = self._pp.xpaths

        for chave in chaves:
            xpaths = xpaths[chave]
        xpath = xpaths

        elemento: tuple[str, str] = (By.XPATH, xpath)

        try:
            WebDriverWait(**self._args_wait).until(presence_of_element_located(elemento))
            WebDriverWait(**self._args_wait).until(visibility_of_element_located(elemento))
            el = WebDriverWait(**self._args_wait).until(element_to_be_clickable(elemento))
            el.clear()  # limpa antes de digitar
            el.send_keys(string)
            self.aguardar()

        except ValueError as e:
            caminho = self._obter_chave_por_valor(self.xpaths, xpath)
            if caminho:
                caminho_str = " > ".join(caminho)
                raise f"Erro: {e}\nMétodo: `digitar_xpath`\nstring: {string}'\nitem: {caminho_str}\n"
            else:
                raise f"Erro: {e}\nMétodo: `digitar_xpath`\nstring: '{string}'\nxpath: {xpath}"

    def aguardar(self):
        elemento = (By.TAG_NAME, 'body')
        WebDriverWait(**self._args_wait).until(presence_of_element_located(elemento))
        WebDriverWait(**self._args_wait).until(visibility_of_element_located(elemento))

    def iterar_turmas(self):
        for série in self._ue.séries:
            self._selecionar_série(série)
            turmas_correspoentes = self._ue.turmas_por_serie[série]
            for turma in turmas_correspoentes:
                self._selecionar_turma(turma)
                yield série, turma


    def _selecionar_turma(self, turma):
        self.__selecionar_opção('composição', valor='199')
        self.__selecionar_opção('turno', valor='1')
        self.__selecionar_opção('turma', texto=turma)

    def _obter_chave_por_valor(self, dicionário: dict, valor_procurado: str, caminho=None):
        if caminho is None:
            caminho = []
        for chave, valor in dicionário.items():
            if isinstance(valor, dict):
                resultado = self._obter_chave_por_valor(valor, valor_procurado, caminho + [chave])
                if resultado:
                    return resultado
            elif valor == valor_procurado:
                return caminho + [chave]
        return None

    def _selecionar_série(self, série):
        self.__selecionar_opção('composição', valor='199')
        self.__selecionar_opção('série', texto=f'{série}º Ano')
        self.__selecionar_opção('turno', valor='1')

    def __selecionar_opção(self, arg, valor=None, texto=None):
        # ids =
        # for chave in chaves:
        #     ids = ids[chave]
        id_element = self._pp.ids[arg]

        elemento: tuple[str, str] = (By.ID, id_element)

        selecionar_elemento = WebDriverWait(**self._args_wait).until(
            presence_of_element_located(elemento)
        )
        selecionar = Select(selecionar_elemento)
        if valor is None and texto is None or valor is not None and texto is not None:
            raise ValueError(f"Nenhum argumento inserido para preenchimento de '{arg}'")
        if valor:
            selecionar.select_by_value(valor)
        if texto:
            selecionar.select_by_visible_text(texto)

    def __getattr__(self, item):
        return getattr(self._master, item)
