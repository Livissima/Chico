from typing import TYPE_CHECKING

from customtkinter import CTkFrame, CTk

from ..config.cabeçalhos import Cabeçalhos
from ..config.parâmetros import parâmetros
from ..utils.prévias import Prévias
from ..widgets import Texto, Botão
from ...auto.bot import Bot

if TYPE_CHECKING:
    from .janela import Janela

class TelaEstatísticas(CTkFrame):
    def __init__(self, master, controller: "Janela"):
        super().__init__(controller)
        self._bt_desfazer = None
        self.master: CTk = master
        self.controller = controller

        self._configurar_layout()
        self._inserir_widgets()

    def _configurar_layout(self) :
        Cabeçalhos(self, 'estatísticas')

    def _inserir_widgets(self):
        self.primeira_linha = 80

        self.__inserir_textos()
        self.segunda_linha = self.primeira_linha + self.tx_valores.altura_somada + self.tx_valores.altura_widget - 15
        self.__inserir_botões()
        self.__inserir_inputs()


    def __inserir_textos(self):
        self.tx_chaves = Texto(
            self,
            textos_empilhados=list(self.estatísticas().keys()),
            largura=200,
            altura=20,
            formato='bold',
            anchor='w',
            # compound='top',
            x=10,
            y=self.primeira_linha
        )

        _x = 190
        largura = self.controller.largura - _x - 5

        self.tx_valores = Texto(
            self,
            textos_empilhados=['-' for chave in list(self.estatísticas().keys())],
            largura=largura,
            altura=20,
            x=_x,
            anchor='w',
            y=self.primeira_linha
        )

        self.tx_valores = Texto(
            self,
            textos_empilhados=list(self.estatísticas().values()),
            largura=largura,
            altura=20,
            x=_x,
            anchor='w',
            y=self.primeira_linha
        )

    def __inserir_inputs(self):
        pass

    def __inserir_botões(self):
        self.bt_sondar = Botão(
            self,
            função=lambda: self.sondar(),
            texto='Atualizar',
            fonte=('times new roman', 20),
            formato='bold',
            y=self.segunda_linha,
            largura=100
        )

        self.bt_back = Botão(
            self,
            função=lambda: self.controller.alternador.abrir('inicial'),
            texto='←',
            fonte=('Arial', 20),
            formato='bold',
            x=10,
            y=10
        )

    def sondar(self):
        Bot(tarefa='sondagem', path=parâmetros.novo_diretório),
        self.controller.alternador.abrir('estatísticas')

    @staticmethod
    def estatísticas():
        resumo = Prévias(parâmetros.novo_diretório).resumo
        chaves = [
            "Composições", "Turnos", "Tipos", "Excedente autorizado", "Excedente ocupado", "Capacidade física",
            "Capacidade legal", "Capacidade Total", "Efetivados", "Vagas disponíveis", "Vagas absolutas",
            "Balanço Físico", "Balanço absoluto", "Turmas Ativas"
        ]

        return {f"{chave}:" : resumo.get(chave, "__ERRO__") for chave in chaves}
