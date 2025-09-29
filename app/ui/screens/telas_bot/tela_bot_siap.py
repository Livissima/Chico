import os.path
import time

from customtkinter import CTkFrame, CTk

from app.auto.bot import Bot
from app.auto.tasks import ConsultaDiasLetivos

from app.config.app_config import DIRETÓRIO_BASE_PADRÃO
from app.config.parâmetros import parâmetros
from app.ui.functions.desfazimento import Desfazimento
from app.ui.widgets import Botão, Input, CheckBox, Texto, Dropdown
from typing import TYPE_CHECKING

from app.ui.config.cabeçalhos import Cabeçalhos
from app.ui.functions.pesquisa_diretório import PesquisaDiretório
from app.ui.widgets.caixa_data import CaixaData

if TYPE_CHECKING :
    from app.ui.screens.janela import Janela

ANO = 2025

class TelaBotSiap(CTkFrame) :
    def __init__(self, master, controller: "Janela") :
        super().__init__(master)
        self.master: CTk = master
        self.controller = controller

        self._configurar_layout()
        self._inserir_widgets()

    def _inserir_widgets(self):

        self.__inserir_botões()
        self.__inserir_textos()
        self.__inserir_checkboxes()
        self.__inserir_inputs()
        self.__inserir_dropdowns()


    def __inserir_textos(self):
        feed_inicial = {
            'texto' : f'{len(parâmetros.lista_dias_letivos)} dias letivos disponíveis para iterar sobre.',
            'fonte' : ('arial', 20)}

        # if not parâmetros.turmas_disponíveis:
        #     feed_inicial = {
        #         'texto' : '',
        #         'fonte' : ('arial', 16),
        #         'cor' : 'orange',
        #         'formato' : 'bold'
        #     }

        self._tx_feedback = Texto(
            self,
            **feed_inicial,
            # texto='  ',
            # fonte=('arial', 16),
            y=400-5,
            altura=100,
            largura=self.controller.largura-10,

        )
        pass

    def _configurar_layout(self) :
        Cabeçalhos(self, 'telas_bot siap')

    def __inserir_dropdowns(self):
        #todo fazer um kit de um frame com 3 widgets dentro, que servirá de modelo para o dropdown que gerará a tupla
        # de datas iniciais e finais
        x_inicial = 10
        self._dd_mês_inicial = Dropdown(
            self,
            alternativas=list(parâmetros.dicionário_dias_letivos.keys()),
            comando=self.atualizar_dropdown_dia_inicial,
            x=x_inicial,
            altura=25,
            largura=70,
            arredondamento=0
        )

        self._dd_dia_inicial = Dropdown(
            self,
            alternativas=[],
            # comando=self.atualizar_dropdown_dia_inicial,
            x=x_inicial+75,
            altura=25,
            largura=70,
            arredondamento=0
        )
        pass

    def __inserir_checkboxes(self):
        self.ck_dias_alvo = CheckBox(
            self,
            opções=['Hoje'],
            valor_exclusivo='Outros Dias',
            y=100
        )

    def __inserir_inputs(self):
        pass

    def __inserir_botões(self):
        self._inserir_botão_de_obter_dias_letivos()

        self.bt_iniciar = Botão(
            self,
            função=lambda: Bot(tarefa='siap', path=parâmetros.novo_diretório ),
            # função=lambda: print(f'{self._dd_dia_inicial.valor_selecionado = }, {self._dd_mês_inicial.valor_selecionado = }'),
            texto='Iniciar',
            formato='bold',
            y=350,
            largura=130
        )

        self.bt_back = Botão(
            self,
            função=lambda: self.controller.alternador.abrir('telas_bot'),
            texto='←',
            fonte=('Arial', 20),
            formato='bold',
            x=10,
            y=10,
        )

        self.bt_modulação = Botão(
            self,
            função= lambda: Bot(tarefa='obter modulações', path=parâmetros.novo_diretório),
            largura=100
        )

    def _inserir_botão_de_obter_dias_letivos(self):

        if len(parâmetros.lista_dias_letivos) == 0:
            self.bt_obter_dias_letivos = Botão(
                self,
                função=lambda: self._função_botão_obter(),
                texto='Obter dias letivos',
                largura=150,
                y=300
            )

    def _função_botão_obter(self):
        self._tx_feedback.att(f'Consultando dias letivos para o ano de {ANO}', ('arial', 20))
        print('clicado')
        time.sleep(1)
        try:
            Bot(tarefa='consultar dias letivos', ano=ANO, path=parâmetros.novo_diretório)
            dias = parâmetros.lista_dias_letivos
            self._tx_feedback.att(f'Dias obtidos em {ANO}: {len(dias)}')
        except Exception as e:
            self._tx_feedback.att(f'Falha em obter dias letivos')
            print(f'Falha em obter dias letivos: {e}')

    def atualizar_dropdown_dia_inicial(self, mês_selecionado):
        novas_alternativas = parâmetros.dicionário_dias_letivos.get(mês_selecionado, [])
        self._dd_dia_inicial.atualizar_alternativas(novas_alternativas)



