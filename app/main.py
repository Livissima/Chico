import concurrent.futures
import threading

from app.ui.screens.janela import Janela
from app.ui.functions.alternadordetelas import AlternadorDeTelas

def main():

    app = Janela()
    alternador = AlternadorDeTelas(app.container, app)
    alternador.abrir('inicial')

main()
