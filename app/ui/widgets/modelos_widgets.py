from typing import Any

from app.config.parâmetros import parâmetros
from app.ui.widgets import Texto, Botão, Input


def frame_feedback(self_tela, extra: Any | None = None) -> Texto:
    #todo: adicionar lógica de kwargs
    txt = ''
    if extra:
        txt = extra

    widget = Texto(
        self_tela,
        texto=txt,
        fonte=('arial', 20),
        y=400 - 5,
        altura=100,
        largura=self_tela.controller.largura - 10
    )
    return widget

def botão_back(self_tela, destino: str | None = 'inicial') -> Botão:
    #todo: recuperar a lógica de stack/histórico
    widget = Botão(
        self_tela,
        função=lambda : self_tela.controller.alternador.abrir(destino),
        texto='←',
        fonte=('Arial', 20),
        formato='bold',
        x=10,
        y=10
    )
    return widget

def campo_input(self_tela) -> Input:
    campo = Input(
        self_tela,
        texto=parâmetros.diretório_base,
        fonte=('arial', 15),
        x=160,

        y=self_tela.primeira_linha or 180,
        largura=435
    )
    return campo
