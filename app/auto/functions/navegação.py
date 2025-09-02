import json
import os.path
from typing import Literal

from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import presence_of_element_located, visibility_of_element_located, element_to_be_clickable

from app.auto.data.sites.propriedades import Propriedades
from app.auto.data.misc.escola import Escola
from app.ui.config.parâmetros import parâmetros


class Navegação:
    def __init__(
            self,
            master: Chrome,
            site: str
    ):
        self._master = master
        self._pp = Propriedades(site)
        self._ue = Escola()
        self._timeout = 15
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

    def caminhar(self, destino: str):
        # uma recursão seria melhor

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

    def obter_valor(self, *chaves) -> str:
        xpaths = self._pp.xpaths

        for chave in chaves :
            xpaths = xpaths[chave]
        xpath = xpaths

        elemento: tuple[str, str] = (By.XPATH, xpath)

        try:
            WebDriverWait(**self._args_wait).until(presence_of_element_located(elemento))
            WebDriverWait(**self._args_wait).until(visibility_of_element_located(elemento))
            _elemento = WebDriverWait(**self._args_wait).until(element_to_be_clickable(elemento))
            valor = _elemento.text

            self.aguardar()
            return valor

        except ValueError as e:
            caminho = self._obter_chave_por_valor(self.xpaths, xpath)
            if caminho:
                caminho_str = " > ".join(caminho)
                raise f"Erro: {e}\nMétodo: `obter_valor`\nitem: {caminho_str}\n"
            else:
                raise f"Erro: {e}\nMétodo: `obter_valor`\nxpath: {xpath}"

    def obter_tabelas(self, nome_arquivo, pasta_destino):

        # elemento: tuple[str, str] = (By.CLASS_NAME, 'tabela')
        elemento: tuple[str, str] = (By.CSS_SELECTOR, 'table.tabela')

        try:
            WebDriverWait(**self._args_wait).until(presence_of_element_located(elemento))
            WebDriverWait(**self._args_wait).until(visibility_of_element_located(elemento))

            tabelas = self._master.find_elements(*elemento)

            print(f'Localizadas {len(tabelas)} tabelas na página.')

            dados_combinados = []
            cabeçalhos = None

            for índice, tabela in enumerate(tabelas):
                print(f'Tratando tabela {índice+1}...')

                if cabeçalhos is None:
                    cabeçalhos = self.extrair_cabeçalhos(tabela)
                    if not cabeçalhos:
                        print(f'Não foi possível extrair cabeçalhos')
                        continue

                dados_tabela = self.extrair_dados_tabela(tabela, cabeçalhos)
                dados_combinados.extend(dados_tabela)
                print(f'{len(dados_combinados)} linhas extraídas')

            if dados_combinados:
                path_json = os.path.join(pasta_destino, f'{nome_arquivo}.json')
                with open(path_json, 'w', encoding='utf-8') as arquivo:
                    json.dump(dados_combinados, arquivo, ensure_ascii=False, indent=2)
                print(f'Total de {len(dados_combinados)} linhas salvas em {path_json}')
                return True
            else:
                print('nenhum dado extraído')
                return False
        except ValueError as e:
            print(f'Erro ao extrair tabelas: {e}')
            return False

    @staticmethod
    def extrair_cabeçalhos(tabela):

        try:
            cabeçalhos = []

            try:
                thead = tabela.find_element(By.CSS_SELECTOR, 'thead')
                ths = thead.find_elements(By.CSS_SELECTOR, 'th')
                cabeçalhos = [th.text.strip() for th in ths if th.text.strip()]
            except:
                pass

            if not cabeçalhos:
                try:
                    primeira_linha = tabela.find_element(By.CSS_SELECTOR, 'tbody tr')
                    tds = primeira_linha.find_elements(By.CSS_SELECTOR, 'td')
                    cabeçalhos = [td.text.strip() for td in tds if td.text.strip()]
                except:
                    pass

            if not cabeçalhos:
                cabecalhos = [
                    "Matrícula", "Aluno", "Data de Nascimento", "Nome da Mãe",
                    "CPF do Responsável", "Nome do Responsável", "Telefone residencial",
                    "Telefone responsável", "Telefone celular", "E-mail Alternativo",
                    "E-mail Institucional", "E-mail Educacional", "Ponto ID"
                ]


            return cabeçalhos
        except Exception as e:
            print(f'Erro ao extrair cabeçalhos: {e}')

    @staticmethod
    def extrair_dados_tabela(tabela, cabeçalhos):
        dados = []

        try:
            linhas = tabela.find_elements(By.CSS_SELECTOR, 'tbody tr')

            for linha in linhas:
                try:
                    ths = linha.find_elements(By.CSS_SELECTOR, 'th')
                    if ths:
                        continue

                    texto_linha = linha.text.lower()
                    texto_cabeçalhos = ' '.join(cabeçalhos).lower()

                    correspondências = sum(1 for cabeçalho in cabeçalhos if cabeçalho.lower() in texto_linha)
                    if correspondências > 3:
                        continue
                except:
                    pass

                células = linha.find_elements(By.CSS_SELECTOR, 'td')
                if not células:
                    continue

                linha_dados = {}

                for índice, célula in enumerate(células):
                    if índice < len(cabeçalhos):
                        nome_coluna = cabeçalhos[índice]
                        linha_dados[nome_coluna] = célula.text.strip()

                    else:
                        linha_dados[f'Coluna_extra_{índice}'] = célula.text.strip()

                if any(linha_dados.values()):
                    dados.append(linha_dados)

        except Exception as e:
            print(f'Erro ao extrair dados da tabela: {e}')

        return dados

    def aguardar(self):
        elemento = (By.TAG_NAME, 'body')
        WebDriverWait(**self._args_wait).until(presence_of_element_located(elemento))
        WebDriverWait(**self._args_wait).until(visibility_of_element_located(elemento))

    def iterar_turmas(self):
        for série in parâmetros.séries_selecionadas:
            self._selecionar_série(série)
            turmas_correspoentes = parâmetros.turmas_selecionadas_por_série[série]
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

    # def __getattr__(self, item):
    #     return getattr(self._master, item)
