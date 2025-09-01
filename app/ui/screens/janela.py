from customtkinter import CTk, CTkFrame
from app.ui import Dimensionamento
from app.ui.utils.alternador_de_telas import AlternadorDeTelas


class Janela(CTk):
    def __init__(self):
        super().__init__()
        self.altura = None
        self.largura = None
        self.container = CTkFrame(self)
        self.container.pack(expand=True, fill='both')

        self.dimensionar()

        self.alternador: AlternadorDeTelas = AlternadorDeTelas(self.container, self)
        self.alternador.abrir('inicial')

        self.mainloop()


    def _ir_tela(self):
        self.alternador = AlternadorDeTelas(self.container, self)
        self.alternador.abrir('inicial')

    def dimensionar(self):
        Dimensionamento(self).posicionar()
        self.largura = Dimensionamento.largura
        self.altura = Dimensionamento.altura
