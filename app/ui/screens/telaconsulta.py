import os.path
from os import PathLike
from pathlib import Path
from typing import TYPE_CHECKING
from platformdirs import user_desktop_dir, user_documents_dir
from customtkinter import CTk, CTkFrame
from app.core import Consulta, Exportação
from app.ui.functions.pesquisa_diretório import PesquisaDiretório
from app.ui.widgets.botão import Botão
from app.ui.widgets.input import Input
from app.ui.widgets.texto import Texto
from .utils.cabeçalhos import Cabeçalhos
from ...config.app_config import DIRETÓRIO_BASE_PADRÃO

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
        Cabeçalhos(self, 'consulta')

    def _inserir_widgets(self):
        self.__inserir_textos()
        self.__iserir_inputs()
        self.__inserir_botões()

    def __inserir_textos(self):

        self.tx_intro = Texto(
            master=self.master,
            controller=self.controller,
            texto=self._obter_situação()[0],
            fonte=('arial', 15),
            formato='bold',
            cor=self._obter_situação()[1],
            x=0+5,
            y=150,
            altura=100,
            largura=self.controller.largura
        )


        self.tx_feedback = Texto(
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
        self.bt_localizar_diretório_base = Botão(
            master=self.master,
            controller=self.controller,
            texto='Localizar',
            fonte=('times new roman', 15),
            formato='bold',
            x=5,
            y=136,
            função=self._pesquisar_diretório,
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
        self.in_diretório_base = Input(
            master=self.master,
            controller=self.controller,
            texto=fr'{DIRETÓRIO_BASE_PADRÃO}',
            fonte=('arial', 12),
            x=120,
            y=135,
            altura=28,
            largura=420+55
        )


    def consultar(self):

        diretório_dados = DIRETÓRIO_BASE_PADRÃO

        def direcionar(alvo) -> str:
            return str(os.path.join(diretório_dados, 'fonte', alvo))

        try:
            self.tx_feedback.att('Consultando')
            consulta = Consulta(
                path_fichas=direcionar('fichas'),
                path_contatos=direcionar('contatos'),
                path_situações=direcionar('situações'),
                path_gêneros=direcionar('gêneros')
            )

            self.tx_feedback.att('Exportando')

            Exportação(consulta=consulta, path_destino=diretório_dados)

            self.tx_feedback.att('Planilhas geradas e exportadas para a área de trabalho')

        except FileNotFoundError: self.tx_feedback.att('Erro ao consultar')

    @staticmethod
    def _obter_situação():
        diretório = Path(DIRETÓRIO_BASE_PADRÃO / 'fonte')
        if diretório.exists():
            return f'A consulta será realizada a partir do diretório:\n{diretório}', 'white'
        else:
            return f'Diretório `{diretório}` não encontrado neste computador.\nPor favor, selecione manualmente o diretório base.', 'red'

    def _pesquisar_diretório(self):
        PesquisaDiretório(
            self,
            título_janela='Selecione a pasta.',
            widget_input_diretório=self.in_diretório_base)
        print(self.in_diretório_base.valor)
        self.tx_intro.att(f'Diretório base atualizado!')