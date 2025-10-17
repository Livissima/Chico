from typing import Literal
from app.auto.functions.normalizar import normalizar_unicode, normalizar_dicionário
from app.auto.tasks import ScrapingSige, ConsultaDiasLetivos
from app.auto.tasks.downloads import Downloads
from app.auto.tasks.credenciador.credenciador import Credenciador
from app.auto.tasks.frequenciador.frequenciador import Frequenciador
from selenium import webdriver

from app.auto.tasks.obtençãodemodulação import ObtençãoDeModulação
from app.auto.tasks.sondagem import Sondagem



class Bot:
    def __init__(
            self,
            tarefa: Literal[
                'downloads', 'siap', 'credenciar', 'sondagem', 'fotos', 'consultar dias letivos',
                'obter modulações'
            ],
            kwargs_tarefa: dict | None = None,
            **kwargs
    ):

        print(f'Bot instanciado para a task "{tarefa}"')

        self._tarefa = normalizar_unicode(tarefa)
        self._kwargs_tarefa = normalizar_dicionário(kwargs_tarefa)
        self._kwargs_planos = normalizar_dicionário(kwargs)
        self.navegador = None
        #todo: Desativado temporariamente para testes.
        self._executar_tarefa(tarefa)
        # self.thread_bot = threading.Thread(target=lambda: self._executar_tarefa(tarefa), daemon=False).start()

    def _obter_parâmetros(self, chave: str) -> dict:
        _chave = normalizar_unicode(chave)
        return self._kwargs_tarefa.get(_chave) or self._kwargs_planos


    def _executar_tarefa(self, tarefa):
        self.navegador = webdriver.Chrome()

        argumentos = self._argumentos

        tarefas = {
            'fotos' : lambda: ScrapingSige(**argumentos(tarefa)),
            'siap'  : lambda: Frequenciador(**argumentos(tarefa)),
            'sondagem'  : lambda: Sondagem(**argumentos(tarefa)),
            'downloads' : lambda: Downloads(**argumentos(tarefa)),
            'credenciar' : lambda: Credenciador(**argumentos(tarefa)),
            'consultar dias letivos' : lambda: ConsultaDiasLetivos(**argumentos(tarefa)),
            'obter modulações' : lambda: ObtençãoDeModulação(**argumentos(tarefa))
        }

        return tarefas[tarefa]()


    def _argumentos(self, _tarefa):
        def obter(argumento):
            parâmetros = self._obter_parâmetros(_tarefa)
            return parâmetros.get(argumento)

        kwargs = {
            'navegador': self.navegador,
            'path' : obter('path'),
            'turmas' : obter('turmas'),
            'destino' : obter('destino'),
            'alvos' : obter('alvos'),
            'path_database' : obter('path_database'),
            'tipo' : obter('tipo'),
            'ano' : obter('ano'),
            'data inicial' : obter('data_inicial'),
            'data final' : obter('data final')
        }
        return kwargs

    def __getattr__(self, item):
        if self.navegador:
            return getattr(self.navegador, item)
        raise AttributeError(f"'{self.__class__.__name__}' não contém atributo '{item}' (navegador não inicializado).")

