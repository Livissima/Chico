from typing import Literal

from customtkinter import CTkFrame, CTk, CTkLabel


class Texto(CTkFrame):
    def __init__(
            self,
            master: CTk,
            controller,
            texto: str,
            fonte: tuple[str, int] = ('Arial', 16),
            formato: Literal['bold', 'italic', 'underline', 'overstrike'] | list[Literal['bold', 'italic', 'underline', 'overstrike']]  = 'normal',
            x: int = 0,
            y: int = 0,
            largura: int = 35,
            altura: int = 35,
            compound: str = 'center',
            anchor: str = 'center',

    ):
        super().__init__(master, width=largura, height=altura)
        self.master: CTk = master
        self.controller = controller
        self.altura_widget = altura
        self.largura_widget = largura
        self.alocar(x, y)

        self.div_texto = CTkLabel(
            self,
            text=texto,
            font=(fonte[0].title(), int(fonte[1]), formato),
            compound=compound,
            anchor=anchor
        )

        self.div_texto.place(relx=0.5, rely=0.5, anchor='center')

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


    def atualizar_texto(self, novo_texto: str):
        self.div_texto.configure(text=novo_texto)
        self.div_texto.update()
