import time

from selenium.webdriver.common.by import By

from app.auto.data.dataclasses.propriedadesweb import PropriedadesWeb
from app.auto.functions import NavegaçãoWeb
from app.auto.tasks.registrotasks import RegistroTasks
from selenium.webdriver import Edge

from app.config.parâmetros.estruturadeseleção import EstruturaDeSeleção

URL_PAINEL_NOTAS = r'https://sige.educacao.go.gov.br/sige/modulos/Academico/Ave_NotasFaltas_cad.asp'
CAIXA_ESCOPO = (By.XPATH, '/html/body/div[8]/form/table/tbody/tr[11]/td')


@RegistroTasks.registrar('coleta notas')
class ColetaNotas:
    def __init__(
            self,
            navegador: Edge,
            seleção: EstruturaDeSeleção,
            **kwargs
    ):
        self.master = navegador
        self._seleção = seleção
        self.nv = NavegaçãoWeb(navegador, 'sige')
        self.pp = PropriedadesWeb('sige')

        self._logon()
        self._executar()

    def _logon(self) -> None:
        self.master.get(self.pp.urls)
        self.master.maximize_window()
        self.nv.digitar_xpath('misc', 'input id', string=self.pp.credenciais_padrão.id)
        self.nv.digitar_xpath('misc', 'input senha', string=self.pp.credenciais_padrão.senha)
        self.nv.clicar('xpath', 'misc', 'entrar')
        self.nv.clicar('xpath', 'misc', 'alerta')

    def _executar(self):
        self.nv.acessar_destino(URL_PAINEL_NOTAS)


        for série, turma in self.nv.iterar_turmas_sige(self._seleção):
            valores_disciplinas, textos_disciplinas = self._obter_disciplinas()

            caixa_escopo = self.master.find_element(*CAIXA_ESCOPO)
            check_boxes = caixa_escopo.find_elements(By.TAG_NAME, 'input')
            for box in check_boxes:
                pass


    def _obter_disciplinas(self) -> tuple[list[str], list[str]]:
        dropdown_disciplinas = self.master.find_element(By.ID, 'cmbDisciplinaQuadro')
        elementos_disciplinas = dropdown_disciplinas.find_elements(By.TAG_NAME, 'option')
        valores_disciplinas = [opção.get_attribute('value') for opção in elementos_disciplinas]
        textos_disciplinas = [opção.text for opção in elementos_disciplinas]
        return valores_disciplinas, textos_disciplinas






