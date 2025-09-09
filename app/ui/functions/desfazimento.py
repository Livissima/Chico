from customtkinter import CTkFrame

from app.config.app_config import DIRETÓRIO_BASE_PADRÃO
from app.config.parâmetros import parâmetros
from typing import TYPE_CHECKING
# if TYPE_CHECKING:
#     from app.ui.screens

class Desfazimento(CTkFrame):
    def __init__(self, self_classe: CTkFrame):
        self.controller = self_classe.controller
        self.master = self_classe.master
        self.classe = self_classe

        super().__init__(self.controller)

    # @staticmethod
    def desfazer(self):
        parâmetros.novo_diretório = DIRETÓRIO_BASE_PADRÃO
        self.classe._in_diretório_base.limpar()
        self.classe._tx_feedback.att('Diretório revertido para o padrão.')
        # self._bt_desfazer.destroy()

        print(f'Desfeito para: {parâmetros.novo_diretório}')

    def __getattr__(self, item):
        return getattr(self.classe, item)


