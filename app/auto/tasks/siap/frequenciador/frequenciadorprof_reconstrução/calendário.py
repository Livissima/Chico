from selenium.webdriver.common.by import By

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from app.auto.tasks.siap.frequenciador.frequenciadorprof import ProcessadorDisciplina
    from app.auto.tasks.siap.frequenciador import LinhasDisciplinas




class Calendário:
    def __init__(
            self,
            # master: Chrome,
            navegação,
            # propriedades,
            # elemento_disciplinas,
            # índice_linha,
            # processador_disciplina: "ProcessadorDisciplina",
            # linhas_disciplinas: "LinhasDisciplinas"

    ) :
        # self._master = master
        self._nv = navegação
        # self.master = master
        # self.pp = propriedades
        # self.nv = navegação
        self.elemento = self._elementar()

    def _elementar(self):
        seletor_calendário = (By.ID, 'cphFuncionalidade_cphCampos_CalendarioMensal')
        div_calendário = self._nv.obter_elemento(*seletor_calendário)
        tabela_calendário = div_calendário.find_element(By.TAG_NAME, 'table')
        corpo_tabela = tabela_calendário.find_element(By.TAG_NAME, 'tbody')
        dias = corpo_tabela.find_elements(By.TAG_NAME, 'td')
        dias_relevantes = [dia for dia in dias if dia.get_attribute('data-executado')]
        dias_ok = [dia for dia in dias_relevantes if dia.get_attribute('data-executado') == 'True']
        dias_pendentes = [dia for dia in dias_relevantes if dia.get_attribute('data-executado') == 'False']

        return dias_relevantes

