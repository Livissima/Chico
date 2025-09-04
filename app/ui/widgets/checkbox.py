import tkinter
from typing import Literal, List
from customtkinter import CTkFrame, CTk, CTkCheckBox

class CheckBox(CTkFrame):
    def __init__(
            self,
            classe,
            opções: List[str],
            valores_iniciais: dict[str, bool] | None = None,
            valor_exclusivo: str | None = None,
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
        self.valor_exclusivo = valor_exclusivo  # Armazena o valor exclusivo

        temp_font = (fonte[0].title(), fonte[1], formato)
        temp_label = tkinter.Label(self.master, text="", font=temp_font)

        # Inclui o valor_exclusivo na lista de textos para cálculo de largura
        textos_calculo = opções[:]
        if valor_exclusivo:
            textos_calculo.append(valor_exclusivo)

        max_text_width = 0
        for texto in textos_calculo:
            temp_label.config(text=texto)
            text_width = temp_label.winfo_reqwidth()
            max_text_width = max(max_text_width, text_width)

        temp_label.destroy()
        checkbox_width = max(largura, max_text_width + 20)
        # Ajusta o número total de checkboxes incluindo o exclusivo se existir
        n_checkboxes = len(opções) + (1 if valor_exclusivo else 0)
        total_width = checkbox_width * n_checkboxes + espaçamento * (n_checkboxes - 1)

        super().__init__(self.master, width=total_width, height=altura)

        self.altura_widget = altura
        self.largura_widget = checkbox_width
        self.espaçamento = espaçamento

        self.checkboxes = {}

        if valores_iniciais is None:
            valores_iniciais = {opção: True for opção in opções}

        # Cria checkboxes regulares
        for índice, texto in enumerate(opções):
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
            # Configura o comando para desmarcar o exclusivo quando marcado
            if valor_exclusivo:
                checkbox.configure(command=lambda v=variável: self._ao_marcar_checkbox(v))
            checkbox.place(x=índice * (checkbox_width + espaçamento), y=0)
            self.checkboxes[texto] = (checkbox, variável)

        # Cria checkbox exclusivo se especificado
        if valor_exclusivo:
            índice_exclusivo = len(opções)
            variável_exclusivo = tkinter.BooleanVar(value=False)
            checkbox_exclusivo = CTkCheckBox(
                self,
                text=valor_exclusivo,
                font=temp_font,
                width=checkbox_width,
                height=altura,
                variable=variável_exclusivo,
                command=self._ao_marcar_exclusivo
            )
            x_pos = índice_exclusivo * (checkbox_width + espaçamento)
            checkbox_exclusivo.place(x=x_pos, y=0)
            self.checkboxes[valor_exclusivo] = (checkbox_exclusivo, variável_exclusivo)

        self.alocar(x, y)

    def _ao_marcar_exclusivo(self):
        """Lida com a marcação do checkbox exclusivo."""
        checkbox_exclusivo, var_exclusivo = self.checkboxes[self.valor_exclusivo]
        if var_exclusivo.get():  # Se o exclusivo foi marcado
            for texto, (checkbox, var) in self.checkboxes.items():
                if texto != self.valor_exclusivo:  # Desmarca todos os outros
                    var.set(False)

    def _ao_marcar_checkbox(self, variável_marcada):
        """Lida com a marcação de checkboxes regulares."""
        if self.valor_exclusivo and variável_marcada.get():
            # Desmarca o checkbox exclusivo se algum outro for marcado
            var_exclusivo = self.checkboxes[self.valor_exclusivo][1]
            var_exclusivo.set(False)

    def valor(self) -> dict[str, bool]:
        return {texto: var.get() for texto, (_, var) in self.checkboxes.items()}

    def marcar(self, texto: str):
        if texto in self.checkboxes:
            self.checkboxes[texto][1].set(True)

    def desmarcar(self, texto: str):
        if texto in self.checkboxes:
            self.checkboxes[texto][1].set(False)

    def alocar(self, x, y):
        _x = 0
        _y = 0

        geometria = self.controller.geometry()
        partes = geometria.split('+')
        tamanho = partes[0].split('x')

        largura_janela = int(tamanho[0])
        altura_janela = int(tamanho[1])

        n_checkboxes = len(self.checkboxes)
        largura_total = self.largura_widget * n_checkboxes + self.espaçamento * (n_checkboxes - 1)

        x_centro = (largura_janela // 2) - (largura_total // 2)
        y_centro = (altura_janela // 2) - (self.altura_widget // 2)

        _x = x_centro if x == 'centro' else x
        _y = y_centro if y == 'centro' else y

        self.place(x=_x, y=_y)

    @property
    def valores_true(self):
        return [chave for chave, valor in self.valor().items() if valor is True]