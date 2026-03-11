import time
from datetime import date

from pandas import DataFrame, Series
from selenium.webdriver.common.by import By
from selenium.webdriver.support.expected_conditions import presence_of_element_located
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait

from app.auto.data.sites.propriedadesweb import PropriedadesWeb
from app.auto.functions.javascript import Javascript
from app.auto.functions.navegaçãoweb import NavegaçãoWeb
from selenium.webdriver import Chrome


class FrequenciadorAdm :
    #todo: utilizar o tipo Período

    def __init__(
            self,
            navegador: Chrome,
            período: list[str],
            relatório_de_ausências: DataFrame = None,
            **kwargs
    ):
        # print(f'{período = }')
        self._período = período
        self._relatório_de_ausências = relatório_de_ausências
        self._master = navegador
        self._nv = NavegaçãoWeb(navegador, 'siap')
        self._pp = PropriedadesWeb(site='siap')
        self._executar()


    def _faltas_do_dia(self, dia) -> list:
        print(f'{dia = }')
        _df = self._relatório_de_ausências
        print(f'{_df = }')
        _df = _df[_df['Data'] == dia]
        # print(f'{df_faltas_do_dia = }')
        matrículas_alvos = _df['Matrícula'].tolist()
        estudantes_alvos = _df['Estudante'].tolist()
        print(f'{matrículas_alvos = }')
        print(f'{estudantes_alvos = }')
        return matrículas_alvos

    def _executar(self):

        for dia in self._período:
            print(f'{dia = }')
            self._acessar_painel_de_frequência()
            self._trocar_data(dia)
            alvos = self._faltas_do_dia(dia)
            print(f'{alvos}')
            self._executar_turmas(alvos)





    def _executar_turmas(self, alvos):

        turmas = self._nv.obter_xpaths_turmas_siap()

        for turma in turmas :
            self._nv.clicar('xpath livre', turma)
            nome_turma = self._master.find_element(By.XPATH, turma).text
            print(f'Processando turma {nome_turma}')

            self._nv.aguardar_página()
            faltas_lançadas = self._marcar_faltas(alvos)
            print(f'>>>>>>> Faltas lançadas na turma {nome_turma}:\n{faltas_lançadas}\n')


            self._justificar_falta(alvos)

            print('Avançando para a próxima turma.')
            self._avançar_turma()

    def _marcar_faltas(self, _alvos):
        self._nv.aguardar_página()
        coluna_pontinhos = self._master.find_element(By.XPATH, '//*[@id="cphFuncionalidade_ControleFrequencia"]/div/div[4]/div[2]/div/div/div[2]')
        lista_pontinhos = coluna_pontinhos.find_elements(By.CLASS_NAME, 'item')
        alvos_atingidos = []

        for ponto in lista_pontinhos:
            if ponto.get_attribute('data-matricula') not in _alvos:
                continue

            print(f"Alvo localizado: {ponto.get_attribute('data-matricula')}")

            if ponto.get_attribute('data-ausente') == 'True':
                print(f"Ponto {ponto.get_attribute('data-matricula')} já está com falta e foi ignorado.")
                continue


            print(f'     → →  Clicando no ponto de {ponto.get_attribute('data-matricula')}')
            ponto.click()
            alvos_atingidos.append(ponto.get_attribute('data-matricula'))

        return alvos_atingidos

    def _justificar_falta(self, _alvos: list) :
        coluna_justificativas = self._master.find_element(By.XPATH, '//*[@id="cphFuncionalidade_ControleFrequencia"]/div/div[4]/div[3]/div/div[2]')
        lista_elementos = coluna_justificativas.find_elements(By.TAG_NAME, 'select')

        lista_xpaths = []
        for índice, _ in enumerate(lista_elementos) :
            xpath = f'//*[@id="cphFuncionalidade_ControleFrequencia"]/div/div[4]/div[3]/div/div[2]/div[{índice + 1}]/select'
            lista_xpaths.append(xpath)

        dicionário = dict(zip(lista_xpaths, lista_elementos))


        for xpath, elemento in dicionário.items() :

            if elemento.get_attribute('data-matricula') not in _alvos :
                continue

            print(f"Alvo para justificativa localizado localizado: {elemento.get_attribute('data-matricula')}")
            print(f' → →  Justificando no ponto de {elemento.get_attribute('data-matricula')}')

            self._nv.selecionar_dropdown('xpath livre', xpath, valor='1')

    def _trocar_data(self, data_desejada):
        alteração_de_data = self._master.execute_script(Javascript.ir_para_data, data_desejada)
        print(f'{alteração_de_data = }')
        self._nv.aguardar_página()

    def _avançar_turma(self) :
        self._nv.clicar('xpath', 'salvar e próximo')



    def _resolver_captcha(self) :
        captcha = self._master.find_element(By.XPATH, self._pp.xpaths['captcha'])
        self._nv.digitar_xpath('input captcha', string=captcha.text)

    def _acessar_painel_de_frequência(self) :
        self._nv.clicar('xpath', 'menu sistema')
        self._nv.clicar('xpath', 'menu frequência')

    # def _anunciar_faltas_lançadas(self, matrículas_clicadas, nome_turma):
    #     for matrícula in matrículas_clicadas:
    #         estudante = self._relatório_de_ausências.get(matrícula, 'Não identificado')
    #
    #         print(f'Falta lançada para: {estudante} - {matrícula}')
    #     print(f'Faltas lançadas na turma {nome_turma}: {len(matrículas_clicadas)}')
