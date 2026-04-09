from os import PathLike
from pathlib import Path
from selenium.webdriver import Chrome
from app.auto.data.sites.propriedadesweb import PropriedadesWeb
from app.auto.functions.navegaçãoweb import NavegaçãoWeb
from app.auto.tasks.taskregistry import TaskRegistry
from app.config.parâmetros.estruturadeseleção import EstruturaDeSeleção
from app.config.parâmetros.getters.tempo import tempo

@TaskRegistry.registrar('downloads')
class DownloadDadosEstudantes:
    #todo: converter isso em algo como BotSige, que armazenará métodos comuns e direcionará rotinas exclusivas.
    # assim, as classes das diferentes tasks de SIGE serão chamadas em métodos do BotSige.
    def __init__(
            self,
            navegador: Chrome,
            destino: str,
            tarefas_sige: list[str],
            seleção: EstruturaDeSeleção,
            **kwargs
    ):
        print(f'class Downloads instanciada.')
        self.master = navegador
        self._destino = destino
        # self._alvos = tarefas_sige
        self._seleção = seleção

        self._nv = NavegaçãoWeb(navegador, 'sige')
        self._pp = PropriedadesWeb('sige')

        self._logon()
        self._executar_conjunto_de_tarefas(tarefas_sige)
        self.master.quit()

    def _logon(self) -> None:
        self.master.get(self._pp.urls)
        self.master.maximize_window()
        self._nv.digitar_xpath('misc', 'input id', string=self._pp.credenciais_padrão.id)
        self._nv.digitar_xpath('misc', 'input senha', string=self._pp.credenciais_padrão.senha)
        self._nv.clicar('xpath', 'misc', 'entrar')
        self._nv.clicar('xpath', 'misc', 'alerta')

    def _executar_conjunto_de_tarefas(self, tarefas: list[str]) -> None:

        for tarefa in tarefas:
            self._nv.acessar_destino(tarefa.lower())
            self._executar_tarefa(tarefa)


    def _avaliar(self, tarefa):
        #selecionar disciplina;
        ## as veze demora para a lista de alunos carregar.
        # Veja se isso está sendo cuidado. A demora acontece após seecionar a turma, então devemos esperar isso para então selecionar disciplina, pois o próprio SIGE não cria essa trava
        #marcar bimestre
        #marcar todos '/html/body/div[8]/form/table/tbody/tr[15]/td/table/tbody/tr[1]/td[1]/input'
        #clicar cadastrar (id cmdCadastrar)
        pass

    def _executar_tarefa(self, tarefa: str) -> None:
        tasks_download = ['Fichas', 'Contatos', 'Situações', 'Gêneros', 'Fotos']
        tasks_avaliação = ['Avaliação']

        for série, turma in self._nv.iterar_turmas_sige(self._seleção):
            if tarefa in tasks_download:
                self._baixar_relatório(tarefa.lower(), turma)
            if tarefa in tasks_avaliação:
                self._avaliar(tarefa)

    def _baixar_relatório(self, tipo: str, turma: str) -> None:
        self.__gerar_relatório(tipo)
        self._nv.download_json(turma, self.__mapear_diretório(tipo), tipo)
        self._retornar()

    def __mapear_diretório(self, tipo: str) -> PathLike:
        return Path(self._destino, 'fonte', tipo.title())

    def __gerar_relatório(self, tipo) -> None:
        if tipo == 'fichas':
            self._nv.clicar('xpath', 'misc', 'marcar todos')
        if tipo == 'gêneros':
            # self.nv.clicar('xpath', 'resumo', 'turmas', 'ativas')
            self._nv.digitar_xpath('lápis docs', 'relatórios', 'acomp. pedagógico', 'input data', string=tempo.hoje)
        self._nv.clicar('id', 'gerar')

    def _retornar(self) -> None:
        self._nv.clicar('css', 'voltar')

