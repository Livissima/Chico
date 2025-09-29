from os import PathLike
from pathlib import Path
from selenium.webdriver import Chrome
from app.auto.data.sites.propriedades import Propriedades
from app.auto.functions.navegaçãoweb import NavegaçãoWeb



class Downloads:

    def __init__(
            self,
            navegador: Chrome,
            destino: str,
            alvos: list[str],
            **kwargs
    ):
        print(f'class Downloads instanciada.')
        self.master = navegador
        self.destino = destino
        self.nv = NavegaçãoWeb(navegador, 'sige')
        self.pp = Propriedades('sige')
        self._logon()

        self._executar(alvos)
        self.master.quit()

    def _logon(self) -> None:
        self.master.get(self.pp.url)
        self.master.maximize_window()
        self.nv.digitar_xpath('misc', 'input id', string=self.pp.credenciais['id'])
        self.nv.digitar_xpath('misc', 'input senha', string=self.pp.credenciais['senha'])
        self.nv.clicar('xpath', 'misc', 'entrar')
        self.nv.clicar('xpath', 'misc', 'alerta')

    def _executar(self, alvos: list[str]) -> None:
        for alvo in alvos:
            self.nv.clicar
            self.__baixar_alvo(alvo.lower())

    def __baixar_alvo(self, alvo: str) -> None:
        self.nv.caminhar(alvo.lower())

        for série, turma in self.nv.iterar_turmas_sige():
            self.__capturar(alvo.lower(), turma)

    def __capturar(self, tipo: str, turma: str) -> None:
        self.__gerar_relatório(tipo)
        self.nv.download_json(turma, self.__mapear_diretório(tipo), tipo)
        self.__voltar()

    def __mapear_diretório(self, tipo: str) -> PathLike:
        return Path(self.destino, 'fonte', tipo.title())

    def __gerar_relatório(self, tipo) -> None:
        if tipo == 'fichas':
            self.nv.clicar('xpath', 'misc', 'marcar todos')
        if tipo == 'gêneros':
            # self.nv.clicar('xpath', 'resumo', 'turmas', 'ativas')
            self.nv.digitar_xpath('resumo', 'turmas', 'input data', string=self.pp.hoje)
        self.nv.clicar('id', 'gerar')

    def __voltar(self) -> None:
        self.nv.clicar('css', 'voltar')

