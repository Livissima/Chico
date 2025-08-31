from typing import TYPE_CHECKING

from customtkinter import CTkFrame, CTk

from ..config.cabeçalhos import Cabeçalhos
from ..config.parâmetros import parâmetros
from ..utils.prévias import Prévias
from ..widgets import Texto, Botão

if TYPE_CHECKING:
    from .janela import Janela


class TelaEstatísticas(CTkFrame):
    def __init__(self, master, controller: "Janela"):
        super().__init__(controller)
        self._bt_desfazer = None
        self.master: CTk = master
        self.controller = controller
        # self.controller.novo_diretório = self._in_diretório_base.valor

        self._configurar_layout()
        self._inserir_widgets()

    def _configurar_layout(self) :
        Cabeçalhos(self, 'estatísticas')

    def _inserir_widgets(self):
        self.primeira_linha = 180
        self.segunda_linha = 350

        self.__inserir_textos()
        self.__inserir_inputs()

        self.__inserir_botões()

    def __inserir_textos(self):
        self.tx_estatísticas = Texto(
            self,
            textos_empilhados=list(self.estatísticas().keys()),
            altura=30
        )
        pass

    def __inserir_inputs(self):
        pass

    def __inserir_botões(self):
        self.bt_back = Botão(
            self,
            função=lambda: self.controller.alternador.abrir('inicial'),
            texto='←',
            fonte=('Arial', 20),
            formato='bold',
            x=10,
            y=10,
        )

    @staticmethod
    def estatísticas():
        resumo = Prévias(parâmetros.novo_diretório).resumo
        return {
            "Turmas:" : resumo['Turmas'],
            "Composições:" : resumo["Composições"],
            "Turnos:" : resumo["Turnos"],
            "Atendimentos:" : resumo["Tipos"],
            "Excedente autorizado": resumo["Excedente autorizado"],
            "Capacidade física" : resumo["Capacidade física"],
            "Capacidade legal" : resumo["Capacidade legal"],
            "Capacidade Total" : resumo["Capacidade Total"],
            "Efetivados" : resumo["Efetivados"],
            "Vagas disponíveis" : resumo["Vagas disponíveis"],
            "Vagas absolutas" : resumo["Vagas absolutas"],
            "Balanço Físico" : resumo["Balanço Físico"],
            "Balanço absoluto" : resumo["Balanço absoluto"],
        }
