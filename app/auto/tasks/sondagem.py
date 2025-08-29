import os.path
import shutil
import time
from typing import Callable
from selenium.webdriver import Chrome
import tempfile
import platform
import subprocess
from app.auto.data.sites.propriedades import Propriedades
from app.auto.functions.impressão import Impressão
from app.auto.functions.navegação import Navegação

class Sonagem:

    def __init__(
            self,
            navegador: Chrome,
            destino: str,
    ):
        print(f'class Downloads instanciada.')
        self.master = navegador
        self.destino_comum = destino

        self.nv = Navegação(navegador, 'sige')
        self.pp = Propriedades('sige')

        self.logon()

    def logon(self):
        self.master.get(self.pp.url)
        self.master.maximize_window()
        self.nv.digitar_xpath('misc', 'input id', string=self.pp.credenciais['id'])
        self.nv.digitar_xpath('misc', 'input senha', string=self.pp.credenciais['senha'])
        self.nv.clicar('xpath', 'misc', 'entrar')
        self.nv.clicar('xpath', 'misc', 'alerta')

    def baixar_alvos(self):
        início_geral = time.time()


        print(f'Iniciando downloads de relatórios: {}')

        início_sessão = time.time()

        print(f'Iniciando Downloads {[]}.')

        fim_sessão = time.time()
        print(f'Sessão {0} concluída em {fim_sessão - início_sessão:.3f} segundos')

        fim_geral = time.time()
        print(f'Downloads de relatórios concluído em {fim_geral - início_geral:.3f}')

    def baixar_fichas(self):
        self.nv.caminhar('fichas')
        for série, turma in self.nv.iterar_turmas():
            self.nv.clicar('xpath', 'misc', 'marcar todos')
            self.nv.clicar('id', 'gerar')

    #         self.printar_e_voltar('fichas', turma)
    #
    # def printar_e_voltar(self, tipo, turma):
    #     self._imprimir(tipo, turma)
    #     self.nv.clicar('css', 'voltar')

    # def _imprimir(self, tipo, nome):
    #     temporária = self.abrir_temporária()
    #     try:
    #         Impressão(
    #             navegador=self.master,
    #             pasta_temp=temporária.name,
    #             tipos_para_pastas=self._map_pastas_por_tipo
    #         ).imprimir_e_mover(tipo, nome)
    #     finally:
    #         self.fechar_temporária(temporária)

    # @staticmethod
    # def abrir_temporária():
    #     pasta_temporária = tempfile.TemporaryDirectory(prefix='.temp')
    #     if platform.system() == 'Windows':
    #         subprocess.call(['attrib', '+h', pasta_temporária.name])
    #     return pasta_temporária
    #
    # @staticmethod
    # def fechar_temporária(pasta):
    #     pasta.cleanup()
