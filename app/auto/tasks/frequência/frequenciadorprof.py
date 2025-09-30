import time

from selenium.webdriver.common.by import By

from app.auto.data.sites.propriedades import Propriedades
from app.auto.functions.javascript import SCRIPT_MARCAR_FALTA_COMO_ADM
from app.auto.functions.navegaçãoweb import NavegaçãoWeb
from selenium.webdriver import Chrome

from app.config.parâmetros import parâmetros


class FrequenciadorProf :

    def __init__(
            self,
            navegador: Chrome,
            professor,
            ausentes_na_data = None,
            **kwargs
    ):
        self.ausentes_na_data = ausentes_na_data
        # self.professor = professor
        self.master = navegador
        self.nv = NavegaçãoWeb(navegador, 'siap')
        self.pp = Propriedades(site='siap')
        self._executar(professor)


    def _executar(self, professor):
        aulas = self.modulação(professor)
        print(f'{aulas = }')
        alvo = (By.XPATH, '/html/body/form/div[4]/div[2]/div/div[1]/div/div[3]/p[2]/select')
        for índice_disciplina, dados_disciplina in aulas:

            self._acessar_painel_frequência()
            self.nv.digitar_xpath('diário', 'ano', string=self.pp.agora.year)
            # self.nv.selecionar_dropdown('diário', 'composição', valor='199')
            # self.nv.selecionar_dropdown('diário', 'série', valor=dados_disciplina['série'], elemento_espera=alvo)
            self.nv.clicar('xpath livre', '//*[@id="FormularioPrincipal"]/div[4]/div[2]/div/div[1]/div')
            self.nv.selecionar_dropdown('diário', 'bimestre', valor='3')
            self.nv.selecionar_dropdown('diário', 'turno', valor='1')
            self.nv.clicar('xpath', 'diário', 'botão listar')
            # self.nv.selecionar_dropdown('diário', 'disciplina')

            time.sleep(1000)

        self.master.quit()

    @staticmethod
    def modulação(cpf_prof):
        print(f'{parâmetros.modulações[cpf_prof]['disciplinas'].items() = }')
        print(f'{parâmetros.modulações[cpf_prof]['disciplinas'] = }')
        return parâmetros.modulações[cpf_prof]['disciplinas'].items()


    def _acessar_painel_frequência(self) :
        self.nv.clicar('xpath', 'menu sistema')
        self.nv.clicar('xpath', 'diário', '_xpath')


    def __marcar_falta_individual(self):
        ausentes = list(self.ausentes_na_data.keys())
        return self.master.execute_script(SCRIPT_MARCAR_FALTA_COMO_ADM, ausentes)


    def __anunciar_faltas_lançadas(self, matrículas_clicadas, nome_turma):
        for matrícula in matrículas_clicadas:
            estudante = self.ausentes_na_data.get(matrícula, 'Não identificado')
            print(f'Falta lançada para: {estudante} - {matrícula}')
        print(f'Faltas lançadas na turma {nome_turma}: {len(matrículas_clicadas)}')







    def __ir_para_data(self, data_desejada):
        raise NotImplemented
