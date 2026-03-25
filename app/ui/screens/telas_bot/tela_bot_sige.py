import os.path

from customtkinter import CTkFrame, CTk

from app.auto.bot import Bot

from app.config.settings.app_config import DIRETÓRIO_BASE_PADRÃO
from app.config.parâmetros import parâmetros
from app.ui.functions.desfazimento import Desfazimento
from app.ui.config.registrodetelas import RegistradorDeTelas
from app.ui.widgets import Botão, Input, CheckBox, Texto
from typing import TYPE_CHECKING

# from app.ui.config.cabeçalhos import Cabeçalhos
from app.ui.functions.pesquisadiretório import PesquisaDiretório

if TYPE_CHECKING:
    pass

@RegistradorDeTelas.registrar(
    nome_tela='telas_bot sige',
    título_da_janela='Bot SIGE',
    cabeçalho='BOT SIGE',
    descrição='Automação de tarefas'
)
class TelaBotSige(CTkFrame):
    def __init__(self, master, controller: "Janela"):
        super().__init__(master)
        self.master: CTk = master
        self.controller = controller

        self._inserir_widgets()
        self._carregar_estado_anterior()

    @property
    def _kwargs(self) -> dict:
        return {
            'destino' : parâmetros.diretório_base,
            'alvos' : self._ck_alvos.valores_true
        }


    def _inserir_widgets(self):

        self.__inserir_checkboxes()
        self.__inserir_textos()
        # self.__inserir_inputs()
        self.__inserir_botões()
        # self.__inserir_dropdowns()

    def __inserir_textos(self):
        feed_inicial = {'texto' : '', 'fonte' : ('arial', 20)}

        if not parâmetros.turmas_disponíveis:
            feed_inicial = {
                'texto' : 'Turmas não encontradas. Faça o download do conteúdo de todas as turmas,\n' 
                          'ou faça uma sondagem caso queira selecionar turmas específicas.',
                'fonte' : ('arial', 16),
                'cor' : 'orange',
                'formato' : 'bold'
            }

        self._tx_feedback = Texto(
            self,
            **feed_inicial,
            # texto=feed_inicial[0],
            # fonte=('arial', feed_inicial[1]),
            y=400-5,
            altura=100,
            largura=self.controller.largura-10,

        )

    def __inserir_inputs(self):
        self._in_diretório_base = Input(
            self,
            texto=str(os.path.join(parâmetros.diretório_base, 'fonte')),
            x=120,
            y=135,
            largura=420+55
        )

    def __inserir_botões(self):
        def back():
            self.salvar_estado()
            self.controller.alternador.abrir('telas_bot')

        self._bt_back = Botão(
            self,
            função=lambda: back(),
            texto='←',
            fonte=('Arial', 20),
            formato='bold',
            x=10,
            y=10,
        )

        # self._bt_localizar_dados = Botão(
        #     self,
        #     texto='Definir pasta',
        #     fonte=('times new roman', 15),
        #     formato='bold',
        #     x=5,
        #     y=136,
        #     função=self.pesquisar_pasta_dados,
        #     altura=25,
        #     largura=100
        # )

        self._bt_iniciar = Botão(
            self,
            texto='Iniciar',
            fonte=('times new roman', 20),
            formato='bold',
            x='centro',
            y=350,
            largura=90,
            função=lambda: self.iniciar_tarefa(),
            condição=len(parâmetros.turmas_disponíveis) > 0
        )


        self._bt_desfazer = Botão(
            self,
            função=lambda: self._desfazer(),
            condição=parâmetros.diretório_base != DIRETÓRIO_BASE_PADRÃO,
            texto='↩',
            fonte=('arial', 25),
            x=560,
            y=135+30
        )

        self.bt_sondagem_emergencial = Botão(
            self,
            função=lambda: Bot(tarefa='sondagem', parâmetros_web=None, path=parâmetros.diretório_base),
            condição=len(parâmetros.turmas_disponíveis) == 0,
            texto='SONDAR',
            fonte=('arial', 15),
            formato='bold',
            x='centro',
            y=300,
            largura=90
        )

    def __inserir_checkboxes(self):
        self._ck_alvos = CheckBox(
            self,
            opções=['Fichas', 'Contatos', 'Situações', 'Gêneros'],
            valor_exclusivo='Fotos',
            altura=30,
            largura=80,
            x=0,
            y=200, espaçamento=5
        )

        self._inserir_checkbox_turmas()

    def _inserir_checkbox_turmas(self) :
        estado_turmas = {}
        for turma in parâmetros.turmas_disponíveis :
            if hasattr(parâmetros, '_estado_turmas') and turma in parâmetros._estado_turmas :
                estado_turmas[turma] = parâmetros._estado_turmas[turma]
            else :
                estado_turmas[turma] = True

        self._ck_turmas = CheckBox(
            self,
            opções=parâmetros.turmas_disponíveis,
            valores_iniciais=estado_turmas
        )

    def __inserir_dropdowns(self):
        pass

    def pesquisar_pasta_dados(self):
        PesquisaDiretório(
            self,
            título_janela='Selecione a pasta onde serão armazenados os relatórios',
            widget_input=self._in_diretório_base
        )
        self._verificar_estatística()

    def iniciar_tarefa(self):
        self.salvar_estado()

        if not self._ck_alvos.valores_true:
            self._tx_feedback.att('Selecione ao menos um conteúdo alvo.')
            print(f'selecione ao menos um conteúdo alvo')

        if any(alvo in self._ck_alvos.valores_true for alvo in ['Fichas', 'Contatos', 'Situações', 'Gêneros']):
            Bot(tarefa='downloads', parâmetros_web=None, destino=self._kwargs['destino'],
                alvos=self._ck_alvos.valores_true)

        if self._ck_alvos.valores_true == ['Fotos']:
            print(f'____Fotos')
            Bot(tarefa='fotos', parâmetros_web=None, turmas=parâmetros.turmas_selecionadas)


    def _verificar_estatística(self):
        self.bt_sondagem_emergencial.atualizar_visibilidade(len(parâmetros.turmas_disponíveis) == 0)
        if len(parâmetros.turmas_disponíveis) == 0:
            self._bt_iniciar.mudar_cor('grey')
        if len(parâmetros.turmas_disponíveis) > 0:
            self._bt_iniciar.mudar_cor('blue')

    def _desfazer(self):
        Desfazimento(self).desfazer()
        self._bt_desfazer.atualizar_visibilidade(
            parâmetros.diretório_base != DIRETÓRIO_BASE_PADRÃO
        )
        self._verificar_estatística()


    def sondar(self):
        Bot(tarefa='sondagem', parâmetros_web=None, path=parâmetros.diretório_base)
        self._verificar_estatística()


    def salvar_estado(self):
        parâmetros.estado_checkbox_alvos = self._ck_alvos.valor()
        parâmetros.estado_checkbox_turmas = self._ck_turmas.valor()
        parâmetros.turmas_selecionadas = [t for t, v in parâmetros.estado_checkbox_turmas.items() if v]

    def _carregar_estado_anterior(self):
        if parâmetros.estado_checkbox_alvos:
            for nome, valor in parâmetros.estado_checkbox_alvos.items():
                if valor: self._ck_alvos.marcar(nome)
                else: self._ck_alvos.desmarcar(nome)

