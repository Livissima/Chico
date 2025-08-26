from app.ui.screens.telabot import TelaBot
from app.ui.screens.telabot_credenciais import TelaBotCredenciais
from app.ui.screens.telabot_sige import TelaBotSige
from app.ui.screens.telaconsulta import TelaConsulta
from app.ui.screens.telainicial import TelaInicial


class AlternadorDeTelas:
    def __init__(self, container, controller):
        self.container = container
        self.controller = controller
        self.telas_ativas = {
            'inicial': TelaInicial,
            'bot': TelaBot,
            'consulta': TelaConsulta,
            'bot sige' : TelaBotSige,
            'bot google' : TelaBotCredenciais
        }


    def abrir(self, nome_tela):
        for widget in self.container.winfo_children():
            widget.destroy()

        if nome_tela not in self.telas_ativas:
            raise ValueError(f"Tela '{nome_tela}' não registrada.")

        tela_classe = self.telas_ativas[nome_tela]
        tela_classe(self.container, self.controller)
