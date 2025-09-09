import os.path
from pathlib import Path
from typing import TYPE_CHECKING
from customtkinter import CTk, CTkFrame
from app.core import Consulta, Exportação
from app.ui.functions.pesquisa_diretório import PesquisaDiretório
from app.config.parâmetros import parâmetros
from app.ui.widgets.botão import Botão
from app.ui.widgets.input import Input
from app.ui.widgets.texto import Texto

from app.ui.config.cabeçalhos import Cabeçalhos
from app.ui.functions.desfazimento import Desfazimento
from app.config.app_config import DIRETÓRIO_BASE_PADRÃO

if TYPE_CHECKING:
    pass

class TelaConsulta(CTkFrame):
    #todo: aprimorar o widget de feedback da consulta, que continua consultando
    # quando o código crasha

    def __init__(self, master: CTk, controller: "Janela"):
        super().__init__(master)
        self._bt_desfazer = None
        self.master: CTk = master
        self.controller = controller

        self._configurar_layout()
        self._inserir_widgets()

    def _configurar_layout(self):
        Cabeçalhos(self, 'consulta')

    def _inserir_widgets(self):
        self.__inserir_botões()
        self.__inserir_textos()
        self.__iserir_inputs()

    def __inserir_textos(self):

        self._tx_feedback = Texto(
            self,
            texto=self._obter_situação()['novo_texto'],
            fonte=('times new roman', 25),
            x='centro',
            y=395,
            altura=100,
            largura=self.controller.largura-5,
        )
        self._tx_feedback.att(**self._obter_situação())

    def __inserir_botões(self):
        self.bt_localizar_diretório_base = Botão(
            self,
            texto='Localizar',
            fonte=('times new roman', 15),
            formato='bold',
            x=5,
            y=136,
            função=lambda: self._pesquisar_diretório(),
            altura=25,
            largura=100
        )

        self.botão_consultar = Botão(
            self,
            função=lambda: self.consultar(),
            texto='CONSULTAR',
            fonte=('times new roman', 20),
            formato='bold',
            largura=(larg := 250),
            x=(self.controller.largura - larg) // 2,
            y=325,
            altura=35
        )

        self.bt_back = Botão(
            self,
            função=lambda: self.controller.alternador.abrir('inicial'),
            texto='←',
            fonte=('Arial', 20),
            formato='bold',
            x=10,
            y=10,
        )

        self._bt_desfazer = Botão(
            self,
            função=lambda: self._desfazer(),
            condição=parâmetros.novo_diretório != DIRETÓRIO_BASE_PADRÃO,
            texto='↩',
            fonte=('arial', 25),
            x=550,
            y=170
        )

    def __iserir_inputs(self):
        self._in_diretório_base = Input(
            self,
            texto=fr'{os.path.join(parâmetros.novo_diretório, 'fonte')}',
            fonte=('arial', 12),
            x=120,
            y=135,
            altura=28,
            largura=420+55
        )

    def consultar(self):
        diretório_base = parâmetros.novo_diretório
        fonte = str(os.path.join(diretório_base, 'fonte'))

        self._tx_feedback.att('Consultando')
        try:
            consulta = Consulta(diretório_fonte=fonte)

            self._tx_feedback.att('Exportando')

            Exportação(consulta=consulta, path_destino=diretório_base)

            self._tx_feedback.att(f'Planilhas geradas e exportadas para\n{diretório_base}')

        except FileNotFoundError: self._tx_feedback.att('Erro ao consultar')

    @staticmethod
    def _obter_situação():
        def truncar_diretório(_dir: str) -> str:
            _diretório = _dir.split('\\')
            _diretório = os.path.join(*_diretório[0 :3], '...', '...', *_diretório[-2 :])
            _diretório = _diretório.replace(':', ':\\')
            return _diretório

        diretório = str(os.path.join(parâmetros.novo_diretório, 'fonte'))

        if len(diretório) > 60:
            diretório_display = truncar_diretório(diretório)
        else:
            diretório_display = diretório

        if Path(diretório).exists():
            return {
                'novo_texto' : f'A consulta será realizada a partir do diretório:\n{diretório_display}',
                'fonte' : ('arial', 20),
                'cor' : 'light green',
                'formato' : 'bold'
            }

        else:
            #todo: rever a condição para considerar a existência dos jsons correspondentes, não do diretório
            return {
                'novo_texto' : f'Diretório não encontrado neste computador:\n'
                               f''f'{diretório_display}\nVocê já executou o Bot de Downloads?',
                'cor' : 'orange',
                'fonte' : ('arial', 18)
            }


    def _pesquisar_diretório(self):
        PesquisaDiretório(self, 'Selecione o novo diretório', self._in_diretório_base)
        self._tx_feedback.att(**self._obter_situação())

    def _desfazer(self):
        Desfazimento(self).desfazer()
        self._tx_feedback.att(**self._obter_situação())
