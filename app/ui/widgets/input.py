import tkinter as tk
from typing import Literal

from customtkinter import CTkFrame, CTk, CTkEntry



class Input(CTkFrame):
    def __init__(
            self,
            classe,
            texto: str,
            fonte: tuple[str, int] = ('Arial', 12),
            formato: Literal['bold', 'italic', 'underline', 'overstrike'] | list[
                Literal['bold', 'italic', 'underline', 'overstrike']] = 'normal',
            x: int = 0,
            y: int = 0,
            altura: int = 35,
            largura: int = 35,
    ):
        self.master = classe.master
        self.controller = classe.controller

        super().__init__(self.master, width=largura, height=altura)

        self.altura_widget = altura
        self.largura_widget = largura
        self.texto = texto
        self.alocar(x, y)

        self.input = CTkEntry(
            self,
            placeholder_text=texto,
            font=(fonte[0].title(), fonte[1], formato),
            height=altura,
            width=largura,

        )
        # self.input.insert(0, texto)
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

    def __getattr__(self, item):
        return getattr(self.input, item)

    def __str__(self):
        return str(self.input.get())

    def att(self, valor):
        self.input.delete(0, "end")
        self.input.insert(0, valor)

    def limpar(self):
        self.input.delete(0, "end")
        self.input.configure(placeholder_text=self.controller.novo_diretório)

