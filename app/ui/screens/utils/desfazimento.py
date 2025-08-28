from customtkinter import CTkFrame

from app.config.app_config import DIRETÓRIO_BASE_PADRÃO
from app.ui.screens.config.parâmetros import parâmetros


class Desfazimento(CTkFrame):
    def __init__(self, self_classe):
        self.controller = self_classe.controller
        self.master = self_classe.master
        self.classe = self_classe

        super().__init__(self.controller)


    def desfazer(self):
        parâmetros.novo_diretório = DIRETÓRIO_BASE_PADRÃO
        self._in_diretório_base.limpar()
        self._tx_feedback.att('Diretório revertido para o padrão.')
        # self._bt_desfazer.destroy()

        print(f'Desfeito para: {parâmetros.novo_diretório}')

    def __getattr__(self, item):
        return getattr(self.classe, item)
