from functools import wraps
from typing import Literal

from pandas import DataFrame
from selenium.common import StaleElementReferenceException

from app.auto.data.dataclasses.propriedadesweb import PropriedadesWeb
from app.auto.functions.navegaçãoweb import NavegaçãoWeb
from selenium.webdriver import Chrome

from app.auto.tasks.siap.frequenciador.prof.constantes import *
from app.auto.tasks.siap.frequenciador.prof.funcs import *
from app.config.parâmetros.getters.tempo import tempo






class FrequenciadorProf :

    def __init__(
            self,
            navegador: Chrome,
            ausentes_na_data: DataFrame,
            **kwargs
    ):
        self._ausentes_na_data = ausentes_na_data
        self.master = navegador
        self.nv = NavegaçãoWeb(navegador, 'siap')
        self.pp = PropriedadesWeb(site='siap')
        self._executar()

    @debugar
    def _executar(self) :
        disciplinas_do_usuário = self._obter_linhas_disciplinas()
        print(f'######## Disciplinas: {disciplinas_do_usuário = }')

        for índice_linha in range(len(disciplinas_do_usuário)) :
            self._processar_disciplina(índice_linha, disciplinas_do_usuário)

    @debugar
    def _processar_disciplina(self, índice_linha: int, linhas: list[WebElement]):
        linhas_resultado = []
        tentativas = 0
        linha_atual = None

        while tentativas < 4:
            try:

                if not primeira_tentativa(tentativas):
                    linhas_resultado = self._obter_linhas_disciplinas()
                if primeira_tentativa(tentativas):
                    linhas_resultado = linhas

                if está_fora_do_range(índice_linha, linhas_resultado):
                    print(f"Linha de índice {índice_linha} fora do range. Retornando None")
                    return

                linha_atual = linhas_resultado[índice_linha]

                if linha_atual :
                    linha_atual.click()
                    time.sleep(1)
                    self.nv.clicar('xpath', 'diário', 'frequência')
                    print(f'## Acessando frequência na linha {índice_linha + 1}')
                    self._processar_dias_letivos_da_disciplina(índice_linha)

            except StaleElementReferenceException as e:
                tentativas = cantar_exception(tentativas, 'processar disciplina', e, índice_linha)
            except Exception as e:
                tentativas = cantar_exception(tentativas, 'processar disciplina', e, índice_linha)

    @debugar
    def _processar_dias_letivos_da_disciplina(self, índice_linha) :
        """Processa os dias pendentes de uma linha"""
        self.nv.selecionar_dropdown('xpath', 'diário', 'mês', texto=MÊS)
        self.nv.aguardar_página(1)

        dias_pendentes = self._obter_calendários_e_dias(índice_linha)

        print(f'Dias pendentes: {[dia.text for dia in dias_pendentes]}')

        if not dias_pendentes :
            print('Nenhum dia pendente encontrado')
            return

        for índice_dia in range(len(dias_pendentes)) :
            self._processar_dia(índice_linha, índice_dia)

    @debugar
    def _verificar_erro(self, índice_linha, índice_dia):
        dias_pendentes_atualizados = self._obter_calendários_e_dias(índice_linha)

        if índice_dia >= len(dias_pendentes_atualizados) :
            print(f"Índice de dia {índice_dia} fora do range")
            return None

        dia_atual = dias_pendentes_atualizados[índice_dia]
        print(f'Clicando no dia: {dia_atual.text}')

        self.master.execute_script("arguments[0].click();", dia_atual)
        self.nv.aguardar_página()

        erro = ''
        body = self.master.find_element(By.TAG_NAME, 'body')

        try:
            erro = body.find_element(By.TAG_NAME, 'h1').text

        except Exception as e:
            print(f'Exception em `obter_erro_e_body`:\n{e}')
            pass

        finally:

            return erro

    @debugar
    def _processar_dia(self, índice_linha, índice_dia) :

        tentativas = 0
        while tentativas < 3 :
            try :

                erro = self._verificar_erro(índice_linha, índice_dia)

                if deu_error(erro):
                    voltar(self)
                    tentativas += 1
                    continue


                lista_pacotes_pontinhos = self._obter_lista_pacotes_pontinhos()
                data_pacote = obter_data_da_lista(lista_pacotes_pontinhos)

                lista_coluna_pontinhos = self._obter_colunas_pontinhos(lista_pacotes_pontinhos)
                lista_matrículas_ausentes = obter_lista_matrículas_ausentes(self, data_pacote)

                self._agir_nas_colunas(lista_coluna_pontinhos, lista_matrículas_ausentes)

                self.nv.clicar('xpath', 'diário', 'salvar')
                self.nv.aguardar_página(1)
                break

            except StaleElementReferenceException as e:
                tentativas = cantar_exception(tentativas, 'dia individual', e, índice_dia)

    @debugar
    def _obter_linhas_disciplinas(self, tentativas: int = 3) -> list[WebElement] :
        print(f'Obtendo disciplinas do(a) professor(a)')
        tries = 0
        lista = []

        while tries < tentativas:
            try:
                acessar_painel_frequência(self)
                preencher_filtro_de_linhas(self)
                tabela_linhas = self.master.find_element(*SELETOR_TABELA_UPDATE)
                tabela_calendário = tabela_linhas.find_element(*SELETOR_CORPO_TABELA)
                linhas_gerais = tabela_calendário.find_elements(*SELETOR_LINHAS_GERAIS)
                linhas_resultado = [linha for linha in linhas_gerais if linha.get_attribute('class') != 'topo']

                print(f'\n  → Disciplinas encontradas: {len(linhas_resultado)}\n')
                lista.append(linhas_resultado)
                break


            except StaleElementReferenceException as e:
                tries = cantar_exception(tries, 'obter linhas disciplinas', e)
            except Exception as e:
                tries = cantar_exception(tries, 'obter linhas disciplinas', e)


        return lista

    @debugar
    def _obter_dias_iteráveis(self, escopo: Literal['pendentes', 'prontos', 'todos'] = 'pendentes'):
        div_calendário = self.nv.obter_elemento(*SELETOR_CALENDÁRIO_ITERÁVEIS)
        tabela_calendário = div_calendário.find_element(*SELETOR_TABELA)
        corpo_tabela = tabela_calendário.find_element(*SELETOR_CORPO_TABELA)
        dias = corpo_tabela.find_elements(*SELETOR_TD)
        dias_relevantes = [dia for dia in dias if dia.get_attribute('data-executado')]
        dias_ok = [dia for dia in dias_relevantes if dia.get_attribute('data-executado') == 'True']
        dias_pendentes = [dia for dia in dias_relevantes if dia.get_attribute('data-executado') == 'False']

        _dias = [dia for dia in dias_relevantes if int(dia.text) <= int(tempo.hoje_dia)]
        print(f'{dias = }')

        retorno = {
            'pendentes' : dias_pendentes,
            'prontos' : dias_ok,
            'todos' : _dias
        }

        return retorno[escopo]

    @debugar
    def _obter_calendários_e_dias(self, índice_linha):
        tentativas = 0
        while tentativas < 4 :
            try:
                return self._obter_dias_iteráveis()

            except StaleElementReferenceException as e:
                tentativas += cantar_exception(tentativas, 'calendários e dias', e, índice_linha)

            except Exception as e:
                tentativas += cantar_exception(tentativas, 'calendários e dias', e, índice_linha)

                if tentativas >= 4:
                    raise Exception('Não deu para obter o calendário.') from e


                linhas = self._obter_linhas_disciplinas()
                self._processar_disciplina(índice_linha, linhas)

        return None

    @debugar
    def _agir_nas_colunas(self, lista_colunas_pontinhos, ausentes):
        pontos_alvos = self._obter_pontinhos_alvos(lista_colunas_pontinhos, ausentes)
        self._agir_nos_pontos(pontos_alvos)

    @debugar
    @staticmethod
    def _obter_pontinhos_alvos(lista_colunas_pontinhos, ausentes):
        pontinhos_alvos = []
        for coluna_pontinhos in lista_colunas_pontinhos :

            pontinhos = coluna_pontinhos.find_elements(By.CLASS_NAME, 'item')

            pontinhos_alvos = [
                ponto for ponto in pontinhos if ponto.get_attribute('data-matricula') in ausentes
            ]

            print(f'{len(pontinhos_alvos) = }')

        return pontinhos_alvos

    @staticmethod
    @debugar
    def _agir_nos_pontos(pontinhos_alvos):
        for ponto_alvo in pontinhos_alvos :

            if ponto_alvo.get_attribute('data-ausente') == 'False':
                ponto_alvo.click()
                time.sleep(0.7)
                print(f'::::::::::: Clicando em {ponto_alvo.get_attribute('data-matricula')}')

            if ponto_alvo.get_attribute('data-ausente') == 'True':
                print(f'::::::::::: O alvo {ponto_alvo.get_attribute('data-matricula')} já estava com falta nesta coluna e foi ignorado.')


    @staticmethod
    @debugar
    def _obter_colunas_pontinhos(lista_pacotes_pontinhos):
        return [pacote.find_element(By.CLASS_NAME, 'itens') for pacote in lista_pacotes_pontinhos]
    @debugar
    def _obter_lista_pacotes_pontinhos(self):
        elemento_maior = self.master.find_element(By.ID, 'cphFuncionalidade_cphCampos_ControleFrequenciaAluno')

        sub_elemento = elemento_maior.find_element(By.CLASS_NAME, 'index-1')
        elemento_empacotador = sub_elemento.find_element(By.CLASS_NAME, 'listaTableWrap')

        return elemento_empacotador.find_elements(By.CLASS_NAME, 'listaDeFrequencias')

