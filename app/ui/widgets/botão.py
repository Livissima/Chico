from typing import Callable, Optional, Literal
from customtkinter import CTkFrame, CTk, CTkButton


# from Frontend import ALTURA_COMUM, LARGURA_COMUM, STICKY_COMUM


#TODO: Formatação condicional
class Botão(CTkFrame) :
    def __init__(
            self,
            master: CTk,
            controller,
            função: any,
            texto: str,
            fonte: tuple[str, int] = ('Arial', 16),
            formato: Literal['bold', 'italic', 'underline', 'overstrike'] | list[
                Literal['bold', 'italic', 'underline', 'overstrike']] = 'normal',
            x: int | str = 'centro',
            y: int | str = 'centro',
            altura: int = 35,
            largura: int = 35
    ):
        super().__init__(master, width=largura, height=altura)
        self.master: CTk = master
        self.controller = controller
        self.altura_widget = altura
        self.largura_widget = largura
        self.alocar(x, y)

        self.botão = CTkButton(
            self,
            text=texto,
            command=função,
            font=(fonte[0].title(), fonte[1], formato),
            width=largura,
            height=altura
        )

        self.botão.place(relx=0.5, rely=0.5, anchor='center')

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


