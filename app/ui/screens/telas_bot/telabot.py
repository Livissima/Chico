from typing import TYPE_CHECKING
from customtkinter import CTkFrame, CTk
from app.auto.bot import Bot
from app.config.parâmetros import parâmetros
from app.ui.config.registrotelas import RegistroTelas
from app.ui.widgets.modelos_widgets import frame_feedback, botão_back
from app.ui.widgets import Botão

if TYPE_CHECKING:
    pass
@RegistroTelas.registrar(
    nome_tela='bot',
    título_da_janela='Bot',
    cabeçalho='BOT',
    descrição='Automação de tarefas'
)
class TelaBot(CTkFrame):
    #todo: Bolar um esqueminha de botão que aborte a automação em curso.
    #todo: Elaborar funções para pedir confirmação para executar o auto
    #todo: Inserir dicas flutuantes

    def __init__(self, master: CTk, controller: "Janela"):
        super().__init__(master)
        self.master: CTk = master
        self.controller = controller
        self._inserir_widgets()

    def _inserir_widgets(self):
        self.__inserir_textos()
        self.__inserir_inputs()
        self.__inserir_botões()
        self.__inserir_dropdowns()

    def __inserir_textos(self):
        self._tx_feedback = frame_feedback(self)

    def __inserir_inputs(self):
        pass

    def __inserir_botões(self):
        y = 90
        largura = 130

        self._bt_siap = Botão(
            self,
            #todo flexibilizar esse path
            função=lambda: self.controller.alternador.abrir('bot siap'),
            texto='SIAP',
            fonte=('Arial', 20),
            formato='bold',
            x=10+80,
            y=y,
            largura=largura,
        )

        self._bt_sige = Botão(
            self,
            função=lambda: self.controller.alternador.abrir('bot sige'),
            texto='SIGE',
            fonte=('Arial', 20),
            formato='bold',
            x=10+150+80,
            y=y,
            largura=largura,
        )

        self._bt_credenciais = Botão(
            self,
            função=lambda: self.controller.alternador.abrir('bot credenciais'),
            texto='Credenciais',
            fonte=('Arial', 20),
            formato='bold',
            x=10+150+150+80,
            y=y,
            largura=largura,
        )
        self._bt_servidores = Botão(
            self,
            # função=lambda: self.controller.alternador.abrir('bot_servidores'),
            função=lambda: Bot(tarefa='servidores', parâmetros_web=None, path=parâmetros.diretório_base),
            texto='Servidores',
            fonte=('Arial', 20),
            formato='bold',
            x=10+80,
            y=y+50,
            largura=largura

        )

        self.bt_back = botão_back(self)

    def __inserir_dropdowns(self):
        pass

