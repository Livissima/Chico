from tkinter import StringVar
from typing import Literal, TYPE_CHECKING, Optional, Union, Callable

from customtkinter import CTkFrame, CTk, CTkOptionMenu
if TYPE_CHECKING:
    from app.ui.screens.janela import Janela

class Dropdown(CTkFrame):
    def __init__(
            self,
            classe,
            alternativas: list[str],
            comando : Optional[Callable] = None,
            fonte: tuple[str, int] = ('Arial', 16),
            formato: Literal['bold', 'italic', 'underline', 'overstrike'] | list[
                Literal['bold', 'italic', 'underline', 'overstrike']] = 'normal',
            x: int | str = 'centro',
            y: int | str = 'centro',
            altura: int = 35,
            largura: int = 100,
            arredondamento: Optional[Union[int]] = None
    ):
        self.master: CTkFrame = classe.master
        self.controller: "Janela" = classe.controller
        super().__init__(self.master, width=largura, height=altura)
        self._comando_mudança = comando
        self.altura_widget = altura
        self.largura_widget = largura
        self.x = x
        self.y = y

        self._variável_valor = StringVar(value=alternativas[0] if alternativas else '')

        self.dropdown = CTkOptionMenu(
            self,
            variable=self._variável_valor,
            values=alternativas,
            command=self._executar_comando,
            width=largura,
            height=altura,
            font=(fonte[0], fonte[1], formato),
            corner_radius=arredondamento,
            anchor='center',
        )

        self.dropdown.place(relx=0.5, rely=0.5, anchor='center')
        self.alocar(x, y)

    def _executar_comando(self, valor_selecionado):
        if self._comando_mudança:
            self._comando_mudança(valor_selecionado)

    def atualizar_alternativas(self, novas_alternativas: list[str]):
        valor_atual = self.valor_selecionado
        self.dropdown.configure(values=novas_alternativas)

        if novas_alternativas and valor_atual not in novas_alternativas:
            self.valor_selecionado = novas_alternativas[0]


    @property
    def valor_selecionado(self):
        return self._variável_valor.get()

    @valor_selecionado.setter
    def valor_selecionado(self, valor: str):
        self._variável_valor.set(valor)

    def alocar(self, x, y) :
        if x == 'centro' or y == 'centro' :
            largura_tela = self.controller.largura
            altura_tela = self.controller.altura
            if x == 'centro' :
                x_pos = (largura_tela - self.largura_widget) // 2
            else :
                x_pos = x
            if y == 'centro' :
                altura_real = self.winfo_reqheight()
                y_pos = (altura_tela - altura_real) // 2
            else :
                y_pos = y
        else :
            x_pos, y_pos = x, y
        self.place(x=x_pos, y=y_pos)






    # def __getattr__(self, item):
    #     return getattr(self.master, item)
