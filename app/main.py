import concurrent.futures
import threading

from app.config.parâmetros import parâmetros
from app.config.parâmetros.appdataloader import AppDataLoader
from app.ui.screens.janela import Janela
from app.ui.functions.alternadordetelas import AlternadorDeTelas

def main():
    AppDataLoader.carregar_tudo(parâmetros)
    app = Janela()
    alternador = AlternadorDeTelas(app.container, app)
    alternador.abrir('inicial')

main()
