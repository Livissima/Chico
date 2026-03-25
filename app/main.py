import concurrent.futures
import threading

from app.config.parâmetros import parâmetros
from app.config.parâmetros.appdataloader import AppDataLoader
from app.ui.config.carregadordetelas import CarregadorDeTelas
from app.ui.screens.janela import Janela
from app.ui.functions.alternadordetelas import AlternadorDeTelas

def main():
    AppDataLoader.carregar_tudo(parâmetros)
    CarregadorDeTelas.carregar_telas()
    app = Janela()
    app.alternador.abrir('inicial')    #repetido
    app.mainloop()
main()
