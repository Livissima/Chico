from typing import Literal

from app.ui.screens.tela_estatísticas import TelaEstatísticas
from app.ui.screens.telas_bot.tela_bot_inicial import TelaBot
from app.ui.screens.telas_bot.tela_bot_credenciais import TelaBotCredenciais
from app.ui.screens.telas_bot.tela_bot_siap import TelaBotSiap
from app.ui.screens.telas_bot.tela_bot_sige import TelaBotSige
from app.ui.screens.tela_consulta import TelaConsulta
from app.ui.screens.tela_inicial import TelaInicial


class AlternadorDeTelas:
    def __init__(self, container, controller):
        self.container = container
        self.controller = controller

        self.telas_ativas = {
            'inicial': TelaInicial,
            'telas_bot': TelaBot,
            'consulta': TelaConsulta,
            'telas_bot sige' : TelaBotSige,
            'telas_bot google' : TelaBotCredenciais,
            'telas_bot siap' : TelaBotSiap,
            'estatísticas' : TelaEstatísticas
        }


    def abrir(self, nome_tela: Literal[
        'inicial', 'telas_bot', 'consulta', 'telas_bot sige', 'telas_bot google', 'telas_bot siap', 'estatísticas'
    ]
              ):
        for widget in self.container.winfo_children():
            widget.destroy()

        if nome_tela not in self.telas_ativas:
            raise ValueError(f"Tela '{nome_tela}' não registrada.")

        tela_classe = self.telas_ativas[nome_tela]
        tela_classe(self.container, self.controller)
