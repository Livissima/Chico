import os.path
from tkinter.filedialog import askdirectory

from customtkinter import CTkFrame, CTk

from app.config.app_config import DIRETÓRIO_BASE_PADRÃO


class PesquisaDiretório(CTkFrame):
    def __init__(
            self,
            classe,
            título_janela: str,
            widget_input
    ):
        self.classe = classe
        self.controller = classe.controller

        super().__init__(master=classe)

        self.widget_input = widget_input
        self.título_janela = título_janela
        self.path: str  = ''

        self.pesquisar()

    def pesquisar(self):

        print(f'Atual: {self.controller.novo_diretório}')

        self.widget_input.att(self.controller.novo_diretório)

        self.obter_diretório()

        self.controller.novo_diretório = self.path

        self.classe._bt_desfazer.atualizar_visibilidade(
            self.controller.novo_diretório != DIRETÓRIO_BASE_PADRÃO
        )

        if self.controller.novo_diretório == DIRETÓRIO_BASE_PADRÃO:
            print(f'Alteração cancelada. Ficou {self.controller.novo_diretório}')

            return

        if self.controller.novo_diretório != DIRETÓRIO_BASE_PADRÃO:
            print(f'Alterado para: {self.controller.novo_diretório}')
            self.classe._tx_feedback.att(f'Diretório base atualizado.')
            return


    def obter_diretório(self):
        pesquisa = askdirectory(title=self.título_janela)
        self._atualizar_valor_widget(pesquisa)

    def _atualizar_valor_widget(self, pesquisa):
        #todo: criar método para atualizar o tx_feedback.

        if pesquisa:
            self.path = os.path.normpath(pesquisa)
            self.widget_input.delete(0, 'end')
            self.widget_input.insert(0, self.path)
            return

        if not pesquisa:
            self.path = self.controller.novo_diretório
            self.widget_input.delete(0, 'end')
            self.widget_input.insert(0, self.path)





