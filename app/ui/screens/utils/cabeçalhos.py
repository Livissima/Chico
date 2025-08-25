from customtkinter import CTkFrame

from app.__metadata__ import PROJECT_NAME, PROJECT_VERSION
from app.ui.widgets import Texto

class Cabeçalhos:
    def __init__(self, master_tela, tela: str):
        self.master = master_tela
        self.tela = tela

        self.cabeçalhar(tela)


    def cabeçalhar(self, tela):
        config = {
            'inicial' : self.inicial,
            'bot' : self.bot,
            'consulta' : self.consulta,
            'bot sige' : self.bot_sige
        }
        setar = config[tela]

        self.master.controller.title(f'{setar['título']}')
        self.master.título = Texto(
            self.master.master,
            controller=self.master.controller,
            texto=setar['cabeçalho'],
            fonte=('times new roman', 30),
            x=0,
            y=0,
            altura=35,
            largura=self.master.controller.largura
        )
        self.master.título = Texto(
            self.master.master,
            controller=self.master.controller,
            texto=setar['descrição'],
            fonte=('Arial', 15),
            x=0,
            y=29,
            altura=25,
            largura=self.master.controller.largura
        )


    @property
    def inicial(self):
        return {
            'título' : f'{PROJECT_NAME}    v.{PROJECT_VERSION}',
            'cabeçalho' : f'{PROJECT_NAME}',
            'descrição' : 'Auxílio administrativo'
        }

    @property
    def bot(self):
        return {
            'título' : f'{PROJECT_NAME} - Bot',
            'cabeçalho' : 'BOT',
            'descrição' : 'Automação de tarefas'
        }

    @property
    def consulta(self):
        return {
            'título' : f'{PROJECT_NAME} - Consulta',
            'cabeçalho' : '----',
            'descrição' : '--'
        }

    @property
    def bot_sige(self):
        return {
            'título' : f'{PROJECT_NAME} - Bot SIGE',
            'cabeçalho' : 'BOT SIGE',
            'descrição' : 'Automação de tarefas'
        }