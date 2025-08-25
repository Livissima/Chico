import os.path

from customtkinter import CTkFrame

from app.auto.bot.navegador import Navegador
from app.ui.widgets import Botão, Input, CheckBox
from typing import TYPE_CHECKING

from .utils.cabeçalhos import Cabeçalhos
from ..functions.obterdiretório import PesquisaDiretório
from ...__metadata__ import PROJECT_NAME

if TYPE_CHECKING:
    from .janelaprincipal import JanelaPrincipal


class TelaBotSige(CTkFrame):
    def __init__(self, master, controller: "JanelaPrincipal"):
        super().__init__(master)
        self.master = master
        self.controller = controller
        self.pack(expand=True, fill='both')
        self._configurar_layout()
        self._inserir_widgets()

    @property
    def _kwargs(self):
        alvos = self.ck_alvos.valor()
        alvos = [chave.lower() for chave, valor in alvos.items() if valor]
        return {
            'destino' : self.input_pasta_dados.valor,
            'alvos' : alvos
        }

    def _configurar_layout(self):
        Cabeçalhos(self, 'bot sige')

    def _inserir_widgets(self):
        self.__inserir_textos()
        self.__inserir_inputs()
        self.__inserir_botões()
        self.__inserir_dropdowns()
        self.__inserir_checkboxes()


    def __inserir_textos(self):
        pass

    def __inserir_inputs(self):
        self.input_pasta_dados = Input(
            master=self.master,
            controller=self.controller,
            texto=r'C:\Users\...\...\Dados',
            fonte=('arial', 10),
            x=120,
            y=135,
            altura=28,
            largura=420+55
        )
        pass

    def __inserir_botões(self):
        self.bt_back = Botão(
            master=self.master,
            controller=self.controller,
            função=lambda: self.controller.alternador.abrir('bot'),
            texto='←',
            fonte=('Arial', 20),
            formato='bold',
            x=10,
            y=10,
        )

        self.bt_localizar_dados = Botão(
            master=self.master,
            controller=self.controller,
            texto='Localizar',
            fonte=('times new roman', 15),
            formato='bold',
            x=5,
            y=136,
            função=self.pesquisar_pasta_dados,
            altura=25,
            largura=100
        )

        self.bt_iniciar = Botão(
            master=self.master,
            controller=self.controller,
            texto='Iniciar',
            fonte=('times new roman', 20),
            formato='bold',
            x='centro',
            y=300,
            largura=90,
            # função=lambda: print(self._kwargs)
            função=lambda: Navegador(tarefa='downloads', destino=self._kwargs['destino'], alvos=self._kwargs['alvos'])
            # função=lambda : Navegador(tarefa='downloads', kwargs_tarefa=self._kwargs)
        )
        pass

    def __inserir_checkboxes(self):
        self.ck_alvos = CheckBox(
            master=self.master,
            controller=self.controller,
            opções=['Fichas', 'Contatos', 'Situações', 'Gêneros'],
            altura=30,
            largura=100,
            x='centro',
            y=200
        )
        pass



    def pesquisar_pasta_dados(self):
        PesquisaDiretório(
            self,
            título_janela='Selecione a pasta onde serão armazenados os relatórios',
            widget_input_diretório=self.input_pasta_dados
        )

    def __inserir_dropdowns(self):
        pass

