import time

from pandas import DataFrame
from selenium.common import StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

from app.auto.data.dataclasses.propriedadesweb import PropriedadesWeb
from app.auto.functions.navegaçãoweb import NavegaçãoWeb
from selenium.webdriver import Chrome

from app.config.parâmetros.getters.tempo import tempo

mês = 'Abril'


def retry(self):
    self.master.back()
    time.sleep(3)

def deu_error(erro: str | None) -> bool:
    if not erro:
        return False
    if 'Server Error' in erro:
        return True
    return False



class FrequenciadorProf :

    def __init__(
            self,
            navegador: Chrome,
            ausentes_na_data: DataFrame,
            **kwargs
    ):
        self._ausentes_na_Data = ausentes_na_data
        self.master = navegador
        self.nv = NavegaçãoWeb(navegador, 'siap')
        self.pp = PropriedadesWeb(site='siap')
        self._executar()

    def _executar(self) :
        linhas_resultado = self._obter_linhas_disciplinas()

        for índice_linha in range(len(linhas_resultado)) :
            self._processar_linha(índice_linha, linhas_resultado)


    def _processar_linha(self, índice_linha, linhas) :
        """Processa uma linha específica com tratamento de stale elements"""
        linhas_resultado = None
        tentativas = 0
        while tentativas < 3 :
            try :
                self._block_try_processar_linha(tentativas, linhas, índice_linha, linhas_resultado)
                break

            except StaleElementReferenceException :
                tentativas += 1
                print(f"Tentativa {tentativas} falhou para linha {índice_linha}")
                time.sleep(2)

    def _block_try_processar_linha(self, tentativas: int, linhas, índice_linha, linhas_resultado):
        if tentativas > 0 :
            linhas_resultado = self._obter_linhas_disciplinas()

        if tentativas == 0 :
            linhas_resultado = linhas

        if índice_linha >= len(linhas_resultado) :
            print(f"Índice {índice_linha} fora do range")
            return

        linha_atual = linhas_resultado[índice_linha]
        linha_atual.click()
        time.sleep(1)

        self.nv.clicar('xpath', 'diário', 'frequência')
        print(f'\n → → → em frequência na linha {índice_linha + 1}')

        self._processar_dias_linha(índice_linha)

    def _processar_dias_linha(self, índice_linha) :
        """Processa os dias pendentes de uma linha"""
        self.nv.selecionar_dropdown('xpath', 'diário', 'mês', texto=mês)
        self.nv.aguardar_página(1)

        dias_pendentes = self._obter_calendários_e_dias(índice_linha)

        print(f'Dias pendentes: {[dia.text for dia in dias_pendentes]}')

        if not dias_pendentes :
            print('Nenhum dia pendente encontrado')
            return

        for índice_dia in range(len(dias_pendentes)) :
            self._processar_dia_individual(índice_linha, índice_dia)

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

    def _processar_dia_individual(self, índice_linha, índice_dia) :

        tentativas = 0
        while tentativas < 3 :
            try :

                erro = self._verificar_erro(índice_linha, índice_dia)

                if deu_error(erro):
                    retry(self)
                    tentativas += 1
                    continue


                lista_pacotes_pontinhos = self._obter_lista_pacotes_pontinhos()
                data_pacote = self._obter_data_da_lista(lista_pacotes_pontinhos)

                lista_coluna_pontinhos = self._obter_colunas_pontinhos(lista_pacotes_pontinhos)
                lista_matrículas_ausentes = self._obter_lista_matrículas_ausentes(data_pacote)

                self._agir_nas_colunas(lista_coluna_pontinhos, lista_matrículas_ausentes)

                self.nv.clicar('xpath', 'diário', 'salvar')
                self.nv.aguardar_página(1)
                break

            except StaleElementReferenceException :
                tentativas += 1
                print(f"Tentativa {tentativas} falhou para dia {índice_dia}")
                time.sleep(2)

    def _obter_lista_matrículas_ausentes(self, data):
        _df = self._ausentes_na_Data.copy()
        df_ausentes_na_data = _df[_df['Data'] == data]
        lista_matrículas_ausentes = df_ausentes_na_data['Matrícula'].tolist()
        return lista_matrículas_ausentes

    def __preencher_filtro_de_linhas(self) :
        seletor_tabela_update = (By.ID, 'cphFuncionalidade_UpdatePanel1')

        self.nv.digitar_xpath('diário', 'ano', string=tempo.ano_atual)
        self.nv.clicar('xpath livre', '//*[@id="FormularioPrincipal"]/div[4]/div[2]/div/div[1]/div')  # clicar fora
        self.nv.selecionar_dropdown('xpath', 'diário', 'bimestre', valor='3')
        self.nv.clicar('xpath', 'diário', 'botão listar', elemento_espera=seletor_tabela_update)


    def __acessar_painel_frequência(self) :
        self.nv.clicar('xpath', 'menu sistema')
        self.nv.clicar('xpath', 'diário', '_xpath')


    def _obter_linhas_disciplinas(self):
        seletor_tabela_update = (By.ID, 'cphFuncionalidade_UpdatePanel1')
        self.__acessar_painel_frequência()
        self.__preencher_filtro_de_linhas()
        tabela_linhas = self.master.find_element(*seletor_tabela_update)
        tabela_calendário = tabela_linhas.find_element(By.TAG_NAME, 'tbody')
        linhas_gerais = tabela_calendário.find_elements(By.TAG_NAME, 'tr')
        linhas_resultado = [linha for linha in linhas_gerais if linha.get_attribute('class') != 'topo']

        print(f'Encontradas {len(linhas_resultado)} linhas')
        return linhas_resultado

    def __obter_dias_pendentes(self):
        #todo: Bolar um esqueminha para decidir entre retornar dias_ok, dias_pendentes e _dias, que são todos úteis em contextos diferentes.
        seletor_calendário = (By.ID, 'cphFuncionalidade_cphCampos_CalendarioMensal')
        div_calendário = self.nv.obter_elemento(*seletor_calendário)
        tabela_calendário = div_calendário.find_element(By.TAG_NAME, 'table')
        corpo_tabela = tabela_calendário.find_element(By.TAG_NAME, 'tbody')
        dias = corpo_tabela.find_elements(By.TAG_NAME, 'td')
        dias_relevantes = [dia for dia in dias if dia.get_attribute('data-executado')]
        dias_ok = [dia for dia in dias_relevantes if dia.get_attribute('data-executado') == 'True']
        dias_pendentes = [dia for dia in dias_relevantes if dia.get_attribute('data-executado') == 'False']

        _dias = [dia for dia in dias_relevantes if int(dia.text) <= int(tempo.hoje_dia)]
        print(f'{dias = }')  # dias = [dia for dia in dias_relevantes if ]
        return dias_pendentes


    def _obter_calendários_e_dias(self, índice_linha):
        tentativas = 0
        while tentativas < 4 :
            try:
                return self.__obter_dias_pendentes()

            except Exception as e:
                print(f'Erro na obtenção de calendário. Tentando novamente... {e}')
                tentativas += 1

                if tentativas >= 4:
                    raise Exception('Não deu para obter o calendário.') from e


                linhas = self._obter_linhas_disciplinas()
                self._processar_linha(índice_linha, linhas)

        return None


    def _agir_nas_colunas(self, lista_colunas_pontinhos, ausentes):
        pontos_alvos = self._obter_pontinhos_alvos(lista_colunas_pontinhos, ausentes)
        self._agir_nos_pontos(pontos_alvos)


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
    def _agir_nos_pontos(pontinhos_alvos):
        for ponto_alvo in pontinhos_alvos :
            if ponto_alvo.get_attribute('data-ausente') == 'False':
                ponto_alvo.click()
                time.sleep(0.7)
                print(f'::::::::::: Clicando em {ponto_alvo.get_attribute('data-matricula')}')

            if ponto_alvo.get_attribute('data-ausente') == 'True':
                print(f'::::::::::: O alvo {ponto_alvo.get_attribute('data-matricula')} já estava com falta nesta coluna e foi ignorado.')


    @staticmethod
    def _obter_colunas_pontinhos(lista_pacotes_pontinhos):
        return [pacote.find_element(By.CLASS_NAME, 'itens') for pacote in lista_pacotes_pontinhos]

    def _obter_lista_pacotes_pontinhos(self):
        elemento_maior = self.master.find_element(By.ID, 'cphFuncionalidade_cphCampos_ControleFrequenciaAluno')

        sub_elemento = elemento_maior.find_element(By.CLASS_NAME, 'index-1')
        elemento_empacotador = sub_elemento.find_element(By.CLASS_NAME, 'listaTableWrap')

        return elemento_empacotador.find_elements(By.CLASS_NAME, 'listaDeFrequencias')

    @staticmethod
    def _obter_data_da_lista(lista_pacote: list[WebElement]):
        data_pacote = lista_pacote[0].get_attribute('data-data')
        print(f'{data_pacote = }')
        return data_pacote

    def _obter