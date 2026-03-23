from typing import Literal

from app.ui.registry import RegistroTelas
from app.ui.screens.tela_estatísticas import TelaEstatísticas
from app.ui.screens.tela_frequência import Frequência
from app.ui.screens.telas_bot.tela_bot_inicial import TelaBot
from app.ui.screens.telas_bot.tela_bot_credenciais import TelaBotCredenciais
from app.ui.screens.telas_bot.tela_bot_servidores import TelaBotServidores
from app.ui.screens.telas_bot.tela_bot_siap import TelaBotSiap
from app.ui.screens.telas_bot.tela_bot_sige import TelaBotSige
from app.ui.screens.tela_consulta import TelaConsulta
from app.ui.screens.tela_inicial import TelaInicial
import importlib
import pkgutil
from app.ui import screens
from app.ui.widgets import Texto, Botão


# from tests.consulta import fonte


class AlternadorDeTelas:
    def __init__(self, container, controller):
        self.container = container
        self.controller = controller
        self.histórico = []
        self.tela_atual = None
        self._carregar_telas()

        self._carregar_telas()

    @staticmethod
    def _carregar_telas():
        if not RegistroTelas.TELA_REGISTRY:
            for loader, module_name, ispkg in pkgutil.walk_packages(screens.__path__, screens.__name__ + "."):
                importlib.import_module(module_name)

    def abrir(self, nome_tela: str, salvar_no_histórico: bool = True):
        if nome_tela not in RegistroTelas.TELA_REGISTRY:
            raise ValueError(f"Tela '{nome_tela}' não encontrada.")

        if salvar_no_histórico and self.tela_atual:
            self.histórico.append(self.tela_atual)

        self.tela_atual = nome_tela

        if self.container.winfo_children():
            for widget in self.container.winfo_children():
                if hasattr(widget, 'salvar_estado'):
                    widget.salvar_estado()
                widget.destroy()

        dados = RegistroTelas.TELA_REGISTRY[nome_tela]

        meta = dados['metadata']

        tela_instância = dados['class'](self.container, self.controller)

        self.controller.title(meta['título_janela'])

        self._criar_cabeçalho_automático(tela_instância, meta)

        if meta['mostrar_voltar'] and self.histórico:
            self._criar_botão_voltar(tela_instância)

    def _criar_cabeçalho_automático(self, tela, meta):


        tela.header_título = Texto(
            classe=tela,
            texto=meta['cabeçalho'],
            fonte=('times new roman', 30),
            # x='centro',
            y=0,
            altura=45,
            largura=self.controller.largura - 10
        )
        tela.header_desc = Texto(
            classe=tela,
            texto=meta['descrição'],
            fonte=('Arial', 17),
            y=40,
            altura=30,
            largura=self.controller.largura - 10
        )

    def voltar(self):
        if self.histórico:
            última_tela = self.histórico.pop()
            self.abrir(última_tela, salvar_no_histórico=False)

    def _criar_botão_voltar(self, tela):
        if not self.histórico:
            return


        tela.bt_back = Botão(
            tela,
            função=self.voltar,
            texto='←',
            fonte=('arial', 20),
            formato='bold',
            x=10, y=10,
            largura= 40, altura=40
        )
        tela.bt_back.lift()

