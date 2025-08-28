import os.path

from customtkinter import CTkFrame, CTk
from app.auto.bot import Bot
from app.ui.widgets import Botão
from typing import TYPE_CHECKING

from app.ui.screens.config.cabeçalhos import Cabeçalhos

if TYPE_CHECKING:
    pass

class TelaBotCredenciais(CTkFrame):
    def __init__(self, master, controller: "Janela"):
        super().__init__(master)
        self.master: CTk = master
        self.controller = controller
        # self.pack(expand=True, fill='both')
        self._configurar_layout()
        self._inserir_widgets()

    def _configurar_layout(self):
        Cabeçalhos(self, 'telas_bot credenciais')

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
            função=lambda: self.controller.alternador.abrir('telas_bot'),
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
                path_database= os.path.join(self.controller.novo_diretório, 'Database.xlsx'),
                tipo='netescola'
            ),
            texto='Netescola',
            largura=100,
            x=150,
        )

        self.bt_google = Botão(
            self,
            função=lambda: print('botão google'),
            texto='Google',
            largura=100,
            x=350
        )
