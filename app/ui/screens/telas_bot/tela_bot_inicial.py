from typing import TYPE_CHECKING

from customtkinter import CTkFrame, CTk

from app.auto.bot import Bot
from app.ui.config.cabeçalhos import Cabeçalhos
from app.ui.widgets import Botão, Texto

if TYPE_CHECKING:
    pass

class TelaBot(CTkFrame):
    #todo: Bolar um esqueminha de botão que aborte a automação em curso.
    #todo: Elaborar funções para pedir confirmação para executar o auto
    #todo: Inserir dicas flutuantes

    def __init__(self, master: CTk, controller: "Janela"):
        super().__init__(master)
        self.master: CTk = master
        self.controller = controller
        # self.pack(expand=True, fill='both')
        self._configurar_layout()
        self._inserir_widgets()

    def _configurar_layout(self):
        Cabeçalhos(self, 'telas_bot')

    def _inserir_widgets(self):
        self.__inserir_textos()
        self.__inserir_inputs()
        self.__inserir_botões()
        self.__inserir_dropdowns()

    def __inserir_textos(self):
        self.tx_feedback = Texto(
            self,
            texto='',
            fonte=('arial', 20),
            y=400 - 5,
            altura=100,
            largura=self.controller.largura - 10
        )

    def __inserir_inputs(self):
        pass

    def __inserir_botões(self):
        y = 90
        largura = 130

        self.bt_siap = Botão(
            self,
            função=lambda: Bot(tarefa='siap'),
            texto='SIAP',
            fonte=('Arial', 20),
            formato='bold',
            x=10+80,
            y=y,
            largura=largura,
        )

        self.bt_sige = Botão(
            self,
            função=lambda: self.controller.alternador.abrir('telas_bot sige'),
            texto='SIGE',
            fonte=('Arial', 20),
            formato='bold',
            x=10+150+80,
            y=y,
            largura=largura,
        )
        self.bt_credenciais = Botão(
            self,
            função=lambda: self.controller.alternador.abrir('telas_bot google'),
            texto='Credenciais',
            fonte=('Arial', 20),
            formato='bold',
            x=10+150+150+80,
            y=y,
            largura=largura,
        )

        self.bt_back = Botão(
            self,
            função=lambda: self.controller.alternador.abrir('inicial'),
            texto='←',
            fonte=('Arial', 20),
            formato='bold',
            x=10,
            y=10,
        )

    def __inserir_dropdowns(self):
        pass

