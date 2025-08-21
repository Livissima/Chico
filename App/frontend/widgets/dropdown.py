from tkinter import StringVar
from typing import Literal

from customtkinter import CTkFrame, CTk, CTkOptionMenu
# from Frontend import ALTURA_COMUM, LARGURA_COMUM, STICKY_COMUM


class Dropdown(CTkFrame):
    def __init__(
            self,
            master: CTk,
            # variável_da_div: StringVar,
            alternativas: list[str],
            fonte: tuple[str, int] = ('Arial', 16),
            formato: Literal['bold', 'italic', 'underline', 'overstrike'] | list[
                Literal['bold', 'italic', 'underline', 'overstrike']] = 'normal',
            x: int = 0,
            y: int = 0,
            altura: int = 35,
            largura: int = 35,
    ):
        super().__init__(master, width=largura, height=altura)
        self.master: CTk = master
        self.altura_widget = altura
        self.largura_widget = largura
        self.alocar(x, y)

        self.div_dropdown = CTkOptionMenu(
            self,
            # variable=variável_da_div,
            values=alternativas,
            width=largura,
            height=altura,
            font=(fonte[0], fonte[1], formato),
        )

        self.div_dropdown.place(relx=0.5, rely=0.5, anchor='center')

    def alocar(self, x, y):
        _x = 0
        _y = 0

        geometria: list = (self.master.geometry().replace('x', ' ').replace('+', ' ')).split()
        coordenadas = [int(coordenada) for coordenada in geometria]

        x_centro = (coordenadas[0] // 2) - (self.largura_widget // 2)
        y_centro = (coordenadas[1] // 2) - (self.altura_widget // 2)

        if x == 'centro' :
            _x = x_centro
        else :
            _x = x

        if y == 'centro' :
            _y = y_centro
        else :
            _y = y

        self.place(x=_x, y=_y)
