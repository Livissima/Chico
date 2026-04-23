from customtkinter import CTkFrame, CTk
from typing import TYPE_CHECKING

from app.ui.config.registrotelas import RegistroTelas
# from ..config.cabeçalhos import Cabeçalhos
from app.ui.widgets import Botão, Texto
from app.config.parâmetros import parâmetros
from app.core.frequency.compiladordefaltas import CompiladorDeFaltas

if TYPE_CHECKING :
    from app.ui.screens.janela import Janela

@RegistroTelas.registrar(
    nome_tela='frequência',
    título_da_janela='Frequência',
    cabeçalho='Frequência',
    descrição=parâmetros.nome_ue
)
class Frequência(CTkFrame) :
    def __init__(self, master, controller: "Janela") :
        super().__init__(controller)
        self.master: CTk = master
        self.controller = controller

        self._inserir_widgets()

    def _inserir_widgets(self) :
        self.__inserir_textos()
        self.__inserir_botões()
        self.__inserir_inputs()

    def __inserir_textos(self) :
        self._tx_feedback = Texto(
            self,
            texto=' ',
            fonte=('times new roman', 25),
            y=395, altura=100,
            largura=self.controller.largura - 5
        )

    def __inserir_botões(self) :
        self._bt_back = Botão(
            self,
            função=lambda : self.controller.alternador.abrir('inicial'),
            texto='←',
            fonte=('Arial', 20),
            formato='bold',
            x=10,
            y=10
        )

        self._bt_compilar_faltas = Botão(
            self,
            função=lambda : self._compilar_faltas(),
            texto='Compilar faltas',
            y=300,
            largura=120
        )

    def __inserir_inputs(self) :
        pass

    def _compilar_faltas(self):
        self._tx_feedback.atualizar('Compilando...')

        try:
            CompiladorDeFaltas(parâmetros.diretório_base).exportar()
            self._tx_feedback.atualizar(f"'Compilado de Faltas' gerado com sucesos em \n{parâmetros.diretório_base}")

        except Exception as e:
            print(f'Exception na frequência: {e}')
            self._tx_feedback.atualizar(f'Erro\n{e}', fonte=('arial', 10), cor='red')
            raise e


