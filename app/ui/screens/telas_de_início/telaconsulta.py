import os.path
from pathlib import Path
from typing import TYPE_CHECKING
from customtkinter import CTk, CTkFrame

from app.config.settings.functions import truncar_diretório
from app.core import ConsultaEstudantes, Exportação
from app.core.query.servidores.consultaservidores import ConsultaServidores
from app.core.utils.pastador import Pastador
from app.config.parâmetros import parâmetros
from app.ui.config.registrotelas import RegistroTelas

from app.ui.widgets.modelos_widgets import frame_feedback, botão_back
from app.ui.widgets.botão import Botão

if TYPE_CHECKING:
    from app.ui.screens.janela import Janela
    pass


@RegistroTelas.registrar(
    nome_tela='consulta',
    título_da_janela='Consulta',
    cabeçalho='Consulta',
    descrição='Leitura e processamento de JSONs para gerar database'
)
class TelaConsulta(CTkFrame):
    #todo: aprimorar o widget de feedback da consulta, que continua consultando
    # quando o código crasha

    def __init__(self, master: CTk, controller: "Janela"):
        super().__init__(master)
        self.master: CTk = master
        self.controller = controller

        self._inserir_widgets()


    def _inserir_widgets(self):
        self.__inserir_botões()
        self.__inserir_textos()
        self.__iserir_inputs()

    def __inserir_textos(self):
        self._tx_feedback = frame_feedback(self, self._obter_situação()['novo_texto'])
        self._tx_feedback.atualizar(**self._obter_situação())

    def __inserir_botões(self):

        self._bt_consultar_estudantes = Botão(
            self,
            função=lambda: self._consultar_estudantes(),
            texto='ESTUDANTES',
            fonte=('times new roman', 20),
            formato='bold',
            largura=(larg := 250),
            x=(self.controller.largura - larg) // 2,
            y=250,
            altura=35
        )

        self._bt_consultar_servidores = Botão(
            self,
            função=lambda: self._consultar_servidores(),
            texto='SERVIDORES',
            fonte=('times new roman', 20),
            formato='bold',
            largura=(larg := 250),
            x=(self.controller.largura - larg) // 2,
            y=300,
            altura=35
        )

        self._bt_back = botão_back(self)

    def __iserir_inputs(self):
        pass

    def _consultar_estudantes(self):
        diretório_base = parâmetros.diretório_base
        fonte = str(os.path.join(diretório_base, 'fonte'))

        self._tx_feedback.atualizar('Consultando estudantes')
        try:
            consulta = ConsultaEstudantes(diretório_fonte=fonte)

            self._tx_feedback.atualizar('Exportando')

            Exportação(consulta=consulta, path_destino=diretório_base)

            Pastador(diretório_base=diretório_base)

            self._tx_feedback.atualizar(
                f'Planilhas geradas e exportadas para\n{diretório_base}',
                ('Arial', 20),
                'bold',
                'light green'
            )

        except Exception as e:
            self._tx_feedback.atualizar(f'Erro ao consultar: {e}')
            raise Exception(f'Problema na consulta: {e}')

    def _consultar_servidores(self) :
        diretório_base = parâmetros.diretório_base
        fonte = str(Path(diretório_base, 'fonte', 'Servidores'))

        self._tx_feedback.atualizar('Consultando servidores')

        try :
            consulta = ConsultaServidores(diretório_fonte=fonte)

            self._tx_feedback.atualizar('Exportando')

            Exportação(consulta=consulta, path_destino=diretório_base)

            self._tx_feedback.atualizar(
                f'Planilhas geradas e exportadas para\n{diretório_base}',
                ('Arial', 20),
                'bold',
                'light green'
            )

        except Exception as e :
            self._tx_feedback.atualizar(f'Erro ao consultar: {e}')
            raise Exception(f'Problema na consulta: {e}')
            # except FileNotFoundError: self._tx_feedback.att('Erro ao consultar')
        pass


    @staticmethod
    def _obter_situação():

        diretório = str(Path(parâmetros.diretório_base, 'fonte'))
        diretório_truncado = truncar_diretório(diretório)

        if len(diretório) > 60 :
            diretório_display = diretório_truncado

        else :
            diretório_display = diretório

        msg_diretório_existente = {
                'novo_texto' : f'A consulta será realizada a partir do diretório:\n{diretório_display}',
                'fonte' : ('arial', 20),
                'cor' : 'light green',
                'formato' : 'bold'
            }

        msg_diretório_inexistente = {
                'novo_texto' : f'Diretório não encontrado neste computador:\n'
                               f''f'{diretório_display}\nVocê já executou o Bot de Downloads?',
                'cor' : 'orange',
                'fonte' : ('arial', 18)
            }



        if Path(diretório).exists():
            return msg_diretório_existente

        else:
            #todo: rever a condição para considerar a existência dos jsons correspondentes, não do diretório
            return msg_diretório_inexistente
