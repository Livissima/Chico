from typing import TYPE_CHECKING

from app.ui.screens import PROJECT_NAME, PROJECT_VERSION
from app.ui.widgets import Texto, Botão

if TYPE_CHECKING:
    from .janelaprincipal import JanelaPrincipal


class TelaInicial:
    def __init__(self, master, controller: "JanelaPrincipal"):
        # super().__init__(controller)
        self.master = master
        self.controller = controller
        self._configurar_layout()
        self._inserir_widgets()  # self.mainloop()

    def _configurar_layout(self) :
        self.controller.title(f'{PROJECT_NAME}    v.{PROJECT_VERSION}')



    
    def _inserir_widgets(self):
        self.__inserir_textos()
        self.__inserir_inputs()
        self.__inserir_botões()
        self.__inserir_dropdowns()

    def __inserir_textos(self):
        self.título = Texto(
            self.master,
            controller=self.controller,
            texto=f'{PROJECT_NAME}',
            fonte=('times new roman', 30),
            x=0,
            y=0,
            altura=35,
            largura=self.controller.largura,
        )

        self.título = Texto(
            self.master,
            controller=self.controller,
            texto='Auxiliar de Secretaria',
            fonte=('Arial', 15),
            x=0,
            y=29,
            altura=25,
            largura=self.controller.largura,
        )

    def __inserir_inputs(self):
        pass

    def __inserir_botões(self):
        self.botão_bot = Botão(
            self.master,
            controller=self.controller,
            função= lambda: self.controller.alternador.abrir('auto'),
            texto='BOT',
            formato='bold',
            x=20,
            y=60,
            largura=100

        )
        self.botão_tratamento = Botão(
            self.master,
            controller=self.controller,
            função= lambda: self.controller.alternador.abrir('consulta'),
            texto='Consulta',
            formato='bold',
            x=20+120,
            y=60,
            largura=100
        )

    def __inserir_dropdowns(self):
        pass
