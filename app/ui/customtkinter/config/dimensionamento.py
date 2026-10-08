from customtkinter import CTk
from screeninfo import get_monitors


class Dimensionamento:
    largura: int = 600
    altura: int = 500

    def __init__(self, janela_ctk: CTk):
        self.janela = janela_ctk
        self.monitor_index = 0

    def posicionar(self):
        self.janela.geometry(f'{self.window_size}+{self.posição_central_tela}')
        self.janela.resizable(False, False)
        # self.janela._set_appearance_mode('dark')

    @property
    def window_size(self):
        return f'{self.largura}x{self.altura}'

    @property
    def posição_central_tela(self):
        monitores = get_monitors()
        if self.monitor_index >= len(monitores):
            raise ValueError(f"Monitor {self.monitor_index} não encontrado. Existem apenas {len(monitores)} monitores.")

        monitor = monitores[self.monitor_index]
        x = monitor.x + (monitor.width // 2) - (self.largura // 2)
        y = monitor.y + (monitor.height // 2) - (self.altura // 2)
        return f'{x}+{y}'




