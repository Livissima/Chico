import time

from pandas import DataFrame
from selenium.common import StaleElementReferenceException
from selenium.webdriver.common.by import By

from app.auto.data.sites.propriedades import Propriedades
from app.auto.functions.javascript import SCRIPT_MARCAR_FALTA_COMO_ADM
from app.auto.functions.navegaçãoweb import NavegaçãoWeb
from selenium.webdriver import Chrome

from app.config.parâmetros import parâmetros
from selenium.webdriver.support.ui import Select

class FrequenciadorProf :

    def __init__(self, navegador: Chrome, professor: str, ausentes_na_data: DataFrame, **kwargs) :
        self.__ausentes_na_data = ausentes_na_data
        self.master = navegador
        self.nv = NavegaçãoWeb(navegador, 'siap')
        self.pp = Propriedades(site='siap')
        self._executar()

    def _executar(self) :

        linhas_resultado = self.obter_linhas_disciplinas()
        #
        print(f'Encontradas {len(linhas_resultado)} linhas')

        for índice_linha in range(len(linhas_resultado)) :
            # SEMPRE re-encontrar elementos antes de usar
            self._processar_linha(índice_linha, linhas_resultado)

    def _processar_linha(self, índice_linha, linhas) :
        """Processa uma linha específica com tratamento de stale elements"""
        linhas_resultado = None
        tentativas = 0
        while tentativas < 3 :
            try :
                if tentativas > 0 :
                    linhas_resultado = self.obter_linhas_disciplinas()
                if tentativas == 0:
                    linhas_resultado = linhas

                if índice_linha >= len(linhas_resultado) :
                    print(f"Índice {índice_linha} fora do range")
                    return

                linha_atual = linhas_resultado[índice_linha]
                linha_atual.click()
                time.sleep(1)

                self.nv.clicar('xpath', 'diário', 'frequência')
                print(f'Clicado em frequência na linha {índice_linha + 1}')

                self._processar_dias_linha(índice_linha)
                break

            except StaleElementReferenceException :
                tentativas += 1
                print(f"Tentativa {tentativas} falhou para linha {índice_linha}")
                time.sleep(2)

    def _processar_dias_linha(self, índice_linha) :
        """Processa os dias pendentes de uma linha"""
        self.nv.selecionar_dropdown('diário', 'mês', texto='Setembro')
        self.nv.aguardar_página(1)

        dias_pendentes = self.obter_calendários_e_dias()

        print(f'Dias pendentes: {[dia.text for dia in dias_pendentes]}')

        if not dias_pendentes :
            print('Nenhum dia pendente encontrado')
            return

        for índice_dia in range(len(dias_pendentes)) :
            self._processar_dia_individual(índice_linha, índice_dia)

    def _processar_dia_individual(self, índice_linha, índice_dia) :
        """Processa um dia individual com proteção contra stale elements"""
        tentativas = 0
        while tentativas < 3 :
            try :
                dias_pendentes_atualizados = self.obter_calendários_e_dias()

                if índice_dia >= len(dias_pendentes_atualizados) :
                    print(f"Índice de dia {índice_dia} fora do range")
                    return

                dia_atual = dias_pendentes_atualizados[índice_dia]
                print(f'Clicando no dia: {dia_atual.text}')
                dia_atual.click()
                self.nv.aguardar_página()

                elemento_maior = self.master.find_element(By.ID, 'cphFuncionalidade_cphCampos_ControleFrequenciaAluno')

                sub_elemento = elemento_maior.find_element(By.CLASS_NAME, 'index-1')
                elemento_empacotador = sub_elemento.find_element(By.CLASS_NAME, 'listaTableWrap')

                lista_pacotes_pontinhos = elemento_empacotador.find_elements(By.CLASS_NAME, 'listaDeFrequencias')
                data_pacote = lista_pacotes_pontinhos[0].get_attribute('data-data')
                print(f'{data_pacote = }')

                lista_coluna_pontinhos = [pacote.find_element(By.CLASS_NAME, 'itens') for pacote in
                                          lista_pacotes_pontinhos]


                _df = self.ausentes_na_data.copy()
                df_ausentes_na_data = _df[_df['Data Falta'] == data_pacote]
                print(f'{df_ausentes_na_data = }')
                lista_matrículas_ausentes = df_ausentes_na_data['Matrícula'].tolist()
                print(f'{lista_matrículas_ausentes = }')


                self.agir_colunas(lista_coluna_pontinhos, lista_matrículas_ausentes)

                self.nv.clicar('xpath', 'diário', 'salvar')
                self.nv.aguardar_página(1)
                break

            except StaleElementReferenceException :
                tentativas += 1
                print(f"Tentativa {tentativas} falhou para dia {índice_dia}")
                time.sleep(2)

    # def _voltar_e_selecionar_linha(self, índice_linha) :
    #     """Volta e seleciona a linha novamente"""
    #
    #     linhas_resultado = self.obter_linhas_disciplinas()
    #
    #     if índice_linha < len(linhas_resultado) :
    #         linha_atual = linhas_resultado[índice_linha]
    #         linha_atual.click()
    #         self.nv.clicar('xpath', 'diário', 'frequência')
    #         self.nv.clicar('xpath', 'diário', 'bt mês anterior')
    #         self.nv.aguardar_página()

    def preencher_filtro_de_linhas(self) :
        # self._acessar_painel_frequência()
        self.nv.digitar_xpath('diário', 'ano', string=self.pp.agora.year)
        # self.nv.selecionar_dropdown('diário', 'composição', valor='199')
        # self.nv.selecionar_dropdown('diário', 'série', valor=dados_disciplina['série'], elemento_espera=alvo)
        self.nv.clicar('xpath livre', '//*[@id="FormularioPrincipal"]/div[4]/div[2]/div/div[1]/div')  # clicar fora
        self.nv.selecionar_dropdown('diário', 'bimestre', valor='3')
        # self.nv.selecionar_dropdown('diário', 'turno', valor='1')

        seletor_tabela_update = (By.ID, 'cphFuncionalidade_UpdatePanel1')
        self.nv.clicar('xpath', 'diário', 'botão listar', elemento_espera=seletor_tabela_update)


    # @staticmethod
    # def modulação(cpf_prof) -> dict :
    #     print(f'{parâmetros.modulações[cpf_prof]['disciplinas'].items() = }')
    #     print(f'{parâmetros.modulações[cpf_prof]['disciplinas'] = }')
    #     return parâmetros.modulações[cpf_prof]['disciplinas'].items()

    def _acessar_painel_frequência(self) :
        self.nv.clicar('xpath', 'menu sistema')
        self.nv.clicar('xpath', 'diário', '_xpath')

    @property
    def ausentes_na_data(self) :
        df = self.__ausentes_na_data

        # print(f'{df.tail(1) = }')
        return df

    @property
    def _núcleo_diversificado(self) :
        return ['PROTAGONISMO', 'ELETIVAS', 'INICIAÇÃO', 'ESTUDO', 'PRÁTICAS']

    # def __marcar_falta_individual(self) :
    #     ausentes = list(self.__ausentes_na_data.keys())
    #     return self.master.execute_script(SCRIPT_MARCAR_FALTA_COMO_ADM, ausentes)
    #
    # def __anunciar_faltas_lançadas(self, matrículas_clicadas, nome_turma) :
    #     for matrícula in matrículas_clicadas :
    #         estudante = self.__ausentes_na_data.get(matrícula, 'Não identificado')
    #         print(f'Falta lançada para: {estudante} - {matrícula}')
    #     print(f'Faltas lançadas na turma {nome_turma}: {len(matrículas_clicadas)}')

    def obter_linhas_disciplinas(self):
        seletor_tabela_update = (By.ID, 'cphFuncionalidade_UpdatePanel1')
        self._acessar_painel_frequência()
        self.preencher_filtro_de_linhas()
        tabela_linhas = self.master.find_element(*seletor_tabela_update)
        tabela_calendário = tabela_linhas.find_element(By.TAG_NAME, 'tbody')
        linhas_gerais = tabela_calendário.find_elements(By.TAG_NAME, 'tr')
        linhas_resultado = [linha for linha in linhas_gerais if linha.get_attribute('class') != 'topo']
        return linhas_resultado

    def obter_calendários_e_dias(self):
        seletor_calendário = (By.ID, 'cphFuncionalidade_cphCampos_CalendarioMensal')

        div_calendário = self.nv.obter_elemento(*seletor_calendário)
        # print(f'{div_calendário = }\n')

        tabela_calendário = div_calendário.find_element(By.TAG_NAME, 'table')
        #                     print(f'{tabela_calendário = }\n')

        corpo_tabela = tabela_calendário.find_element(By.TAG_NAME, 'tbody')
        #                     print(f'{corpo_tabela = }\n')

        dias = corpo_tabela.find_elements(By.TAG_NAME, 'td')
        # print(f'{[dia.text for dia in dias] = }\n')
        # print(f'{len(dias) = }\n')

        dias_relevantes = [dia for dia in dias if dia.get_attribute('data-executado')]
        # print(f'{[dia.text for dia in dias_relevantes] = }')
        # print(f'{len(dias_relevantes) = }\n')

        dias_ok = [dia for dia in dias_relevantes if dia.get_attribute('data-executado') == 'True']
        # print(f'{[dia.text for dia in dias_ok] = }')
        # print(f'{len(dias_ok) = }\n')

        # esta é a variável real. Fiz a substituição por dias relevantes para facilitar os testes.
        dias_pendentes = [dia for dia in dias_relevantes if dia.get_attribute('data-executado') == 'False']
        # dias_pendentes = dias_relevantes
        return dias_relevantes


    @staticmethod
    def agir_colunas(lista_colunas_pontinhos, ausentes):
        for coluna_pontinhos in lista_colunas_pontinhos :

            pontinhos = coluna_pontinhos.find_elements(By.CLASS_NAME, 'item')

            print(f'{len(pontinhos) = }')

            print(f'{[ponto.get_attribute('data-matricula') for ponto in pontinhos] = }')

            pontinhos_alvos = [ponto for ponto in pontinhos if
                               ponto.get_attribute('data-matricula') in ausentes]

            print(f'{len(pontinhos_alvos)}')
            print(f'{pontinhos_alvos = }')

            for ponto_alvo in pontinhos_alvos :
                ponto_alvo.click()
                print(f'############ Clicando no pontinho de {ponto_alvo.get_attribute('data-matricula')}')


