from App.frontend.screens.telabot import TelaBot
from App.frontend.screens.telaconsulta import TelaConsulta
from App.frontend.screens.telainicial import TelaInicial


class AlternadorDeTelas:
    def __init__(self, container, controller):
        self.container = container
        self.controller = controller
        self.telas_ativas = {
            'inicial': TelaInicial,
            'bot': TelaBot,
            'consulta': TelaConsulta
        }


    def abrir(self, nome_tela):
        for widget in self.container.winfo_children():
            widget.destroy()

        if nome_tela not in self.telas_ativas:
            raise ValueError(f"Tela '{nome_tela}' não registrada.")

        tela_classe = self.telas_ativas[nome_tela]
        tela_classe(self.container, self.controller)
