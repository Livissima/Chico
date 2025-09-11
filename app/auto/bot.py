import concurrent.futures
import threading
from typing import Literal
from app.auto.functions.normalizar import remover_acentos, normalizar_dicionário
from app.auto.tasks import ScrapingSige
from app.auto.tasks.downloads import Downloads
from app.auto.tasks.gerenciaracessos import GerenciarAcessos
from app.auto.tasks.presenciamento import Presenciamento
from selenium import webdriver
from app.auto.data.misc.parâmetroswebdriver import ParâmetrosWebdriver
from app.auto.tasks.sondagem import Sondagem



class Bot:
    def __init__(
            self,
            tarefa: Literal['downloads', 'siap', 'gerenciar', 'sondagem', 'fotos'],
            kwargs_tarefa: dict | None = None,
            **kwargs
    ):

        print(f'Bot instanciado para a task "{tarefa}"')

        self._tarefa = remover_acentos(tarefa)
        self._kwargs_tarefa = normalizar_dicionário(kwargs_tarefa)
        self._kwargs_planos = normalizar_dicionário(kwargs)
        self.navegador = None
        #todo: Desativado temporariamente para testes.
        self._executar_tarefa(tarefa)
        # self.thread_bot = threading.Thread(target=lambda: self._executar_tarefa(tarefa), daemon=False).start()

    def _obter_parâmetros(self, chave: str) -> dict:
        _chave = remover_acentos(chave)
        return self._kwargs_tarefa.get(_chave) or self._kwargs_planos


    def _executar_tarefa(self, tarefa):
        wd_settings = ParâmetrosWebdriver().impressão
        self.navegador = webdriver.Chrome(wd_settings)

        def argumentos(_tarefa):
            parâmetros = self._obter_parâmetros(_tarefa)
            arg_path = parâmetros.get('path')
            arg_turmas = parâmetros.get('turmas')
            arg_destino = parâmetros.get('destino')
            arg_alvos = parâmetros.get('alvos')
            arg_path_database = parâmetros.get('path_database')
            arg_tipo = parâmetros.get('tipo')

            kwargs = {
                'navegador': self.navegador,
                'path' : arg_path,
                'turmas' : arg_turmas,
                'destino' : arg_destino,
                'alvos' : arg_alvos,
                'path_database' : arg_path_database,
                'tipo' : arg_tipo
            }
            return kwargs

        tarefas = {
            'fotos' : lambda: ScrapingSige(**argumentos(tarefa)),
            'siap' : lambda: Presenciamento(**argumentos(tarefa)),
            'sondagem' : lambda: Sondagem(**argumentos(tarefa)),
            'downloads' : lambda: Downloads(**argumentos(tarefa)),
            'gerenciar' : lambda: GerenciarAcessos(**argumentos(tarefa)),
        }

        return tarefas[tarefa]()


    def __getattr__(self, item):
        if self.navegador:
            return getattr(self.navegador, item)
        raise AttributeError(f"'{self.__class__.__name__}' não contém atributo '{item}' (navegador não inicializado).")

if __name__ == '__main__':
    Bot(tarefa='sondagem')
