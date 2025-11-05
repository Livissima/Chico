from customtkinter import CTkFrame, CTk
from typing import TYPE_CHECKING

from ..config.cabeçalhos import Cabeçalhos
from ..widgets import Botão, Input
from ...core.frequency.compiladordefaltas import CompiladorDeFaltas

if TYPE_CHECKING :
    from .janela import Janela


class Frequência(CTkFrame) :
    def __init__(self, master, controller: "Janela") :
        super().__init__(controller)
        self.master: CTk = master
        self.controller = controller

        self._configurar_layout()
        self._inserir_widgets()

    def _configurar_layout(self) :
        Cabeçalhos(self, 'frequência')

    def _inserir_widgets(self) :
        self.__inserir_textos()
        self.__inserir_botões()
        # self.__inserir_inputs()

    def __inserir_textos(self) :
        pass

    def __inserir_botões(self) :
        self._bt_back = Botão(
            self,
            função=lambda : self.controller.alternador.abrir('inicial'),
            texto='←',
            fonte=('Arial', 20),
            formato='bold', x=10, y=10
        )

        self._bt_compilar_faltas = Botão(
            self,
            função=lambda: CompiladorDeFaltas
        )




    def __inserir_inputs(self) :
        self.in_nome = Input(
            self,
            texto='Estudante',
            formato='bold',
            y=400,
            largura=self.controller.largura-20

        )
        pass
