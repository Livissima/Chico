from os import PathLike
from pathlib import Path
from selenium.webdriver import Chrome
from app.auto.data.sites.propriedades import Propriedades
from app.auto.functions.navegação import Navegação



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
        self.nv = Navegação(navegador, 'sige')
        self.pp = Propriedades('sige')
        self._logon()

        self.executar(alvos)
        self.master.quit()

    def _logon(self):
        self.master.get(self.pp.url)
        self.master.maximize_window()
        self.nv.digitar_xpath('misc', 'input id', string=self.pp.credenciais['id'])
        self.nv.digitar_xpath('misc', 'input senha', string=self.pp.credenciais['senha'])
        self.nv.clicar('xpath', 'misc', 'entrar')
        self.nv.clicar('xpath', 'misc', 'alerta')

    def executar(self, alvos):
        for alvo in alvos:
            self.nv.clicar
            self._baixar_alvo(alvo.lower())

    def _baixar_alvo(self, alvo):
        self.nv.caminhar(alvo.lower())

        for série, turma in self.nv.iterar_turmas_sige():
            self._gerar_obter_sair(alvo.lower(), turma)

    def _gerar_obter_sair(self, tipo, turma):
        self.__clicar_gerar(tipo)
        self.nv.gerar_json(turma, self._mapear_diretório(tipo), tipo)
        self.__voltar()

    def _mapear_diretório(self, tipo: str) -> PathLike:
        return Path(self.destino, 'fonte', tipo.title())

    def __clicar_gerar(self, tipo):
        if tipo == 'fichas':
            self.nv.clicar('xpath', 'misc', 'marcar todos')
        if tipo == 'gêneros':
            self.nv.clicar('xpath', 'resumo', 'turmas', 'ativas')
            self.nv.digitar_xpath('resumo', 'turmas', 'input data', string=self.pp.hoje)
        self.nv.clicar('id', 'gerar')

    def __voltar(self):
        self.nv.clicar('css', 'voltar')

