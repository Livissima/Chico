import os.path
from tkinter.filedialog import askdirectory

from customtkinter import CTkFrame, CTk


class PesquisaDiretório(CTkFrame):
    def __init__(
            self,
            master,
            título_janela: str,
            widget_input_diretório
    ):
        super().__init__(master=master)

        self.widget_input_diretório = widget_input_diretório
        self.título_janela = título_janela
        self.path: str  = ''
        self.pesquisar()

    def pesquisar(self):
        pesquisa = self._pesquisar()
        self._atualizar_texto(pesquisa)


    def _pesquisar(self):
        return askdirectory(title=self.título_janela)

    def _atualizar_texto(self, pesquisa):
        if pesquisa:
            self.path = os.path.normpath(pesquisa)
            self.widget_input_diretório.delete(0, 'end')
            self.widget_input_diretório.insert(0, self.path)


