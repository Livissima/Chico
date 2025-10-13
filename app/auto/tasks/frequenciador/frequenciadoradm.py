
from selenium.webdriver.common.by import By
from app.auto.data.sites.propriedades import Propriedades
from app.auto.functions.javascript import SCRIPT_MARCAR_FALTA_COMO_ADM, SCRIPT_JUSTIFICAR, SCRIPT_IR_PARA_DATA
from app.auto.functions.navegaçãoweb import NavegaçãoWeb
from selenium.webdriver import Chrome


class FrequenciadorAdm :

    def __init__(
            self,
            navegador: Chrome,
            ausentes_na_data = None,
            **kwargs
    ):
        self.ausentes_na_data = ausentes_na_data
        self.master = navegador
        self.nv = NavegaçãoWeb(navegador, 'siap')
        self.pp = Propriedades(site='siap')
        self._executar()

    def _executar(self):
        self.__acessar_painel_de_frequência()
        turmas = self.nv.obter_turmas_siap()
        for turma in turmas :
            self.nv.clicar('xpath livre', turma)
            nome_turma = self.master.find_element(By.XPATH, turma).text
            self.nv.aguardar_página()
            faltas_marcadas = self.__marcar_falta_individual()
            self.__justificar_falta()
            self.__anunciar_faltas_lançadas(faltas_marcadas, nome_turma)
            self.__avançar_turma()


    def __justificar_falta(self):
        ausentes = list(self.ausentes_na_data.keys())
        return self.master.execute_script(SCRIPT_JUSTIFICAR, ausentes)

    def __trocar_data(self, data_desejada):
        alteração_de_data = self.master.execute_script(SCRIPT_IR_PARA_DATA, data_desejada)
        print(f'{alteração_de_data = }')
        self.nv.aguardar_página()

    def __avançar_turma(self) :
        self.nv.clicar('xpath', 'salvar e próximo')

    def __marcar_falta_individual(self):
        ausentes = list(self.ausentes_na_data.keys())
        return self.master.execute_script(SCRIPT_MARCAR_FALTA_COMO_ADM, ausentes)

    def __resolver_captcha(self) :
        captcha = self.master.find_element(By.XPATH, self.pp.xpaths['captcha'])
        self.nv.digitar_xpath('input captcha', string=captcha.text)

    def __acessar_painel_de_frequência(self) :
        self.nv.clicar('xpath', 'menu sistema')
        self.nv.clicar('xpath', 'menu frequência')

    def __anunciar_faltas_lançadas(self, matrículas_clicadas, nome_turma):
        for matrícula in matrículas_clicadas:
            estudante = self.ausentes_na_data.get(matrícula, 'Não identificado')

            print(f'Falta lançada para: {estudante} - {matrícula}')
        print(f'Faltas lançadas na turma {nome_turma}: {len(matrículas_clicadas)}')
