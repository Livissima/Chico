#app/ui/screens/telas_bot/tela_bot_servidores.py
from customtkinter import CTkFrame, CTk

from app.auto.bot import Bot

from app.config.parâmetros import parâmetros
from app.ui.config.registrodetelas import RegistradorDeTelas
from app.ui.widgets import Botão


# from app.ui.config.cabeçalhos import Cabeçalhos



@RegistradorDeTelas.registrar(
    nome_tela='telas_bot servidores',
    título_da_janela='Servidores',
    cabeçalho='Servidores',
    descrição='Dossiê de servidores'
)
class TelaBotServidores(CTkFrame):
    def __init__(self, master, controller: "Janela") :
        super().__init__(master)
        self.master: CTk = master
        self.controller  = controller

        self._inserir_widgets()

    def _inserir_widgets(self):

        self.__inserir_botões()
        self.__inserir_textos()
        self.__inserir_checkboxes()
        self.__inserir_inputs()
        self.__inserir_dropdowns()


    def __inserir_textos(self):
        pass



    def __inserir_dropdowns(self):
        pass

    def __inserir_checkboxes(self):
        pass

    def __inserir_inputs(self):
        pass

    def __inserir_botões(self):
        self.bt_iniciar = Botão(
            self,
            função=lambda: Bot(tarefa='servidores', parâmetros_web=None, path=parâmetros.diretório_base),
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

