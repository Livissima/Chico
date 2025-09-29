from warnings import deprecated

from customtkinter import CTkFrame

from app.config.app_config import DIRETÓRIO_BASE_PADRÃO
from app.config.parâmetros import parâmetros


class NavegaçãoUi(CTkFrame):
    #Todo: Construir classe de navegação ui
    def __init__(self, self_classe):
        self.controller = self_classe.controller
        self.master = self_classe.master
        self.classe = self_classe
        self.trocar_tela()

        super().__init__(self.controller)

    def resetar_path(self):
        parâmetros.novo_diretório = DIRETÓRIO_BASE_PADRÃO
        self.classe._in_diretório_base.limpar()
        self.classe._tx_feedback.att('Diretório revertido para o padrão.')

        print(f'Alteração de path reiniciada para: {parâmetros.novo_diretório}')


    def trocar_tela(self):
        raise NotImplemented

    def bt_back(self):
        raise NotImplemented


