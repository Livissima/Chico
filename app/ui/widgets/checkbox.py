import tkinter
from typing import Literal, List

from customtkinter import CTkFrame, CTk, CTkCheckBox


class CheckBox(CTkFrame):
    def __init__(
            self,
            classe,
            opções: List[str],
            fonte: tuple[str, int] = ('Arial', 16),
            formato: Literal['bold', 'italic', 'underline', 'overstrike'] | list[
                Literal['bold', 'italic', 'underline', 'overstrike']] = 'normal',
            x: int | str = 'centro',
            y: int | str = 'centro',
            altura: int = 35,
            largura: int = 35,
            espaçamento: int = 5
    ):
        self.master: CTkFrame = classe.master
        self.controller: CTk = classe.controller
        super().__init__(
            self.master,
            width=largura*len(opções) + espaçamento*(len(opções)-1),
            height=altura
        )

        self.altura_widget = altura
        self.largura_widget = largura

        self.checkboxes = {}


        for idx, texto in enumerate(opções):
            variável = tkinter.BooleanVar(value=True)
            checkbox = CTkCheckBox(
                self,
                text=texto,
                font=(fonte[0].title(), fonte[1], formato),
                width=largura,
                height=altura,
                variable=variável
            )
            checkbox.place(x=idx*(largura + espaçamento), y=0)
            self.checkboxes[texto] = (checkbox, variável)

        self.alocar(x, y)

    def valor(self) -> dict[str, bool]:
        return {texto: var.get() for texto, (_, var) in self.checkboxes.items()}

    def marcar(self, texto: str):
        if texto in self.checkboxes:
            self.checkboxes[texto][1].set(True)

    def desmarcar(self, texto: str):
        if texto in self.checkboxes:
            self.checkboxes[texto][0].set(False)


    def alocar(self, x, y) :
        _x = 0
        _y = 0

        geometria: list = (self.controller.geometry().replace('x', ' ').replace('+', ' ')).split()
        coordenadas = [int(coordenada) for coordenada in geometria]

        x_centro = (coordenadas[0] // 2) - (self.largura_widget*len(self.checkboxes) // 2)
        y_centro = (coordenadas[1] // 2) - (self.altura_widget // 2)

        _x = x_centro if x == 'centro' else x
        _y = y_centro if y == 'centro' else y

        self.place(x=_x, y=_y)