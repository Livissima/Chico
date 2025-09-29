import json
import os.path
import time
from typing import Literal, Generator, Any
from selenium.common import ElementClickInterceptedException, StaleElementReferenceException
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import presence_of_element_located, visibility_of_element_located, \
    element_to_be_clickable

from app.auto.data.sites.propriedades import Propriedades
from app.auto.functions.javascript import SCRIPT_OBTER_TABELAS_SIMPLES, SCRIPT_OBTER_TABELAS_FICHAS
from app.config.parâmetros import parâmetros


class NavegaçãoWeb :
    #todo distribuir responsabilidades para sub módulos

    def __init__(self, master: Chrome, site: str) :
        self.master = master
        self._pp = Propriedades(site)
        self.__timeout = 15
        self.__args_wait = {'driver' : self.master, 'timeout' : self.__timeout}

    def clicar(self, by: Literal['xpath', 'id', 'css', 'css livre', 'xpath livre', 'id livre'] = 'xpath', *chaves: str) -> None :
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
        # uma recursão seria melhor

        print(f'    Caminhando para {destino}')
        destinos = self._pp.caminhos
        for tupla in destinos[destino] :

            self.clicar('xpath', *tupla)

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
            caminho = self.__obter_chave_por_valor(self.xpaths, xpath)
            if caminho :
                caminho_str = " > ".join(caminho)
                raise f"Erro: {e}\nMétodo: `digitar_xpath`\nstring: {string}'\nitem: {caminho_str}\n"
            else :
                raise f"Erro: {e}\nMétodo: `digitar_xpath`\nstring: '{string}'\nxpath: {xpath}"

    def obter_valor(self, *chaves) -> str :
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

    def iterar_turmas_sige(self) -> Generator[tuple[Any, Any], Any, None]:
        for série in parâmetros.séries_selecionadas :
            self._selecionar_série(série)
            turmas_correspoentes = parâmetros.turmas_selecionadas_por_série[série]
            for turma in turmas_correspoentes :
                self._selecionar_turma_sige(turma)
                yield série, turma

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

    def __obter_tabelas(self, tipo: str) -> list[str] | list[dict[str, str]]:
        tipos_simples = {'contatos', 'situações', 'gêneros'}
        script = """"""

        if tipo in tipos_simples :
            elemento = (By.CSS_SELECTOR, 'table.tabela')
            WebDriverWait(**self.__args_wait).until(presence_of_element_located(elemento))
            script = SCRIPT_OBTER_TABELAS_SIMPLES

        if tipo == 'fichas' :
            script = SCRIPT_OBTER_TABELAS_FICHAS

        dados = self.master.execute_script(script)
        return dados

    def _obter_tabelas_fallback(self, nome_arquivo, pasta_destino) -> bool:
        #Fallback
        elemento = (By.CSS_SELECTOR, 'table.tabela')

        try :
            WebDriverWait(**self.__args_wait).until(presence_of_element_located(elemento))
            WebDriverWait(**self.__args_wait).until(visibility_of_element_located(elemento))

            tabelas = self.master.find_elements(*elemento)
            print(f'Localizadas {len(tabelas)} tabelas na página.')

            dados_combinados = []
            cabeçalhos = None

            for índice, tabela in enumerate(tabelas) :
                print(f'Tratando tabela {índice + 1}...')

                if cabeçalhos is None :
                    cabeçalhos = self.__extrair_cabeçalhos(tabela)
                    if not cabeçalhos :
                        print(f'Não foi possível extrair cabeçalhos')
                        continue

                dados_tabela = self.__extrair_dados_tabela(tabela, cabeçalhos)
                dados_combinados.extend(dados_tabela)
                print(f'{len(dados_combinados)} linhas extraídas')

            if dados_combinados :
                path_json = os.path.join(pasta_destino, f'{nome_arquivo}.json')
                with open(path_json, 'w', encoding='utf-8') as arquivo :
                    json.dump(dados_combinados, arquivo, ensure_ascii=False, indent=2)
                print(f'Total de {len(dados_combinados)} linhas salvas em {path_json}')
                return True
            else :
                print('nenhum dado extraído')
                return False
        except Exception as e :
            print(f'Erro ao extrair tabelas (fallback): {e}')
            return False

    def _selecionar_turma_sige(self, turma) -> None :
        self._selecionar_opção('composição', valor='199')
        self._selecionar_opção('turno', valor='1')
        self._selecionar_opção('turma', texto=turma)

    def _selecionar_série(self, série) -> None :
        self._selecionar_opção('composição', valor='199')
        self._selecionar_opção('série', texto=f'{série}º Ano')
        self._selecionar_opção('turno', valor='1')

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
    def __extrair_cabeçalhos(tabela) :
        try :
            cabeçalhos = []

            try :
                thead = tabela.find_element(By.CSS_SELECTOR, 'thead')
                ths = thead.find_elements(By.CSS_SELECTOR, 'th')
                cabeçalhos = [th.text.strip() for th in ths if th.text.strip()]
            except :
                pass

            if not cabeçalhos :
                try :
                    primeira_linha = tabela.find_element(By.CSS_SELECTOR, 'tbody tr')
                    tds = primeira_linha.find_elements(By.CSS_SELECTOR, 'td')
                    cabeçalhos = [td.text.strip() for td in tds if td.text.strip()]
                except :
                    pass

            if not cabeçalhos :
                cabeçalhos = ["Matrícula", "Aluno", "Data de Nascimento", "Nome da Mãe", "CPF do Responsável",
                              "Nome do Responsável", "Telefone residencial", "Telefone responsável", "Telefone celular",
                              "E-mail Alternativo", "E-mail Institucional", "E-mail Educacional", "Ponto ID"]

            return cabeçalhos
        except Exception as e :
            print(f'Erro ao extrair cabeçalhos: {e}')
            return None

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
