from app.auto.tasks.registrotasks import RegistroTasks
from app.config.parâmetros import parâmetros
from app.config.parâmetros.appdataloader import AppDataLoader
from app.ui.customtkinter.config.carregadordetelas import CarregadorDeTelas
from app.ui.customtkinter.screens.janela import Janela

def main():
    AppDataLoader.carregar_dados(parâmetros)
    RegistroTasks.carregar_tasks()
    CarregadorDeTelas.carregar_telas()
    janela = Janela()
    janela.alternador.abrir('inicial')
    janela.mainloop()

main()
