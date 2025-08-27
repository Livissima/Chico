from customtkinter import CTkFrame, CTk
from app.auto.bot import Bot
from app.ui.widgets import Botão, Input, Texto
from typing import TYPE_CHECKING

from .utils.cabeçalhos import Cabeçalhos
from ..functions.pesquisa_diretório import PesquisaDiretório
from ...auto.tasks import GerenciarAcessos

if TYPE_CHECKING:
    from .janela import Janela

class TelaBotCredenciais(CTkFrame):
    def __init__(self, master, controller: "Janela"):
        super().__init__(master)
        self.master: CTk = master
        self.controller = controller
        # self.pack(expand=True, fill='both')
        self._configurar_layout()
        self._inserir_widgets()

    def _configurar_layout(self):
        Cabeçalhos(self, 'bot credenciais')

    def _inserir_widgets(self):
        self.__inserir_textos()
        self.__inserir_inputs()
        self.__inserir_botões()

    def __inserir_textos(self):
        pass

    def __inserir_inputs(self):
        pass

    def __inserir_botões(self):
        self.bt_back = Botão(
            self,
            função=lambda: self.controller.alternador.abrir('bot'),
            texto='←',
            fonte=('Arial', 20),
            formato='bold',
            x=10,
            y=10,
        )

        self.bt_netescola = Botão(
            self,
            função=lambda: Bot(
                tarefa='gerenciar',
                path_database= self.controller.novo_diretório,
                tipo='netescola'
            ),
            texto='Netescola',
            largura=100
        )
