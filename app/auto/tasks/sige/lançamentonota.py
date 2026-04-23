from selenium.webdriver import Chrome
from app.auto.data.dataclasses.propriedadesweb import PropriedadesWeb
from app.auto.functions.navegaçãoweb import NavegaçãoWeb
from app.auto.tasks.registrotasks import RegistroTasks
from app.config.parâmetros.estruturadeseleção import EstruturaDeSeleção

@RegistroTasks.registrar('noteador')
class LançadorDeNotas:
    def __init__(
            self,
            navegador: Chrome,
            seleção: EstruturaDeSeleção,
            alvos: list[str],
            **kwargs
    ):
        print(f'Classe LançadorDeNotas instanciada: \n{seleção = }\n{alvos = }')

        self.master = navegador
        self._seleção = seleção

        self._nv = NavegaçãoWeb(navegador, 'sige')
        self._pp = PropriedadesWeb('sige')

        self._logon()
        self._executar(alvos=alvos)

    def _logon(self):
        self.master.get(self._pp.urls)
        self.master.maximize_window()
        self._nv.digitar_xpath('misc', 'input id', string=self._pp.credenciais_padrão.id)
        self._nv.digitar_xpath('misc', 'input senha', string=self._pp.credenciais_padrão.senha)
        self._nv.clicar('xpath', 'misc', 'entrar')
        self._nv.clicar('xpath', 'misc', 'alerta')

    def _executar(self, alvos: list[str]) -> None :
        
        for alvo in alvos :
            print(f'{alvo = }')
            self._preencher_form()

    def _preencher_form(self, função) -> None :
        self._nv.acessar_destino('https://sige.educacao.go.gov.br/sige/modulos/Academico/ave_chamada_cad.asp')

        for série, turma in self._nv.iterar_turmas_sige(self._seleção) :
            função()
            print(f'{série = }, {turma = }')


    def _lançar_notas(self):
        #selecionar disciplina;
        ## as veze demora para a lista de alunos carregar.
        # Veja se isso está sendo cuidado. A demora acontece após seecionar a turma, então devemos esperar isso para então selecionar disciplina, pois o próprio SIGE não cria essa trava
        #marcar bimestre
        #marcar todos '/html/body/div[8]/form/table/tbody/tr[15]/td/table/tbody/tr[1]/td[1]/input'
        #clicar cadastrar (id cmdCadastrar)
        pass

    def _ordenar(self):
        pass

    def _preencher_cargas_horárias(self):
        # self._nv.acessar_destino('https://sige.educacao.go.gov.br/sige/modulos/Academico/Ave_NotasFaltas_cad.asp')
        #selecionar disciplina
        pass



    def _selecionar_bimestre(self, bimestre: int) -> None:
        _bimestres = list(range(1, 5))
        xpath_bimestre = f'/html/body/div[8]/form/table/tbody/tr[11]/td/input[{_bimestres[bimestre]}]'
        self._nv.clicar('xpath livre', xpath_bimestre)


