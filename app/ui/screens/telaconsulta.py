from pathlib import Path
from typing import TYPE_CHECKING

from customtkinter import CTk, CTkFrame

from app.backend import Consulta, Exportação
from app.ui.functions.obterdiretório import PesquisaDiretório
from app.ui.screens import PROJECT_NAME
from app.ui.widgets.botão import Botão
from app.ui.widgets.input import Input
from app.ui.widgets.texto import Texto

if TYPE_CHECKING:
    from .janelaprincipal import JanelaPrincipal

class TelaConsulta(CTkFrame):
    #todo: aprimorar o widget de feedback da consulta, que continua consultando
    # quando o código crasha

    def __init__(self, master: CTk, controller: "JanelaPrincipal"):
        super().__init__(master)
        self.master: CTk = master
        self.controller = controller
        self.pack(expand=True, fill='both')
        self._configurar_layout()
        self._inserir_widgets()

    def _configurar_layout(self):
        self.controller.title(f'{PROJECT_NAME} - Consulta')

    def _inserir_widgets(self):
        self.__inserir_textos()
        self.__iserir_inputs()
        self.__inserir_botões()

    def __inserir_textos(self):
        self.título = Texto(
            master=self.master,
            controller=self.controller,
            texto='GO Office',
            fonte=('times new roman', 30),
            x=0,
            y=0,
            altura=35,
            largura=self.controller.largura,
        )

        self.título = Texto(
            master=self.master,
            controller=self.controller,
            texto='Auxiliar de Secretaria',
            fonte=('Arial', 15),
            x=0,
            y=29,
            altura=25,
            largura=self.controller.largura,
        )

        self.tex_insira_caminho = Texto(
            master=self.master,
            controller=self.controller,
            texto=' Insira o caminho para cada pasta de relatórios e clique em CONSULTAR.',
            fonte=('Arial', 16),
            x=0,
            y=75,
            altura=25,
            largura=self.controller.largura,
        )

        self.tex_fichas = Texto(
            master=self.master,
            controller=self.controller,
            texto='Fichas:',
            fonte=('arial', 15),
            formato='bold',
            x=0+5,
            y=118,
            altura=15,
            largura=55
        )

        self.tex_contatos = Texto(
            master=self.master,
            controller=self.controller,
            texto='Contatos:',
            fonte=('arial', 15),
            formato='bold',
            x=0+5,
            y=118 + 50,
            altura=15,
            largura=70
        )

        self.text_situações = Texto(
            master=self.master,
            controller=self.controller,
            texto='Situações:',
            fonte=('arial', 15),
            formato='bold',
            x=0+5,
            y=118 + 50 + 50,
            altura=15,
            largura=70
        )

        self.tex_gêneros = Texto(
            master=self.master,
            controller=self.controller,
            texto='Gêneros:',
            fonte=('arial', 15),
            formato='bold',
            x=0+5,
            y=118 + 50 + 50 + 50,
            altura=15,
            largura=70
        )

        self.painel_resposta = Texto(
            master=self.master,
            controller=self.controller,
            texto='',
            fonte=('times new roman', 25),
            x=0,
            y=370,
            altura=100,
            largura=self.controller.largura,
        )

    def __inserir_botões(self):
        self.botão_localizar_fichas = Botão(
            master=self.master,
            controller=self.controller,
            texto='Localizar',
            fonte=('times new roman', 13),
            x=5,
            y=136,
            função=self.pesquisar_fichas,
            altura=25,
            largura=100
        )

        self.botão_localizar_contatos = Botão(
            master=self.master,
            controller=self.controller,
            texto='Localizar',
            fonte=('times new roman', 13),
            x=5,
            y=136 + 50,
            função=self.pesquisar_contatos,
            altura=25,
            largura=100
        )


        self.botão_localizar_situações = Botão(
            master=self.master,
            controller=self.controller,
            texto='Localizar',
            fonte=('times new roman', 13),
            x=5,
            y=136 + 50 + 50,
            função=self.pesquisar_situações,
            altura=25,
            largura=100
        )

        self.botão_localizar_gêneros = Botão(
            master=self.master,
            controller=self.controller,
            texto='Localizar',
            fonte=('times new roman', 13),
            x=5,
            y=136 + 50 + 50 + 50,
            função=self.pesquisar_gêneros,
            altura=25,
            largura=100
        )

        self.botão_consultar = Botão(
            master=self.master,
            controller=self.controller,
            função=self.consultar,
            texto='CONSULTAR',
            fonte=('times new roman', 20),
            formato='bold',
            largura=(larg := 250),
            x=(self.controller.largura - larg) // 2,
            y=325,
            altura=35
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

    def __iserir_inputs(self):
        self.input_fichas = Input(
            master=self.master,
            controller=self.controller,
            texto=r'C:\Users\...\...\Fichas',
            fonte=('arial', 10),
            x=120,
            y=135,
            altura=28,
            largura=420+55
        )

        self.input_contatos = Input(
            master=self.master,
            controller=self.controller,
            texto=r'C:\Users\...\...\Contatos',
            fonte=('arial', 10),
            x=120,
            y=135 + 50,
            altura=28,
            largura=420+55
        )

        self.input_situações = Input(
            master=self.master,
            controller=self.controller,
            texto=r'C:\Users\...\...\Situações',
            fonte=('arial', 10),
            x=120,
            y=135 + 50 + 50,
            altura=28,
            largura=420+55
        )

        self.input_gêneros = Input(
            master=self.master,
            controller=self.controller,
            texto=r'C:\Users\...\...\Gêneros',
            fonte=('arial', 10),
            x=120,
            y=135 + 50 + 50 + 50,
            altura=28,
            largura=420+55
        )

    def consultar(self):
        self.painel_resposta.atualizar_texto('Consultando')
        consulta = Consulta(
            path_fichas=self.input_fichas.valor,
            path_contatos=self.input_contatos.valor,
            path_situações=self.input_situações.valor,
            path_gêneros=self.input_gêneros.valor
        )
        self.painel_resposta.atualizar_texto('Exportando')
        Exportação(consulta=consulta, path_destino=Path.home() / "Desktop")

        self.painel_resposta.atualizar_texto('Planilhas geradas e exportadas para a área de trabalho')

    #todo: Unificar em uma função flexível, que retorne uma função sem executar
    def pesquisar_fichas(self):
        PesquisaDiretório(
            self,
            título_janela='Selecione a pasta com relatórios de fichas.',
            widget_input_diretório=self.input_fichas)
        print(self.input_fichas.valor)

    def pesquisar_contatos(self):
        PesquisaDiretório(
            self,
            título_janela='Selecione a pasta com relatórios de contatos.',
            widget_input_diretório=self.input_contatos)
        print(self.input_contatos.valor)

    def pesquisar_situações(self):
        PesquisaDiretório(
            self,
            título_janela='Selecione a pasta com relatórios de situações.',
            widget_input_diretório=self.input_situações)
        print(self.input_situações.valor)

    def pesquisar_gêneros(self):
        PesquisaDiretório(
            self,
            título_janela='Selecione a pasta com relatórios de gêneros.',
            widget_input_diretório=self.input_gêneros)
        print(self.input_gêneros.valor)
