import time
from datetime import date

from pandas import DataFrame, Series
from selenium.webdriver.common.by import By
from app.auto.data.sites.propriedades import Propriedades
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
        self._pp = Propriedades(site='siap')
        self._executar()


    def _faltas_do_dia(self, dia) -> list:
        print(f'{dia = }')
        _df = self._relatório_de_ausências
        print(f'{_df = }')
        _df = _df[_df['Data Falta'] == dia]
        # print(f'{df_faltas_do_dia = }')
        matrículas_alvos = _df['Matrícula'].tolist()
        estudantes_alvos = _df['Estudante'].tolist()
        print(f'{estudantes_alvos = }')
        return matrículas_alvos

    def _executar(self):
        self._acessar_painel_de_frequência()

        for dia in self._período:
            self._trocar_data(dia)
            alvos = self._faltas_do_dia(dia)
            self._executar_turmas(alvos)





    def _executar_turmas(self, alvos):

        turmas = self._nv.obter_xpaths_turmas_siap()

        for turma in turmas :
            self._nv.clicar('xpath livre', turma)

            self._nv.aguardar_página()
            faltas_marcadas = self._marcar_falta_individual(alvos)
            print(f'>>>>>>>{faltas_marcadas = }')
            self._justificar_falta(alvos)
            # if not faltas_marcadas :
            #     time.sleep(5)
            self._avançar_turma()

            # nome_turma = self._master.find_element(By.XPATH, turma).text
            # self._anunciar_faltas_lançadas(faltas_marcadas, nome_turma)


    def _justificar_falta(self, _alvos: DataFrame):
        return self._master.execute_script(Javascript.justificar, _alvos)

    def _marcar_falta_individual(self, _alvos):




        return self._master.execute_script(Javascript.lançar_falta_adm, _alvos)



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
