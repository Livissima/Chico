import os.path
from pathlib import Path

from customtkinter import CTkFrame, CTk
from platformdirs import user_documents_dir

from app.auto.bot import Bot

from app.config.app_config import DIRETÓRIO_BASE_PADRÃO
from app.ui.config.parâmetros import parâmetros
from app.ui.functions.desfazimento import Desfazimento
from app.ui.widgets import Botão, Input, CheckBox, Texto
from typing import TYPE_CHECKING

from app.ui.config.cabeçalhos import Cabeçalhos
from app.ui.functions.pesquisa_diretório import PesquisaDiretório

if TYPE_CHECKING:
    from app.ui.screens.janela import Janela


class TelaBotSige(CTkFrame):
    def __init__(self, master, controller: "Janela"):
        super().__init__(master)
        self.master: CTk = master
        self.controller = controller

        self._configurar_layout()
        self._inserir_widgets()

    @property
    def _kwargs(self):
        alvos = self._ck_alvos.valor()
        alvos = [chave.lower() for chave, valor in alvos.items() if valor]
        return {
            'destino' : parâmetros.novo_diretório,
            'alvos' : alvos
        }

    def _configurar_layout(self):
        Cabeçalhos(self, 'telas_bot sige')

    def _inserir_widgets(self):
        self.__inserir_checkboxes()
        self.__inserir_textos()
        self.__inserir_inputs()
        self.__inserir_botões()
        # self.__inserir_dropdowns()

    def __inserir_textos(self):
        # self._tx_intro = Texto(
        #     self,
        #     texto='Diretório selecionado:',
        #     fonte=('arial', 15),
        #     formato='bold',
        #     y=200,
        #     largura=self.controller.largura-5,
        # )

        self._tx_feedback = Texto(
            self,
            texto='',
            fonte=('arial', 20),
            y=400-5,
            altura=100,
            largura=self.controller.largura-10,
        )

    def __inserir_inputs(self):
        self._in_diretório_base = Input(
            self,
            texto=str(os.path.join(parâmetros.novo_diretório, 'fonte')),
            fonte=('arial', 15),
            x=120,
            y=135,
            altura=28,
            largura=420+55
        )

    def __inserir_botões(self):
        def back():
            self.salvar_valores_checkboxes()
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

        self._bt_localizar_dados = Botão(
            self,
            texto='Definir pasta',
            fonte=('times new roman', 15),
            formato='bold',
            x=5,
            y=136,
            função=self.pesquisar_pasta_dados,
            altura=25,
            largura=100
        )

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
            condição=parâmetros.novo_diretório != DIRETÓRIO_BASE_PADRÃO,
            texto='↩',
            fonte=('arial', 25),
            x=560,
            y=135+30
        )

        self.bt_sondagem_emergencial = Botão(
            self,
            função=lambda: Bot(tarefa='sondagem', path=parâmetros.novo_diretório),
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
        self.salvar_valores_checkboxes()

        if self._ck_alvos.valores_true == []:
            self._tx_feedback.att('Selecione ao menos um conteúdo alvo.')
            print(f'selecione ao menos um conteúdo alvo')

        if any(alvo in self._ck_alvos.valores_true for alvo in ['Fichas', 'Contatos', 'Situações', 'Gêneros']):
            print(f'____Downloads: {self._ck_alvos.valores_true}')
            Bot(tarefa='downloads', destino=self._kwargs['destino'], alvos=self._kwargs['alvos'])

        if self._ck_alvos.valores_true == ['Fotos']:
            print(f'____Fotos')
            Bot(tarefa='fotos', turmas=parâmetros.turmas_selecionadas)


    def _verificar_estatística(self):
        self.bt_sondagem_emergencial.atualizar_visibilidade(len(parâmetros.turmas_disponíveis) == 0)
        if len(parâmetros.turmas_disponíveis) == 0:
            self._bt_iniciar.mudar_cor('grey')
        if len(parâmetros.turmas_disponíveis) > 0:
            self._bt_iniciar.mudar_cor('blue')

    def _desfazer(self):
        Desfazimento(self).desfazer()
        self._bt_desfazer.atualizar_visibilidade(
            parâmetros.novo_diretório != DIRETÓRIO_BASE_PADRÃO
        )
        self._verificar_estatística()

    def sondar(self):
        Bot(tarefa='sondagem', path=parâmetros.novo_diretório)
        self._verificar_estatística()

    def salvar_valores_checkboxes(self):
        valores = self._ck_turmas.valor()
        parâmetros._estado_turmas = valores
        turmas_selecionadas = [turma for turma, selecionada in valores.items() if selecionada]
        parâmetros.turmas_selecionadas = turmas_selecionadas


