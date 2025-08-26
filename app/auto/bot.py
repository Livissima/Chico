from typing import Literal
from app.auto.functions.normalizar import remover_acentos, normalizar_dicionário
from app.auto.tasks.downloads import Downloads
from app.auto.tasks.gerenciaracessos import GerenciarAcessos
from app.auto.tasks.presenciamento import Presenciamento
from selenium import webdriver
from app.auto.data.misc.parâmetroswebdriver import ParâmetrosWebdriver


class Bot:
    def __init__(
            self,
            tarefa: Literal['downloads', 'siap', 'gerenciar'],
            kwargs_tarefa: dict | None = None,
            **kwargs
    ):

        print(f'Bot instanciado para a task "{tarefa}"')

        self._tarefa = remover_acentos(tarefa)
        self._kwargs_tarefa = normalizar_dicionário(kwargs_tarefa)
        self._kwargs_planos = normalizar_dicionário(kwargs)
        self.navegador = None

        self._executar_tarefa()

        print(f'Task {tarefa} finalizada')

    def _obter_parâmetros(self, chave: str) -> dict:

        _chave = remover_acentos(chave)
        return self._kwargs_tarefa.get(_chave) or self._kwargs_planos


    def _executar_tarefa(self):
        tarefa = self._tarefa
        tarefas_válidas = {'downloads', 'siap', 'gerenciar'}
        if tarefa not in tarefas_válidas:
            raise KeyError(f'Tarefa inválida para o navegador: {tarefa}')

        if tarefa == 'downloads':
            parâmetros = normalizar_dicionário(self._obter_parâmetros('downloads'))

            pasta_destino = parâmetros.get('destino')
            alvos = parâmetros.get('alvos')

            if not pasta_destino or not alvos:
                raise ValueError('Necessário informar destino e alvos')

            if isinstance(alvos, str):
                alvos = [alvo.strip() for alvo in alvos.split(',') if alvo.strip()]

            wd_settings = parâmetros.get('webdriver_settings') or ParâmetrosWebdriver().impressão
            self.navegador = webdriver.Chrome(wd_settings)
            Downloads(self.navegador, pasta_destino, *alvos)
            return

        if tarefa == 'siap':
            parâmetros = normalizar_dicionário(self._obter_parâmetros('siap'))
            wd_settings = parâmetros.get('webdriver_settings') or ParâmetrosWebdriver().impressão
            self.navegador = webdriver.Chrome(wd_settings)
            Presenciamento(self.navegador)
            return

        if tarefa == 'gerenciar':
            parâmetros = normalizar_dicionário(self._obter_parâmetros('gerenciar'))
            path_database = parâmetros.get('path_database')
            tipo = parâmetros.get('tipo')
            turma = parâmetros.get('turma')

            if not path_database or not tipo:
                raise ValueError('Necessário informar `path_database` e `tipo`')

            wd_settings = parâmetros.get('webdriver_settings') or ParâmetrosWebdriver().impressão
            self.navegador = webdriver.Chrome(wd_settings)
            GerenciarAcessos(
                navegador=self.navegador,
                path_database=path_database,
                tipo=tipo,
                turma=turma
            )
            return

    def __getattr__(self, item):
        if self.navegador:
            return getattr(self.navegador, item)
        raise AttributeError(f"'{self.__class__.__name__}' não contém atributo '{item}' (navegador não inicializado).")

