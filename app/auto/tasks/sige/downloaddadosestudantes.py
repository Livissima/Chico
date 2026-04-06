#app/auto/tasks/sige/downloaddadosestudantes.py
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
    def __init__(
            self,
            navegador: Chrome,
            destino: str,
            alvos: list[str],
            seleção: EstruturaDeSeleção,
            **kwargs
    ):
        print(f'class Downloads instanciada.')
        self.master = navegador
        self._destino = destino
        self._alvos = alvos
        self._seleção = seleção

        self._nv = NavegaçãoWeb(navegador, 'sige')
        self._pp = PropriedadesWeb('sige')

        self._logon()
        self._executar(alvos)
        self.master.quit()

    def _logon(self) -> None:
        self.master.get(self._pp.urls)
        self.master.maximize_window()
        self._nv.digitar_xpath('misc', 'input id', string=self._pp.credenciais_padrão.id)
        self._nv.digitar_xpath('misc', 'input senha', string=self._pp.credenciais_padrão.senha)
        self._nv.clicar('xpath', 'misc', 'entrar')
        self._nv.clicar('xpath', 'misc', 'alerta')

    def _executar(self, alvos: list[str]) -> None:
        for alvo in alvos:
            # self._nv.clicar
            self.__baixar_alvo(alvo.lower())

    def __baixar_alvo(self, alvo: str) -> None:
        self._nv.acessar_url(alvo.lower())

        for série, turma in self._nv.iterar_turmas_sige(self._seleção):
            self.__capturar(alvo.lower(), turma)

    def __capturar(self, tipo: str, turma: str) -> None:
        self.__gerar_relatório(tipo)
        self._nv.download_json(turma, self.__mapear_diretório(tipo), tipo)
        self.__voltar()

    def __mapear_diretório(self, tipo: str) -> PathLike:
        return Path(self._destino, 'fonte', tipo.title())

    def __gerar_relatório(self, tipo) -> None:
        if tipo == 'fichas':
            self._nv.clicar('xpath', 'misc', 'marcar todos')
        if tipo == 'gêneros':
            # self.nv.clicar('xpath', 'resumo', 'turmas', 'ativas')
            self._nv.digitar_xpath('lápis docs', 'relatórios', 'acomp. pedagógico', 'input data', string=tempo.hoje)
        self._nv.clicar('id', 'gerar')

    def __voltar(self) -> None:
        self._nv.clicar('css', 'voltar')

