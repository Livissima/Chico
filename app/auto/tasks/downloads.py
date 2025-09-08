import os.path
import shutil
import time
from os import PathLike
from typing import Callable
from selenium.webdriver import Chrome
import tempfile
import platform
import subprocess
from app.auto.data.sites.propriedades import Propriedades
from app.auto.functions.impressão import Impressão
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
        self.logon()

        self.baixar_alvos(alvos)
        self.master.quit()

    def logon(self):
        self.master.get(self.pp.url)
        self.master.maximize_window()
        self.nv.digitar_xpath('misc', 'input id', string=self.pp.credenciais['id'])
        self.nv.digitar_xpath('misc', 'input senha', string=self.pp.credenciais['senha'])
        self.nv.clicar('xpath', 'misc', 'entrar')
        self.nv.clicar('xpath', 'misc', 'alerta')

    def baixar_alvos(self, sessões):
        início_geral = time.time()

        sessões_dict = {
            'fichas'    : self.baixar_fichas,
            'contatos'  : self.baixar_contatos,
            'situações' : self.baixar_situações,
            'gêneros'   : self.baixar_gêneros
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

    def baixar_fichas(self):
        self.nv.caminhar('fichas')
        for série, turma in self.nv.iterar_turmas():
            self.nv.clicar('xpath', 'misc', 'marcar todos')
            self.nv.clicar('id', 'gerar')
            self._imprimir('fichas', turma)

            self.nv.clicar('css', 'voltar')


    def baixar_contatos(self):
        self.nv.caminhar('contatos')
        for série, turma in self.nv.iterar_turmas():

            self.gerar_obter_sair('contatos', turma)


    def baixar_situações(self):
        self.nv.caminhar('situações')
        for série, turma in self.nv.iterar_turmas():

            self.gerar_obter_sair('situações', turma)

    def baixar_gêneros(self):
        self.nv.caminhar('gêneros')
        for série, turma in self.nv.iterar_turmas():

            self.nv.digitar_xpath('misc', 'input data', string=self.pp.hoje)
            self.gerar_obter_sair('gêneros', turma)


    def gerar_obter_sair(self, tipo, turma):
        self.nv.clicar('id', 'gerar')
        self.nv.obter_tabelas(turma, self._map_pastas_por_tipo[str(tipo)])
        self.nv.clicar('css', 'voltar')

    @property
    def _map_pastas_por_tipo(self) -> dict [str, str]:
        return {
            'fichas'    : os.path.join(self.destino, 'fonte', 'Fichas'),
            'contatos'  : os.path.join(self.destino, 'fonte', 'Contatos'),
            'situações' : os.path.join(self.destino, 'fonte', 'Situações'),
            'gêneros'   : os.path.join(self.destino, 'fonte', 'Gêneros')
        }


    def _imprimir(self, tipo, nome):
        temporária = self.abrir_temporária()
        try:
            Impressão(
                navegador=self.master,
                pasta_temp=temporária.name,
                tipos_para_pastas=self._map_pastas_por_tipo
            ).imprimir_e_mover(tipo, nome)
        finally:
            self.fechar_temporária(temporária)

    @staticmethod
    def abrir_temporária():
        pasta_temporária = tempfile.TemporaryDirectory(prefix='.temp')
        if platform.system() == 'Windows':
            subprocess.call(['attrib', '+h', pasta_temporária.name])
        return pasta_temporária

    @staticmethod
    def fechar_temporária(pasta):
        pasta.cleanup()
