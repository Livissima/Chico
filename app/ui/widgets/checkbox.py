import tkinter
from typing import Literal, List
from customtkinter import CTkFrame, CTk, CTkCheckBox


class CheckBox(CTkFrame) :
    def __init__(
            self,
            classe,
            opções: List[str],
            valores_iniciais: dict[str, bool] | None = None,
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

        temp_font = (fonte[0].title(), fonte[1], formato)
        temp_label = tkinter.Label(self.master, text="", font=temp_font)

        max_text_width = 0
        for texto in opções :
            temp_label.config(text=texto)
            text_width = temp_label.winfo_reqwidth()
            max_text_width = max(max_text_width, text_width)

        temp_label.destroy()
        checkbox_width = max(largura, max_text_width + 20)
        total_width = checkbox_width * len(opções) + espaçamento * (len(opções) - 1)

        super().__init__(self.master, width=total_width, height=altura)

        self.altura_widget = altura
        self.largura_widget = checkbox_width
        self.espaçamento = espaçamento

        self.checkboxes = {}

        if valores_iniciais is None:
            valores_iniciais = {opção: True for opção in opções}

        for índice, texto in enumerate(opções) :
            valor_inicial = valores_iniciais.get(texto, True)

            variável = tkinter.BooleanVar(value=valor_inicial)
            checkbox = CTkCheckBox(
                self,
                text=texto,
                font=temp_font,
                width=checkbox_width,
                height=altura,
                variable=variável
            )

            checkbox.place(x=índice * (checkbox_width + espaçamento), y=0)
            self.checkboxes[texto] = (checkbox, variável)

        self.alocar(x, y)

    def valor(self) -> dict[str, bool] :
        return {texto : var.get() for texto, (_, var) in self.checkboxes.items()}

    def marcar(self, texto: str) :
        if texto in self.checkboxes :
            self.checkboxes[texto][1].set(True)

    def desmarcar(self, texto: str) :
        if texto in self.checkboxes :
            self.checkboxes[texto][1].set(False)

    def alocar(self, x, y) :
        _x = 0
        _y = 0


        geometria = self.controller.geometry()
        partes = geometria.split('+')
        tamanho = partes[0].split('x')

        largura_janela = int(tamanho[0])
        altura_janela = int(tamanho[1])


        largura_total = self.largura_widget * len(self.checkboxes) + self.espaçamento * (len(self.checkboxes) - 1)


        x_centro = (largura_janela // 2) - (largura_total // 2)
        y_centro = (altura_janela // 2) - (self.altura_widget // 2)

        _x = x_centro if x == 'centro' else x
        _y = y_centro if y == 'centro' else y

        self.place(x=_x, y=_y)

    @property
    def valores_true(self):
        return [chave for chave, valor in self.valor().items() if valor is True]

