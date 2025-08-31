from typing import Callable, Optional, Literal
from customtkinter import CTkFrame, CTk, CTkButton


#TODO: Formatação condicional
class Botão(CTkFrame) :
    def __init__(
            self,
            classe,
            texto: str,
            função,
            condição: bool = True,
            fonte: tuple[str, int] = ('Arial', 16),
            formato: Literal['bold', 'italic', 'underline', 'overstrike'] | list[
                Literal['bold', 'italic', 'underline', 'overstrike']] = 'normal',
            x: int | str = 'centro',
            y: int | str = 'centro',
            altura: int = 35,
            largura: int = 35,
            cor:  str | tuple[str, str] | None = None,
    ):
        self.master: CTkFrame = classe.master
        self.controller: CTk = classe.controller

        super().__init__(self.master, width=largura, height=altura)
        self.altura_widget = altura
        self.largura_widget = largura
        self._x = x
        self._y = y

        self.condição = condição



        self.widget_botão = CTkButton(
            self,
            text=texto,
            command=função,
            font=(fonte[0].title(), fonte[1], formato),
            width=largura,
            height=altura,
            fg_color=cor
        )

        self.widget_botão.place(relx=0.5, rely=0.5, anchor='center')

        self.atualizar_visibilidade(self.condição)



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

    def atualizar_visibilidade(self, condição):

        if condição is True:
            self.alocar(self._x, self._y)
        if condição is False:
            self.place_forget()

    def mudar_cor(self, nova_cor):
        self.widget_botão.configure(fg_color=nova_cor)
        self.widget_botão.update()

    def esconder(self):
        if not self.condição :
            self.place_forget()



    # def __getattr__(self, item):
    #     return getattr(self, item)
