import os.path
from pathlib import Path

from customtkinter import CTkFrame, CTk
from platformdirs import user_documents_dir

from app.auto.bot import Bot
from app.ui.widgets import Botão, Input, CheckBox, Texto
from typing import TYPE_CHECKING

from .utils.cabeçalhos import Cabeçalhos
from ..functions.pesquisa_diretório import PesquisaDiretório

if TYPE_CHECKING:
    from .janela import Janela


class TelaBotSige(CTkFrame):
    def __init__(self, master, controller: "Janela"):
        super().__init__(master)
        self.master: CTk = master
        self.controller = controller

        # self.pack(expand=True, fill='both')
        self._configurar_layout()
        self._inserir_widgets()

    @property
    def _kwargs(self):
        alvos = self.ck_alvos.valor()
        alvos = [chave.lower() for chave, valor in alvos.items() if valor]
        return {
            'destino' : Path(user_documents_dir()) / 'SIGE' / 'fonte',
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
        self.tx_intro = Texto(
            self,
            texto='Diretório selecionado:',
            fonte=('arial', 15),
            formato='bold',
            y=200,
            largura=self.controller.largura-5,
        )

        self.tx_feedback = Texto(
            self,
            texto='',
            fonte=('arial', 20),
            y=400-5,
            altura=100,
            largura=self.controller.largura-10,
        )

    def __inserir_inputs(self):
        self.input_pasta_dados = Input(
            self,
            texto=str(os.path.join(self.controller.novo_diretório, 'fonte')),
            fonte=('arial', 10),
            x=120,
            y=135,
            altura=28,
            largura=420+55
        )


    def __inserir_botões(self):
        self.bt_back = Botão(
            self,
            função=lambda: self.controller.alternador.abrir('bot'),
            texto='←',
            fonte=('Arial', 20),
            formato='bold',
            x=10,
            y=10,
        )

        self.bt_localizar_dados = Botão(
            self,
            texto='Definir pasta',
            fonte=('times new roman', 15),
            formato='bold',
            x=5,
            y=136,
            função=self.pesquisar_pasta_dados,
            altura=25,
            largura=100
        )

        self.bt_iniciar = Botão(
            self,
            texto='Iniciar',
            fonte=('times new roman', 20),
            formato='bold',
            x='centro',
            y=300,
            largura=90,
            # função=lambda: print(self._kwargs)
            função=lambda: Bot(tarefa='downloads', destino=self._kwargs['destino'], alvos=self._kwargs['alvos'])
            # função=lambda : Bot(tarefa='downloads', kwargs_tarefa=self._kwargs)
        )
        pass

    def __inserir_checkboxes(self):
        self.ck_alvos = CheckBox(
            self,
            opções=['Fichas', 'Contatos', 'Situações', 'Gêneros'],
            altura=30,
            largura=100,
            x='centro',
            y=200
        )
        pass


    def pesquisar_pasta_dados(self):
        print()
        PesquisaDiretório(
            self,
            título_janela='Selecione a pasta onde serão armazenados os relatórios',
            widget_input=self.input_pasta_dados
        )

    def __inserir_dropdowns(self):
        pass

