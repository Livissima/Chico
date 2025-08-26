from typing import TYPE_CHECKING

from customtkinter import CTkFrame, CTk

from .__init__ import PROJECT_NAME, PROJECT_VERSION
from app.ui.widgets import Texto, Botão, Input
from app.ui.screens.utils.cabeçalhos import Cabeçalhos
from ..functions.pesquisa_diretório import PesquisaDiretório
from ...config.app_config import DIRETÓRIO_BASE_PADRÃO

if TYPE_CHECKING:
    from .janelaprincipal import JanelaPrincipal


class TelaInicial(CTkFrame):
    def __init__(self, master, controller: "JanelaPrincipal"):
        super().__init__(controller)
        self.master: CTk = master
        self.controller = controller

        self._configurar_layout()
        self._inserir_widgets()  # self.mainloop()

    def _configurar_layout(self) :
        Cabeçalhos(self, 'inicial')

    def _inserir_widgets(self):
        self.primeira_linha = 180
        self.segunda_linha = 350

        self.__inserir_textos()
        self.__inserir_inputs()
        self.__inserir_botões()
        self.__inserir_dropdowns()

    def __inserir_textos(self):
        self.tx_intro = Texto(
            master=self.master,
            controller=self.controller,
            texto=f'Diretório base:\n{DIRETÓRIO_BASE_PADRÃO}',
            fonte=('arial', 15),
            x='centro',
            y=80,
            largura=self.controller.largura-10,
            altura=60
        )

        self.tx_alterar_diretório = Texto(
            master=self.master,
            controller=self.controller,
            texto='Alterar diretório (opcional)',
            formato='bold',
            x=5,
            y=self.primeira_linha-35,
            largura=220
        )

        self.tx_feedback = Texto(
            master=self.master,
            controller=self.controller,
            texto='',
            fonte=('arial', 20),
            y=400-5,
            altura=100,
            largura=self.controller.largura-10,
        )

    def __inserir_inputs(self):

        self.in_diretório_base = Input(
            master=self.master,
            controller=self.controller,
            texto=f'{DIRETÓRIO_BASE_PADRÃO}',
            fonte=('arial', 15),
            x=160,
            y=self.primeira_linha,
            altura=30,
            largura=420
        )

    def __inserir_botões(self):

        self.bt_bot = Botão(
            self.master,
            controller=self.controller,
            função= lambda: self.controller.alternador.abrir('bot'),
            texto='BOT',
            formato='bold',
            x=20+160,
            y=self.segunda_linha,
            largura=100
        )

        self.bt_consulta = Botão(
            self.master,
            controller=self.controller,
            função= lambda: self.controller.alternador.abrir('consulta'),
            texto='Consulta',
            formato='bold',
            x=20+120+160,
            y=self.segunda_linha,
            largura=100
        )

        self.bt_pesquisar_diretório = Botão(
            master=self.master,
            controller=self.controller,
            função=self._pesquisar_diretório,
            texto='Pesquisar diretório',
            fonte=('arial', 14),
            formato='bold',
            x=5,
            y=self.primeira_linha,
            altura=30,
            largura=150
        )

    def __inserir_dropdowns(self):
        pass

    def _pesquisar_diretório(self):

        PesquisaDiretório(
            self,
            título_janela='Selecione o novo diretório base',
            widget_input_diretório=self.in_diretório_base
        )
        novo_diretório = self.in_diretório_base.valor

        if not novo_diretório:
            return

        print(self.in_diretório_base.valor)


        self.tx_feedback.att(f'Diretório base alterado.')


        def desfazer():

            self.in_diretório_base.limpar()
            self.tx_feedback.att('Alteração de diretório revertida.')

        self.bt_desfazer = Botão(
            master=self.master,
            controller=self.controller,
            função=lambda: desfazer(),
            texto='↩',
            fonte=('arial', 25),
            x=550
        )

