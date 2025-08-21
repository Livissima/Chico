from typing import TYPE_CHECKING

from customtkinter import CTkFrame, CTk

from app.auto.bot.navegador import Navegador
from app.frontend.widgets import Texto, Botão
from .__init__ import TITLE

if TYPE_CHECKING:
    from .janelaprincipal import JanelaPrincipal

class TelaBot(CTkFrame):
    #todo: Bolar um esqueminha de botão que aborte a automação em curso.
    #todo: Elaborar funções para pedir confirmação para executar o auto
    #todo: Inserir dicas flutuantes

    def __init__(self, master: CTk, controller: "JanelaPrincipal"):
        super().__init__(master)
        self.master: CTk = master
        self.controller = controller
        self.pack(expand=True, fill='both')
        self._configurar_layout()
        self._inserir_widgets()
        # self.mainloop()

    def _configurar_layout(self):
        self.controller.title(f'{TITLE} - Bot')


    def _inserir_widgets(self):
        self.__inserir_textos()
        self.__inserir_inputs()
        self.__inserir_botões()
        self.__inserir_dropdowns()

    def __inserir_textos(self):
        self.título = Texto(
            master=self.master,
            controller=self.controller,
            texto='BOT',
            x=0,
            y=0,
            altura=35,
            largura=self.controller.largura,
            fonte=('times new roman', 30)
        )

        self.título = Texto(
            master=self.master,
            controller=self.controller,
            texto='Automação de tarefas',
            fonte=('Arial', 15),
            x=0,
            y=29,
            altura=25,
            largura=self.controller.largura,
        )

        self.título = Texto(
            master=self.master,
            controller=self.controller,
            texto='Automação de tarefas',
            fonte=('Arial', 15),
            x=0,
            y=29,
            altura=25,
            largura=self.controller.largura,
        )

    def __inserir_inputs(self):
        pass

    def __inserir_botões(self):
        self.bt_siap = Botão(
            master=self.master,
            controller=self.controller,
            função=lambda: Navegador(tarefa='siap'),
            texto='SIAP',
            fonte=('Arial', 20),
            formato='bold',
            x=10+80,
            y=100,
            largura=100,
        )
        self.bt_sige = Botão(
            master=self.master,
            controller=self.controller,
            função=lambda: Navegador(tarefa='downloads', ),
            texto='SIGE',
            fonte=('Arial', 20),
            formato='bold',
            x=10+150+80,
            y=100,
            largura=100,
        )
        self.bt_google = Botão(
            master=self.master,
            controller=self.controller,
            função=self.controller.quit,
            texto='Google',
            fonte=('Arial', 20),
            formato='bold',
            x=10+150+150+80,
            y=100,
            largura=100,
        )

        self.bt_back = Botão(
            master=self.master,
            controller=self.controller,
            função=lambda: self.controller.alternador.abrir('inicial'),
            texto='←',
            fonte=('Arial', 20),
            formato='bold',
            x=10,
            y=10,

        )

    def __inserir_dropdowns(self):
        # self.tarefa = Dropdown(
        #     self,
        #     # variável_da_div=self.botao,
        #     alternativas=Tarefas().tarefas,
        #     x=10,
        #     y=100,
        #     largura=150,
        #     altura=30,
        #     fonte=('arial', 15)
        # )
        pass



if __name__ == '__main__':
    TelaBot()
