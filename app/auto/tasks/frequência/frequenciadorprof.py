import time

from pandas import DataFrame
from selenium.webdriver.common.by import By

from app.auto.data.sites.propriedades import Propriedades
from app.auto.functions.javascript import SCRIPT_MARCAR_FALTA_COMO_ADM
from app.auto.functions.navegaçãoweb import NavegaçãoWeb
from selenium.webdriver import Chrome

from app.config.parâmetros import parâmetros


class FrequenciadorProf :

    def __init__(self, navegador: Chrome, professor, ausentes_na_data: DataFrame, **kwargs) :
        self.__ausentes_na_data = ausentes_na_data
        self.master = navegador
        self.nv = NavegaçãoWeb(navegador, 'siap')
        self.pp = Propriedades(site='siap')
        self._executar(professor)

    def _executar(self, professor) :

        linhas_relevantes = []
        aulas = self.modulação(professor)
        print(f'{aulas = }')
        alvo = (By.XPATH, '/html/body/form/div[4]/div[2]/div/div[1]/div/div[3]/p[2]/select')

        for índice_disciplina, dados_disciplina in aulas :

            self._acessar_painel_frequência()
            self.nv.digitar_xpath('diário', 'ano', string=self.pp.agora.year)
            # self.nv.selecionar_dropdown('diário', 'composição', valor='199')
            # self.nv.selecionar_dropdown('diário', 'série', valor=dados_disciplina['série'], elemento_espera=alvo)
            self.nv.clicar('xpath livre', '//*[@id="FormularioPrincipal"]/div[4]/div[2]/div/div[1]/div')  #clicar fora
            self.nv.selecionar_dropdown('diário', 'bimestre', valor='3')
            # self.nv.selecionar_dropdown('diário', 'turno', valor='1')

            seletor_tabela_update = (By.ID, 'cphFuncionalidade_UpdatePanel1')
            self.nv.clicar('xpath', 'diário', 'botão listar', elemento_espera=seletor_tabela_update)
            time.sleep(5)

            #todo: DEU PROBLEMA A PARTIR DAQUI::::↓↓↓↓↓↓↓↓

            tabela_update = self.master.find_element(*seletor_tabela_update)
            print(f'{tabela_update = }\n')

            tabela_calendário = tabela_update.find_element(By.TAG_NAME, 'tbody')
            print(f'{tabela_calendário = }\n')
            linhas_gerais = tabela_calendário.find_elements(By.TAG_NAME, 'tr')
            print(f'{linhas_gerais = }\n')
            linhas_resultado = [linha for linha in linhas_gerais if linha.get_attribute('class') != 'topo']
            print(f'{linhas_resultado = }\n')

            linhas_relevantes = [linha for linha in linhas_resultado if
                                 not any(palavra in linha.text.split() for palavra in self._núcleo_diversificado)]

            print(f'{len(linhas_relevantes) = }\n')


            self.clicar_linhas_disciplinas(linhas_relevantes)

    def clicar_linhas_disciplinas(self, linhas_relevantes):
        self.nv.aguardar_página()

        for linha in linhas_relevantes :
            # if linha:
            #     print(f'{linha.text = }')
            linha.click()
            time.sleep(3)
            self.nv.clicar('xpath', 'diário', 'frequência')
            print(f'clicado em frequência')

            seletor_calendário = (By.ID, 'cphFuncionalidade_cphCampos_CalendarioMensal')

            div_calendário = self.nv.obter_elemento(*seletor_calendário)
            print(f'{div_calendário = }\n')

            tabela_calendário = div_calendário.find_element(By.TAG_NAME, 'table')
            print(f'{tabela_calendário = }\n')

            corpo_tabela = tabela_calendário.find_element(By.TAG_NAME, 'tbody')
            print(f'{corpo_tabela = }\n')

            dias = corpo_tabela.find_elements(By.TAG_NAME, 'td')
            print(f'{dias = }\n')
            print(f'{len(dias) = }\n')

            dias_relevantes = [dia for dia in dias if dia.get_attribute('data-executado')]
            print(f'{dias_relevantes = }')
            print(f'{len(dias_relevantes) = }\n')

            dias_ok = [dia for dia in dias_relevantes if dia.get_attribute('data-executado') == "True"]
            print(f'{dias_ok = }')
            print(f'{len(dias_ok) = }\n')

            for dia in dias_ok :
                print(f'{dia.text = }')

            dias_pendentes = [dia for dia in dias_relevantes if dia.get_attribute('data-executado') == 'False']

            print(f'{dias_pendentes = }')
            print(f'{len(dias_pendentes) = }\n')
            if len(dias_pendentes) == 0 :
                # todo: navegação de saída.
                self.master.back()
                self.nv.aguardar_página(1)

                print(f'Lista de dias pendentes vazias. Escapando loop.')
                continue



            else: self.clicar_dias_pendentes(dias_pendentes)

    def clicar_dias_pendentes(self, dias_pendentes):

        for dia in dias_pendentes :
            print(f'{dia.text = }')

            self.nv.aguardar_página()
            dia.click()
            self.nv.aguardar_página()

            coluna_pontinhos = self.nv.obter_elemento(By.CLASS_NAME, 'itens')

            pontinhos = coluna_pontinhos.find_elements(By.TAG_NAME, 'div')

            pontinhos_alvos = [ponto for ponto in pontinhos if
                               ponto.get_attribute('data-matricula') in self.ausentes_na_data[
                                   'Matrícula'] and dia.get_attribute('data-canonica') == self.ausentes_na_data[
                                   'Data canonica']]

            self.clicar_faltas(pontinhos_alvos)


    @staticmethod
    def clicar_faltas(pontinhos_alvos):
        for ponto in pontinhos_alvos :
            ponto.click()
            print(f'Clicando em {ponto.get_attribute('data-matricula')}')

        # pontinhos_para_marcar = [  #     ponto for ponto in pontinhos if ponto.get_attribute('data-matrícula') in self.ausentes_na_data[]  # ]
            print('fim!!')
            time.sleep(1000)

    @property
    def _núcleo_diversificado(self) :
        return ['PROTAGONISMO', 'ELETIVAS', 'INICIAÇÃO', 'ESTUDO', 'PRÁTICAS']

    @staticmethod
    def modulação(cpf_prof) :
        print(f'{parâmetros.modulações[cpf_prof]['disciplinas'].items() = }')
        print(f'{parâmetros.modulações[cpf_prof]['disciplinas'] = }')
        return parâmetros.modulações[cpf_prof]['disciplinas'].items()

    def _acessar_painel_frequência(self) :
        self.nv.clicar('xpath', 'menu sistema')
        self.nv.clicar('xpath', 'diário', '_xpath')

    def __marcar_falta_individual(self) :
        ausentes = list(self.__ausentes_na_data.keys())
        return self.master.execute_script(SCRIPT_MARCAR_FALTA_COMO_ADM, ausentes)

    def __anunciar_faltas_lançadas(self, matrículas_clicadas, nome_turma) :
        for matrícula in matrículas_clicadas :
            estudante = self.__ausentes_na_data.get(matrícula, 'Não identificado')
            print(f'Falta lançada para: {estudante} - {matrícula}')
        print(f'Faltas lançadas na turma {nome_turma}: {len(matrículas_clicadas)}')

    @property
    def ausentes_na_data(self) :
        df = self.__ausentes_na_data
        df['Data canonica'] = df['Data Falta'].strftime('%Y%m%d')
        print(f'{df.tail() = }')
        return df

