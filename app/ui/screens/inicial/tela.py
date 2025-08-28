from typing import TYPE_CHECKING
from customtkinter import CTkFrame, CTk
from app.ui.widgets import Texto, Botão, Input
from app.ui.screens.config.cabeçalhos import Cabeçalhos
from app.ui.screens.utils.desfazimento import Desfazimento

from app.ui.functions.pesquisa_diretório import PesquisaDiretório
from app.config.app_config import DIRETÓRIO_BASE_PADRÃO

if TYPE_CHECKING:
    pass


class TelaInicial(CTkFrame):
    def __init__(self, master, controller: "Janela"):
        super().__init__(controller)
        self._bt_desfazer = None
        self.master: CTk = master
        self.controller = controller
        # self.controller.novo_diretório = self._in_diretório_base.valor

        self._configurar_layout()
        self._inserir_widgets()  # self.mainloop()

    def _configurar_layout(self) :
        Cabeçalhos(self, 'inicial')

    def _inserir_widgets(self):
        self.primeira_linha = 180
        self.segunda_linha = 350

        self.__inserir_textos()
        self.__inserir_inputs()
        self.__inserir_dropdowns()

        self.__inserir_botões()

    def __inserir_textos(self):
        self.tx_intro = Texto(
            self,
            texto=f'Diretório base:\n{DIRETÓRIO_BASE_PADRÃO}',
            fonte=('arial', 15),
            x='centro',
            y=80,
            largura=self.controller.largura-10,
            altura=40
        )

        self.tx_alterar_diretório = Texto(
            self,
            texto='Alterar diretório (opcional)',
            formato='bold',
            x=5,
            y=self.primeira_linha-35,
            largura=220
        )

        self._tx_feedback = Texto(
            self,
            texto='',
            fonte=('arial', 20),
            y=400-5,
            altura=100,
            largura=self.controller.largura-10,
        )

    def __inserir_inputs(self):

        self._in_diretório_base = Input(
            self,
            texto=self.controller.novo_diretório,
            fonte=('arial', 15),
            x=160,
            y=self.primeira_linha,
            altura=30,
            largura=420
        )

    def __inserir_botões(self):

        self.bt_bot = Botão(
            self,
            função= lambda: self.controller.alternador.abrir('telas_bot'),
            texto='BOT',
            formato='bold',
            x=20+160,
            y=self.segunda_linha,
            largura=100
        )

        self.bt_consulta = Botão(
            self,
            função= lambda: self.controller.alternador.abrir('consulta'),
            texto='Consulta',
            formato='bold',
            x=20+120+160,
            y=self.segunda_linha,
            largura=100
        )

        self.bt_pesquisar_diretório = Botão(
            self,
            função=lambda: PesquisaDiretório(self, 'testando', self._in_diretório_base),
            texto='Pesquisar diretório',
            fonte=('arial', 14),
            formato='bold',
            x=5,
            y=self.primeira_linha,
            altura=30,
            largura=150
        )

        self._bt_desfazer = Botão(
            self,
            função=lambda: self._desfazer(),
            condição=self.controller.novo_diretório != DIRETÓRIO_BASE_PADRÃO,
            texto='↩',
            fonte=('arial', 25),
            x=550
        )


    def __inserir_dropdowns(self):
        pass

    def _pesquisar_diretório(self):
        PesquisaDiretório(self, 'testando', self._in_diretório_base)

    def aplicar_botão_de_desfazer(self):
        if self.controller.novo_diretório != DIRETÓRIO_BASE_PADRÃO:

            self._tx_feedback.att(f'Diretório base atualizado!')

        return None

    def _desfazer(self):
        self._bt_desfazer.atualizar_visibilidade(
            self.controller.novo_diretório != DIRETÓRIO_BASE_PADRÃO
        )
        Desfazimento(self).desfazer()


