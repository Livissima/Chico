import tkinter as tk
from typing import Literal

from customtkinter import CTkFrame, CTk, CTkEntry


# from Frontend import ALTURA_COMUM, LARGURA_COMUM, STICKY_COMUM


class Input(CTkFrame):
    def __init__(
            self,
            master: CTk,
            controller,
            texto: str,
            fonte: tuple[str, int] = ('Arial', 12),
            formato: Literal['bold', 'italic', 'underline', 'overstrike'] | list[
                Literal['bold', 'italic', 'underline', 'overstrike']] = 'normal',
            x: int = 0,
            y: int = 0,
            altura: int = 35,
            largura: int = 35,
    ):
        super().__init__(master, width=largura, height=altura)
        self.master: CTk = master
        self.controller = controller
        self.altura_widget = altura
        self.largura_widget = largura
        self.alocar(x, y)

        self.input = CTkEntry(
            self,
            placeholder_text=texto,
            font=(fonte[0].title(), fonte[1], formato),
            height=altura,
            width=largura,

        )
        self.input.place(relx=0.5, rely=0.5, anchor='center')

        # self.div_input.configure(justify=tk.CENTER)
    def alocar(self, x, y) :
        _x = 0
        _y = 0

        geometria: list = (self.controller.geometry().replace('x', ' ').replace('+', ' ')).split()
        coordenadas = [int(coordenada) for coordenada in geometria]

        x_centro = (coordenadas[0] // 2) - (self.largura_widget // 2)
        y_centro = (coordenadas[1] // 2) - (self.altura_widget // 2)

        if x == 'centro': _x = x_centro
        else: _x = x

        if y == 'centro': _y = y_centro
        else: _y = y

        self.place(x=_x, y=_y)


    @property
    def valor(self):
        return self.input.get()

    def atualizar_valor_zerado(self):
        self.input.delete(0, tk.END)
        self.input.insert(0, '1')

    def __getattr__(self, item):
        return getattr(self.input, item)

    def __str__(self):
        return str(self.input.get())


