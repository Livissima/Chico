import json
import os.path
import time
from typing import Literal
from selenium.common import ElementClickInterceptedException, StaleElementReferenceException
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import presence_of_element_located, visibility_of_element_located, \
    element_to_be_clickable

from app.auto.data.sites.propriedades import Propriedades
# from app.auto.data.misc.escola import Escola
from app.config.parâmetros import parâmetros


class Navegação :
    def __init__(self, master: Chrome, site: str) :
        self.master = master
        self._pp = Propriedades(site)
        self._timeout = 15
        self._args_wait = {'driver' : self.master, 'timeout' : self._timeout}

    def clicar(self, by: Literal['xpath', 'id', 'css', 'css livre', 'xpath livre', 'id livre'] = 'xpath', *chaves: str) :
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
            elemento_web = WebDriverWait(**self._args_wait).until(presence_of_element_located(elemento))

            self.master.execute_script(
                "arguments[0].scrollIntoView({block: 'center', behavior: 'smooth'});",
                elemento_web
            )

            WebDriverWait(**self._args_wait).until(visibility_of_element_located(elemento))
            WebDriverWait(**self._args_wait).until(element_to_be_clickable(elemento)).click()

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
                print(f"Clique via JavaScript em: {str(*chaves[-1 :])}")
                self.aguardar_página()
            except Exception as js_error :
                raise f"Falha no clique via JavaScript: {js_error}"

    def caminhar(self, destino: str) :
        # uma recursão seria melhor

        print(f'    Caminhando para {destino}')
        destinos = self._pp.caminhos
        for tupla in destinos[destino] :
            # print('Click em: ', end='')
            # print(f'{str(tupla[-1:])}', end=', ')
            self.clicar('xpath', *tupla)

    def digitar_xpath(self, *chaves, string: str) :
        xpaths = self._pp.xpaths

        for chave in chaves :
            xpaths = xpaths[chave]
        xpath = xpaths

        elemento: tuple[str, str] = (By.XPATH, xpath)

        try :
            WebDriverWait(**self._args_wait).until(presence_of_element_located(elemento))
            WebDriverWait(**self._args_wait).until(visibility_of_element_located(elemento))
            el = WebDriverWait(**self._args_wait).until(element_to_be_clickable(elemento))
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
            WebDriverWait(**self._args_wait).until(presence_of_element_located(elemento))
            WebDriverWait(**self._args_wait).until(visibility_of_element_located(elemento))
            _elemento = WebDriverWait(**self._args_wait).until(element_to_be_clickable(elemento))
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

    def aguardar_página(self, tempo: float | None = None) :
        elemento = (By.TAG_NAME, 'body')
        WebDriverWait(**self._args_wait).until(presence_of_element_located(elemento))
        WebDriverWait(**self._args_wait).until(visibility_of_element_located(elemento))
        if tempo:
            time.sleep(tempo)

    def aguardar_preenchimento(self, elemento: str) :
        def _predicate(driver) :
            try :
                elem = driver.find_element(By.ID, elemento)
                value = elem.get_attribute("value")
                return value.strip() != ""
            except StaleElementReferenceException:
                return False

        WebDriverWait(**self._args_wait).until(_predicate)

    def gerar_json(self, nome_arquivo, pasta_destino, tipo: Literal['fichas', 'contatos', 'gêneros', 'situações']) :
        tipos = ['contatos', 'gêneros', 'situações']
        inicio = time.time()
        dados = {}
        # try :
        if tipo == 'fichas':
            dados = self.obter_fichas()
        if tipo in tipos:
            dados = self.obter_tabelas()

        # except Exception as e:
        #     print(f'Erro na extração de dados do {nome_arquivo}, {tipo}: {e}')

        if dados :
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

            # Fallback
        # return self._obter_tabelas_fallback(nome_arquivo, pasta_destino)

    def obter_tabelas(self):
        elemento = (By.CSS_SELECTOR, 'table.tabela')
        WebDriverWait(**self._args_wait).until(presence_of_element_located(elemento))

        script = """
                        function extrairTabelas() {
                            var tabelas = document.querySelectorAll('table.tabela');
                            var resultados = [];

                            for (var i = 0; i < tabelas.length; i++) {
                                var tabela = tabelas[i];
                                var dados = [];
                                var cabecalhos = [];

                                // Extrair cabeçalhos
                                var ths = tabela.querySelectorAll('thead th');
                                if (ths.length > 0) {
                                    for (var h = 0; h < ths.length; h++) {
                                        cabecalhos.push(ths[h].innerText.trim());
                                    }
                                } else {
                                    // Tentar primeira linha como cabeçalho
                                    var primeiraLinha = tabela.querySelector('tbody tr');
                                    if (primeiraLinha) {
                                        var cells = primeiraLinha.querySelectorAll('td, th');
                                        for (var h = 0; h < cells.length; h++) {
                                            cabecalhos.push(cells[h].innerText.trim());
                                        }
                                    }
                                }

                                // Se ainda não tem cabeçalhos, usa padrão
                                if (cabecalhos.length === 0) {
                                    cabecalhos = [
                                        "Matrícula", "Aluno", "Data de Nascimento", "Nome da Mãe",
                                        "CPF do Responsável", "Nome do Responsável", "Telefone residencial",
                                        "Telefone responsável", "Telefone celular", "E-mail Alternativo",
                                        "E-mail Institucional", "E-mail Educacional", "Ponto ID"
                                    ];
                                }

                                // Extrair dados
                                var linhas = tabela.querySelectorAll('tbody tr');
                                for (var r = 0; r < linhas.length; r++) {
                                    var linha = linhas[r];

                                    // Pular linhas que parecem ser cabeçalhos
                                    if (linha.querySelectorAll('th').length > 0) continue;

                                    var celulas = linha.querySelectorAll('td');
                                    var linhaDados = {};

                                    for (var c = 0; c < celulas.length; c++) {
                                        var nomeColuna = cabecalhos[c] || 'coluna_' + c;
                                        linhaDados[nomeColuna] = celulas[c].innerText.trim();
                                    }

                                    // Só adiciona se tiver dados
                                    if (Object.keys(linhaDados).length > 0) {
                                        dados.push(linhaDados);
                                    }
                                }

                                resultados.push(...dados);
                            }

                            return resultados;
                        }

                        return extrairTabelas();
                        """  # SCRIPT FEITO PELO DEEPSEEK

        dados = self.master.execute_script(script)
        return dados


    def obter_fichas(self):
        tag_body = self.master.find_element(By.TAG_NAME, 'body')
        tag_table = tag_body.find_elements(By.TAG_NAME, 'table')
        páginas = [pag for pag in tag_table if pag.get_attribute('height') == '60%']

        linhas_web = []
        for página in páginas:
            página.find_elements(By.TAG_NAME, 'tr')
            linhas_web.append(página.text)

        dict_da_turma = dict(enumerate(linhas_web))
        print(dict_da_turma)
        return dict_da_turma

    def obter_turmas_siap(self) -> list[str]:
        elementos = self.master.find_elements(By.CSS_SELECTOR, '.listaTurmas.dentroPrazo')
        lista_css = []
        for índice, elemento in enumerate(elementos, start=2) :
            css_elemento = f'#cphFuncionalidade_ControleFrequencia > div > div.containerTurmaTurno > div:nth-child({índice})'
            lista_css.append(css_elemento)
        return lista_css

    def _obter_tabelas_fallback(self, nome_arquivo, pasta_destino) :
        #Fallback
        elemento = (By.CSS_SELECTOR, 'table.tabela')

        try :
            WebDriverWait(**self._args_wait).until(presence_of_element_located(elemento))
            WebDriverWait(**self._args_wait).until(visibility_of_element_located(elemento))

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

    def _iterar_turmas_sige(self) :
        for série in parâmetros.séries_selecionadas :
            self._selecionar_série(série)
            turmas_correspoentes = parâmetros.turmas_selecionadas_por_série[série]
            for turma in turmas_correspoentes :
                self._selecionar_turma_sige(turma)
                yield série, turma

    def _selecionar_turma_sige(self, turma) :
        self._selecionar_opção('composição', valor='199')
        self._selecionar_opção('turno', valor='1')
        self._selecionar_opção('turma', texto=turma)

    def _selecionar_série(self, série) :
        self._selecionar_opção('composição', valor='199')
        self._selecionar_opção('série', texto=f'{série}º Ano')
        self._selecionar_opção('turno', valor='1')

    def _selecionar_opção(self, arg, valor=None, texto=None) :
        id_element = self._pp.ids[arg]

        elemento: tuple[str, str] = (By.ID, id_element)

        selecionar_elemento = WebDriverWait(**self._args_wait).until(presence_of_element_located(elemento))
        selecionar = Select(selecionar_elemento)
        if valor is None and texto is None or valor is not None and texto is not None :
            raise ValueError(f"Nenhum argumento inserido para preenchimento de '{arg}'")
        if valor :
            selecionar.select_by_value(valor)
        if texto :
            selecionar.select_by_visible_text(texto)

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