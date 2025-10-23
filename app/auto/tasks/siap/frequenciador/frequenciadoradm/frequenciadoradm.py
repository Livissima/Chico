import time
from datetime import date

from pandas import DataFrame, Series
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select

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
        _df = _df[_df['Data Falta'] == dia]
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

            self._nv.aguardar_página()
            self._marcar_faltas(alvos)
            # print(f'>>>>>>> {faltas_marcadas = }')
            self._justificar_falta(alvos)
            # if not faltas_marcadas :
            # time.sleep(5)
            self._avançar_turma()

            # nome_turma = self._master.find_element(By.XPATH, turma).text
            # self._anunciar_faltas_lançadas(faltas_marcadas, nome_turma)


    def _justificar_falta(self, _alvos: DataFrame):
        coluna_justificativas = self._master.find_element(By.XPATH, '//*[@id="cphFuncionalidade_ControleFrequencia"]/div/div[4]/div[3]/div/div[2]')
        lista_justificativas = coluna_justificativas.find_elements(By.TAG_NAME, 'select')
        for justificativa in lista_justificativas:
            if justificativa.get_attribute('data-matricula') not in _alvos:
                continue

            print(f"Alvo para justificativa localizado localizado: {justificativa.get_attribute('data-matrícula')}")


            print(f'         → →  Justificando no ponto de {justificativa.get_attribute('data-matricula')}')

            (Select(justificativa).select_by_value('1'))




        return self._master.execute_script(Javascript.justificar, _alvos)

    def _marcar_faltas(self, _alvos):
        self._nv.aguardar_página()
        print(f'{len(self._master.find_elements(By.CLASS_NAME, 'itens')) = }')
        coluna_pontinhos = self._master.find_element(By.XPATH, '//*[@id="cphFuncionalidade_ControleFrequencia"]/div/div[4]/div[2]/div/div/div[2]')
        lista_pontinhos = coluna_pontinhos.find_elements(By.CLASS_NAME, 'item')

        for ponto in lista_pontinhos:
            if ponto.get_attribute('data-matricula') not in _alvos:
                continue

            print(f"Alvo localizado: {ponto.get_attribute('data-matrícula')}")
            if ponto.get_attribute('data-ausente') != 'True':
                print(f"Ponto {ponto.get_attribute('data-matricula')} já está com falta e foi ignorado.")

            print(f'     → →  Clicando no ponto de {ponto.get_attribute('data-matricula')}')
            ponto.click()




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
