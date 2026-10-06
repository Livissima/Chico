from customtkinter import CTk, CTkFrame
from app.ui.customtkinter.config.dimensionamento import Dimensionamento
from app.ui.customtkinter.navegabilidade.alternadordetelas import AlternadorDeTelas


class Janela(CTk):
    def __init__(self):
        super().__init__()

        self.largura = Dimensionamento.largura
        self.altura = Dimensionamento.altura

        self.container = CTkFrame(self)

        self._definir_layout()

        self.alternador: AlternadorDeTelas = AlternadorDeTelas(self.container, self)

    def _ir_tela(self):
        self.alternador.abrir('inicial')

    def _definir_layout(self):
        self.container.pack(expand=True, fill='both')
        self._set_appearance_mode('dark')
        Dimensionamento(self).posicionar()

