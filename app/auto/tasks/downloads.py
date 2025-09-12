import os.path
import time
from typing import Callable
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

        self._baixar_alvos(alvos)
        self.master.quit()

    def _logon(self):
        self.master.get(self.pp.url)
        self.master.maximize_window()
        self.nv.digitar_xpath('misc', 'input id', string=self.pp.credenciais['id'])
        self.nv.digitar_xpath('misc', 'input senha', string=self.pp.credenciais['senha'])
        self.nv.clicar('xpath', 'misc', 'entrar')
        self.nv.clicar('xpath', 'misc', 'alerta')

    def _baixar_alvos(self, sessões):
        início_geral = time.time()

        sessões_dict = {
            'fichas'    : self._baixar_fichas,
            'contatos'  : self._baixar_contatos,
            'situações' : self._baixar_situações,
            'gêneros'   : self._baixar_gêneros
        }

        funções: list[Callable[[], None]] = [sessões_dict[sessão.lower()] for sessão in sessões if sessão.lower() in sessões_dict]

        print(f'Iniciando downloads de relatórios: {sessões}')

        for função in funções:
            início_sessão = time.time()
            sessão = str(função.__name__.split('_')[1]).title()
            print(f'Iniciando Downloads {sessão}.')

            função()

            fim_sessão = time.time()
            print(f'Sessão {sessão} concluída em {fim_sessão - início_sessão:.3f} segundos')

        fim_geral = time.time()
        print(f'Downloads de relatórios concluído em {fim_geral - início_geral:.3f}')

    def _baixar_fichas(self):
        self.nv.caminhar('fichas')
        for série, turma in self.nv._iterar_turmas_sige():
            self.nv.clicar('xpath', 'misc', 'marcar todos')
            self._gerar_obter_sair('fichas', turma)

    def _baixar_contatos(self):
        self.nv.caminhar('contatos')
        for série, turma in self.nv._iterar_turmas_sige():
            self._gerar_obter_sair('contatos', turma)

    def _baixar_situações(self):
        self.nv.caminhar('situações')
        for série, turma in self.nv._iterar_turmas_sige():
            self._gerar_obter_sair('situações', turma)

    def _baixar_gêneros(self):
        self.nv.caminhar('gêneros')
        for série, turma in self.nv._iterar_turmas_sige():
            self.nv.digitar_xpath('misc', 'input data', string=self.pp.hoje)
            self._gerar_obter_sair('gêneros', turma)

    def _gerar_obter_sair(self, tipo, turma):
        self.nv.clicar('id', 'gerar')
        self.nv.gerar_json(turma, self._map_pastas_por_tipo[str(tipo)], tipo)
        self.nv.clicar('css', 'voltar')

    @property
    def _map_pastas_por_tipo(self) -> dict [str, str]:
        #todo dict compre
        return {
            'fichas'    : os.path.join(self.destino, 'fonte', 'Fichas'),
            'contatos'  : os.path.join(self.destino, 'fonte', 'Contatos'),
            'situações' : os.path.join(self.destino, 'fonte', 'Situações'),
            'gêneros'   : os.path.join(self.destino, 'fonte', 'Gêneros')
        }

