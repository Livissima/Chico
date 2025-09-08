import os.path

from customtkinter import CTkFrame, CTk
from app.auto.bot import Bot
from app.config.parâmetros import parâmetros
from app.ui.widgets import Botão, CheckBox, Texto
from typing import TYPE_CHECKING

from app.ui.config.cabeçalhos import Cabeçalhos

if TYPE_CHECKING:
    pass

class TelaBotCredenciais(CTkFrame):
    def __init__(self, master, controller: "Janela"):
        super().__init__(master)
        self.master: CTk = master
        self.controller = controller
        # self.pack(expand=True, fill='both')
        self._configurar_layout()
        self._inserir_widgets()

    def _configurar_layout(self):
        Cabeçalhos(self, 'telas_bot credenciais')

    def _inserir_widgets(self):
        self.__inserir_textos()
        self.__inserir_inputs()
        self.__inserir_botões()
        self.__inserir_checkboxes()

    def __inserir_textos(self):
        self._tx_feedback = Texto(
            self,
            texto='',
            fonte=('arial', 20),
            y=400-5,
            altura=100,
            largura=self.controller.largura-10,
        )


    def __inserir_inputs(self):
        pass

    def __inserir_botões(self):
        def back():
            self.salvar_valores_checkboxes()
            self.controller.alternador.abrir('telas_bot')

        self.bt_back = Botão(
            self,
            função=lambda: back(),
            texto='←',
            fonte=('Arial', 20),
            formato='bold',
            x=10,
            y=10,
        )
        y = 350
        self.bt_netescola = Botão(
            # todo: o feedback no console está inacurado.
            self,
            função=lambda: Bot(
                tarefa='gerenciar',
                path_database= os.path.join(parâmetros.novo_diretório, 'Database.xlsx'),
                tipo='netescola',
                turmas=self._ck_turmas.valores_true
            ),
            texto='Netescola',
            largura=100,
            x=150,
            y=y
        )

        self.bt_google = Botão(
            self,
            função=lambda: print('botão google'),
            texto='Google',
            largura=100,
            x=350,
            y=y
        )

    def __inserir_checkboxes(self):
        self._inserir_checkbox_turmas()

    def _inserir_checkbox_turmas(self):

        estado_turmas = {}
        for turma in parâmetros.turmas_disponíveis:
            if hasattr(parâmetros, '_estado_turmas') and turma in parâmetros._estado_turmas:
                estado_turmas[turma] = parâmetros._estado_turmas[turma]
            else:
                estado_turmas[turma] = True
        self._ck_turmas = CheckBox(
            self,
            opções=parâmetros.turmas_disponíveis,
            valores_iniciais=estado_turmas
        )

    def salvar_valores_checkboxes(self):
        valores = self._ck_turmas.valor()
        parâmetros._estado_turmas = valores
        turmas_selecionadas = [turma for turma, selecionada in valores.items() if selecionada]
        parâmetros.turmas_selecionadas = turmas_selecionadas
