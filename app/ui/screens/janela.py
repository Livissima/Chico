from customtkinter import CTk, CTkFrame

from app.config.app_config import DIRETÓRIO_BASE_PADRÃO
from app.ui import Dimensionamento
from app.ui.screens.utils.alternador_de_telas import AlternadorDeTelas
from .__init__ import PROJECT_NAME, PROJECT_VERSION


class Janela(CTk):
    def __init__(self):
        super().__init__()
        self.container = CTkFrame(self)
        self.container.pack(expand=True, fill='both')
        self.novo_diretório = DIRETÓRIO_BASE_PADRÃO

        self._configurar_layout()

        self.alternador: AlternadorDeTelas = AlternadorDeTelas(self.container, self)
        self.alternador.abrir('inicial')

        self.mainloop()


    def _ir_tela(self):
        self.alternador = AlternadorDeTelas(self.container, self)
        self.alternador.abrir('inicial')

    def _configurar_layout(self):
        self._dimensionamento()

    def _dimensionamento(self):
        Dimensionamento(self).posicionar()
        self.largura = Dimensionamento.largura
        self.altura = Dimensionamento.altura

if __name__ == '__main__':
    Janela()
