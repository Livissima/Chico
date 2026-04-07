import concurrent.futures
import threading

from app.auto.tasks.taskregistry import TaskRegistry
from app.config.parâmetros import parâmetros
from app.config.parâmetros.appdataloader import AppDataLoader
from app.ui.config.carregadordetelas import CarregadorDeTelas
from app.ui.screens.janela import Janela

def main():
    AppDataLoader.carregar_tudo(parâmetros)
    TaskRegistry.carregar_tasks()
    CarregadorDeTelas.carregar_telas()
    app = Janela()
    app.alternador.abrir('inicial')    #repetido
    app.mainloop()
main()
