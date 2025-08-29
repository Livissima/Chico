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
            'telas_bot' : self.bot,
            'consulta' : self.consulta,
            'telas_bot sige' : self.bot_sige,
            'telas_bot credenciais': self.bot_credenciais
        }
        setar = config[tela]

        self.master.controller.title(f'{setar['título']}')

        self.master.título = Texto(
            self.master,
            texto=setar['cabeçalho'],
            fonte=('times new roman', 30),
            x='centro',
            y=0,
            altura=45,
            largura=self.master.controller.largura-10
        )
        self.master.título = Texto(
            self.master,
            texto=setar['descrição'],
            fonte=('Arial', 15),
            x='centro',
            y=40,
            altura=30,
            largura=self.master.controller.largura-10
        )


    @property
    def inicial(self):
        return {
            'título' : f'{PROJECT_NAME}    v.{PROJECT_VERSION}',
            'cabeçalho' : f'{PROJECT_NAME}',
            'descrição' : 'Utilitário administrativo'
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

    @property
    def bot_credenciais(self):
        return {
            'título' : f'{PROJECT_NAME} - Bot Credenciais',
            'cabeçalho' : 'BOT Credenciais',
            'descrição' : 'Gerenciamento automático de credenciais'
        }