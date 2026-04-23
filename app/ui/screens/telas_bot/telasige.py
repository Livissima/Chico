#app/ui/screens/telas_bot/tela_bot_sige.py
from customtkinter import CTkFrame, CTk
from app.auto.bot import Bot
from app.config.parâmetros.estruturadeseleção import EstruturaDeSeleção
from app.config.settings.app_config import DIRETÓRIO_BASE_PADRÃO
from app.config.parâmetros import parâmetros
from app.ui.functions.desfazimento import Desfazimento
from app.ui.config.registrotelas import RegistroTelas
from app.ui.widgets.modelos_widgets import frame_feedback, campo_input, botão_back
from app.ui.widgets import Botão, CheckBox
from typing import TYPE_CHECKING
from app.ui.functions.pesquisadiretório import PesquisaDiretório

if TYPE_CHECKING:
    pass


@RegistroTelas.registrar(
    nome_tela='bot sige',
    título_da_janela='Bot SIGE',
    cabeçalho='BOT SIGE',
    descrição='Automação de tarefas'
)
class TelaSige(CTkFrame):

    def __init__(self, master, controller: "Janela"):
        super().__init__(master)
        self.master: CTk = master
        self.controller = controller

        self._inserir_widgets()
        self._carregar_estado_anterior()


    def _inserir_widgets(self):

        self.__inserir_checkboxes()
        self.__inserir_textos()
        self.__inserir_botões()

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

        self._tx_feedback = frame_feedback(self, feed_inicial['texto'])

    def __inserir_inputs(self):
        self._in_diretório_base = campo_input(self)

    def __inserir_botões(self):
        self._bt_back = botão_back(self, 'bot')

        self._bt_iniciar = Botão(
            self,
            texto='Iniciar',
            fonte=('times new roman', 20),
            formato='bold',
            x=150,
            y=350,
            largura=120,
            função=lambda: self._iniciar_tarefa(),
            condição=len(parâmetros.turmas_disponíveis) > 0
        )

        self._bt_noteador = Botão(
            self,
            texto='Lançar notas',
            fonte=('times new roman', 20),
            formato='bold',
            x=300,
            y=350,
            largura=140,
            função=lambda: self._notear()
        )

        self.bt_sondagem_emergencial = Botão(
            self,
            função=lambda: Bot(tarefa='sondagem', parâmetros_web=None, path=parâmetros.diretório_base),
            condição=len(parâmetros.turmas_disponíveis) == 0,
            texto='SONDAR',
            fonte=('arial', 15),
            formato='bold',
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
            y=200,
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

    def _iniciar_tarefa(self):
        self.salvar_estado()

        seleção = EstruturaDeSeleção(
            séries_selecionadas=parâmetros.séries_selecionadas,
            turmas_selecionadas_por_série=parâmetros.turmas_selecionadas_por_série
        )

        if not self._ck_alvos.valores_true or not seleção.turmas_selecionadas_por_série:
            self._tx_feedback.atualizar('Selecione ao menos um conteúdo alvo.')
            print(f'\n      ### Nenhum conteúdo selecionado para download.\n')
            return

        if not seleção.turmas_selecionadas_por_série:
            self._tx_feedback.atualizar('Selecione ao menos uma turma')
            print('     ### Nenhuma turma selecionada para download.')
            return

        if any(alvo in self._ck_alvos.valores_true for alvo in ['Fichas', 'Contatos', 'Situações', 'Gêneros']):
            # print(f'{seleção = }')
            # print(f'{seleção = }')
            # print(f'{seleção = }')
            Bot(tarefa='downloads', destino=parâmetros.diretório_base, tarefas_sige=self._ck_alvos.valores_true, seleção=seleção)

        if self._ck_alvos.valores_true == ['Fotos']:
            pass
            # Bot(tarefa='fotos', turmas=parâmetros.turmas_selecionadas, seleção=seleção)


    def _verificar_estatística(self):
        self.bt_sondagem_emergencial.atualizar_visibilidade(len(parâmetros.turmas_disponíveis) == 0)
        if len(parâmetros.turmas_disponíveis) == 0:
            self._bt_iniciar.mudar_cor('grey')
        if len(parâmetros.turmas_disponíveis) > 0:
            self._bt_iniciar.mudar_cor('blue')


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


    def _notear(self):
        Bot(tarefa='noteador', seleção=self.seleção, alvos=self._ck_alvos)