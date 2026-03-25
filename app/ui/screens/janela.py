from customtkinter import CTk, CTkFrame
from app.ui.config.dimensionamento import Dimensionamento
from app.ui.functions.alternadordetelas import AlternadorDeTelas


class Janela(CTk):
    def __init__(self):
        super().__init__()
        self.altura = None
        self.largura = None
        self.container = CTkFrame(self)
        self.container.pack(expand=True, fill='both')
        self._set_appearance_mode('dark')

        self.dimensionar()

        self.alternador: AlternadorDeTelas = AlternadorDeTelas(self.container, self)

    def _ir_tela(self):
        self.alternador.abrir('inicial')

    def dimensionar(self):
        Dimensionamento(self).posicionar()
        self.largura = Dimensionamento.largura
        self.altura = Dimensionamento.altura
