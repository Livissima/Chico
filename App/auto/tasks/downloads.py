import os.path
import time
from typing import Callable
from selenium.webdriver import Chrome

from App.auto.info.sites.propriedades import Propriedades
from App.auto.functions.impressão import Impressão
from App.auto.functions.navegação import Navegação

class Downloads:

    def __init__(
            self,
            navegador: Chrome,
            pasta_temporária: str,
            pasta_destino_comum: str,
            *alvos
    ):
        print(f'class Downloads instanciada.')
        self.master = navegador
        self.pasta_temporária = pasta_temporária
        self.destino_comum = pasta_destino_comum

        self.nv = Navegação(navegador, 'sige')
        self.pp = Propriedades('sige')

        self.logon()
        self.baixar_alvos(*alvos)

    def logon(self):
        self.master.get(self.pp.url)
        self.master.maximize_window()
        self.nv.digitar_xpath('misc', 'input id', string=self.pp.credenciais['id'])
        self.nv.digitar_xpath('misc', 'input senha', string=self.pp.credenciais['senha'])
        self.nv.clicar('xpath', 'misc', 'entrar')
        self.nv.clicar('xpath', 'misc', 'alerta')

    def baixar_alvos(self, *sessões):
        início_geral = time.time()

        sessões_dict = {
            'fichas'    : self.baixar_fichas,
            'contatos'  : self.baixar_contatos,
            'situações' : self.baixar_situações,
            'gêneros'   : self.baixar_gêneros
        }

        funções: list[Callable[[], None]] = [sessões_dict[sessão] for sessão in sessões if sessão in sessões_dict]

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

            self.printar_e_voltar('fichas', turma)

    def baixar_contatos(self):
        self.nv.caminhar('contatos')
        for série, turma in self.nv.iterar_turmas():
            self.nv.clicar('id', 'gerar')

            self.printar_e_voltar('contatos', turma)

    def baixar_situações(self):
        self.nv.caminhar('situações')
        for série, turma in self.nv.iterar_turmas():
            self.nv.clicar('id', 'gerar')

            self.printar_e_voltar('situações', turma)

    def baixar_gêneros(self):
        self.nv.caminhar('gêneros')
        for série, turma in self.nv.iterar_turmas():
            self.nv.digitar_xpath('misc', 'input data', string=self.pp.hoje)
            self.nv.clicar('id', 'gerar')

            self.printar_e_voltar('gêneros', turma)

    def printar_e_voltar(self, tipo, turma):
        self._imprimir(tipo, turma)
        self.nv.clicar('css', 'voltar')

    @property
    def _map_pastas_por_tipo(self):
        return {
            'fichas' : os.path.join(self.destino_comum, 'Fichas'),
            'contatos' : os.path.join(self.destino_comum, 'Contatos'),
            'situações' : os.path.join(self.destino_comum, 'Situações'),
            'gêneros' : os.path.join(self.destino_comum, 'Gêneros')
        }

    def _imprimir(self, tipo, nome):
        Impressão(
            self.master,
            self.pasta_temporária,
            self._map_pastas_por_tipo
        ).imprimir_e_mover(tipo, nome)
