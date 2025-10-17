import json
import os
from collections import defaultdict

from app.config.app_config import DIRETÓRIO_BASE_PADRÃO
from app.config.getters.dias_letivos import DiasLetivos
from app.config.getters.modulação_servidor import ModulaçãoServidor
from app.config.getters.prévias import Prévias
from app.config.getters.séries_letivas import TurmasSéries

#todo dinamizar essa constante com algum getter
ANO_ATUAL = 2025

class Parâmetros:
    def __init__(self):

        self.novo_diretório = DIRETÓRIO_BASE_PADRÃO
        self.prévias = Prévias(self.novo_diretório)

        self._séries_selecionadas = None
        self._turmas_selecionadas_por_série = None
        self._estado_turmas = {}

        self.__lista_dias_letivos = DiasLetivos(self.novo_diretório, ANO_ATUAL).lista_dias_letivos
        self.__dicio_dias_letivos = DiasLetivos(self.novo_diretório, ANO_ATUAL).dicionário_dias_letivos

        self.__modulações = ModulaçãoServidor(self.novo_diretório).modulações

        self.__resumo = self.prévias.resumo
        self.__nome_ue = self.prévias.nome_ue

        self.turmas_disponíveis = self.prévias.turmas

        self.séries_disponíveis = TurmasSéries(self.prévias).lista_séries
        self.turmas_disponíveis_por_série = TurmasSéries(self.prévias).dicionário_turmas_por_série

        for turma in self.turmas_disponíveis:
            self._estado_turmas[turma] = True

        self._turmas_selecionadas = self.turmas_disponíveis


    @property
    def resumo(self) -> dict :
        return self.__resumo

    @resumo.setter
    def resumo(self, valor) -> None:
        self.__resumo = valor

    @property
    def lista_dias_letivos(self) -> list:
        return self.__lista_dias_letivos

    @lista_dias_letivos.setter
    def lista_dias_letivos(self, valor) -> None:
        self.__lista_dias_letivos = valor

    @property
    def dicionário_dias_letivos(self)  -> dict:
        return self.__dicio_dias_letivos

    @dicionário_dias_letivos.setter
    def dicionário_dias_letivos(self, valor) -> None:
        self.__dicio_dias_letivos = valor

    @property
    def nome_ue(self) -> str:
        return self.__nome_ue

    @nome_ue.setter
    def nome_ue(self, valor) -> None:
        self.__nome_ue = valor

    @property
    def modulações(self) -> dict:
        return self.__modulações

    @modulações.setter
    def modulações(self, valor) -> None:
        self.__modulações = valor

    @property
    def turmas_selecionadas(self) -> list[str]:
        return self._turmas_selecionadas

    @turmas_selecionadas.setter
    def turmas_selecionadas(self, value: list[str]) -> None:
        self._turmas_selecionadas = value
        self._séries_selecionadas = TurmasSéries.gerar_lista_de_séries(value)
        self._turmas_selecionadas_por_série = TurmasSéries.gerar_dicionário_turmas_por_série(value)

    @property
    def séries_selecionadas(self) -> list:
        return self._séries_selecionadas

    @property
    def turmas_selecionadas_por_série(self):
        return self._turmas_selecionadas_por_série


parâmetros = Parâmetros()

