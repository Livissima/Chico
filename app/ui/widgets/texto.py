from typing import Literal, TYPE_CHECKING

from customtkinter import CTkFrame, CTk, CTkLabel
if TYPE_CHECKING:
    from app.ui.screens.janela import Janela

class Texto(CTkFrame):
    def __init__(
            self,
            classe,
            texto: str = None,
            textos_empilhados: list[str] = None,
            fonte: tuple[str, int] = ('Arial', 16),
            formato: Literal['bold', 'italic', 'underline', 'overstrike'] | list[Literal['bold', 'italic', 'underline', 'overstrike']]  = 'normal',
            cor = None,
            x: int | str = 'centro',
            y: int | str = 'centro',
            largura: int = 35,
            altura: int = 35,
            compound: str = 'center',
            anchor: str = 'center',
            espaçamento: int = 5,
            preenchimento_x: int = 0
    ):

        self.altura_somada = None
        self.master: CTkFrame = classe.master
        self.controller: "Janela" = classe.controller

        super().__init__(self.master, width=largura, height=altura)

        self.altura_widget = altura
        self.largura_widget = largura
        self.x = x
        self.y = y
        self.preenchimento_x = preenchimento_x

        self.linhas_de_texto = textos_empilhados or []
        self.espaçamento = espaçamento
        self.texto = texto or ''
        self.widget_texto = None
        self.widgets_de_texto: list[CTkLabel] = []

        if self.texto and not self.linhas_de_texto:
            self.criar_texto_único(fonte, formato, cor, compound, anchor)
        if self.linhas_de_texto and not self.texto:
            self.criar_textos_empilhados(fonte, formato, cor, compound, anchor)

        self.alocar(x, y)


    def criar_texto_único(self, fonte, formato, cor, compound, anchor):
        self.widget_texto = CTkLabel(
            self,
            text=f'{self.texto}',
            font=(fonte[0].title(), int(fonte[1]), formato),
            compound=compound,
            anchor=anchor,
            text_color=cor,
            width=self.largura_widget - 2 * self.preenchimento_x,
        )
        if anchor in ['w', 'nw', 'sw'] :
            self.widget_texto.place(relx=0, x=self.preenchimento_x, rely=0.5, anchor='w')

        elif anchor in ['e', 'ne', 'se']:
            self.widget_texto.place(relx=1.0, x=-self.preenchimento_x, rely=0.5, anchor='e')
        else:
            self.widget_texto.place(relx=0.5, rely=0.5, anchor='center')

        self.widgets_de_texto.append(self.widget_texto)


    def criar_textos_empilhados(self, fonte, formato, cor, compound, anchor):

        self.altura_somada = len(self.linhas_de_texto) * self.altura_widget + (len(self.linhas_de_texto) - 1) * self.espaçamento
        self.configure(height=self.altura_somada)

        for índice, linha in enumerate(self.linhas_de_texto):
            y = índice * (self.altura_widget + self.espaçamento) + self.altura_widget / 2
            rely_pos = y / self.altura_somada
            widget = CTkLabel(
                self,
                text=linha,
                font=(fonte[0].title(), int(fonte[1]), formato),
                compound=compound,
                anchor=anchor,
                text_color=cor,
                height=self.altura_widget,
                width=self.largura_widget - 2 * self.preenchimento_x
            )

            if anchor in ['w', 'nw', 'sw']:
                widget.place(relx=0, x=self.preenchimento_x, rely=rely_pos, anchor=anchor)
            elif anchor in ['e', 'ne', 'se']:
                widget.place(relx=1.0, x=-self.preenchimento_x, rely=rely_pos, anchor=anchor)
            else:
                widget.place(relx=0.5, rely=rely_pos, anchor=anchor)
            self.widgets_de_texto.append(widget)


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


    def att(
            self,
            novo_texto: str,
            fonte: tuple[str, int] = ('Arial', 16),
            formato: Literal['bold', 'italic', 'underline', 'overstrike'] | list[Literal['bold', 'italic', 'underline', 'overstrike']]  = 'normal',
            cor: str = 'white',
            índice: int = None
    ):

        if not índice:
            for widget in self.widgets_de_texto:
                widget.configure(text=novo_texto, text_color=cor, font=(fonte[0].title(), int(fonte[1]), formato))

        if isinstance(índice, int) and 0 <= índice < len(self.widgets_de_texto):
            self.widgets_de_texto[índice].configure(text=novo_texto, text_color=cor, font=(fonte[0].title(), int(fonte[1]), formato))




