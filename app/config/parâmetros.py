import json
import os

from app.config.app_config import DIRETÓRIO_BASE_PADRÃO
from collections import defaultdict
from app.config.prévias import Prévias
ANO = 2025

class Parâmetros:
    def __init__(self):

        self.novo_diretório = DIRETÓRIO_BASE_PADRÃO
        prévias = Prévias(self.novo_diretório)

        self._séries_selecionadas = None
        self._turmas_selecionadas_por_série = None
        self._estado_turmas = {}

        self.__lista_dias_letivos = self.__importar_dias_letivos(self.novo_diretório, ANO)
        self.__dicio_dias_letivos = self._gerar_dict_dias_letivos(self.lista_dias_letivos)
        self.__resumo = prévias.resumo
        self.__nome_ue = prévias.nome_ue
        self.turmas_disponíveis = prévias.turmas

        self.séries_disponíveis = self.__obter_séries(self.turmas_disponíveis)
        self.turmas_disponíveis_por_série = self.__gerar_turmas_por_serie(self.turmas_disponíveis)

        for turma in self.turmas_disponíveis:
            self._estado_turmas[turma] = True

        self._turmas_selecionadas = self.turmas_disponíveis


    @property
    def resumo(self):
        return self.__resumo

    @resumo.setter
    def resumo(self, valor):
        self.__resumo = valor

    @property
    def lista_dias_letivos(self):
        return self.__lista_dias_letivos

    @lista_dias_letivos.setter
    def lista_dias_letivos(self, valor):
        self.__lista_dias_letivos = valor

    @property
    def dicionário_dias_letivos(self):
        return self.__dicio_dias_letivos

    @dicionário_dias_letivos.setter
    def dicionário_dias_letivos(self, valor):
        self.__dicio_dias_letivos = valor

    @property
    def nome_ue(self):
        return self.__nome_ue

    @nome_ue.setter
    def nome_ue(self, valor):
        self.__nome_ue = valor

    @property
    def turmas_selecionadas(self):
        return self._turmas_selecionadas

    @turmas_selecionadas.setter
    def turmas_selecionadas(self, value):
        self._turmas_selecionadas = value
        self._séries_selecionadas = self.__obter_séries(value)
        self._turmas_selecionadas_por_série = self.__gerar_turmas_por_serie(value)

    @property
    def séries_selecionadas(self):
        return self._séries_selecionadas

    @property
    def turmas_selecionadas_por_série(self):
        return self._turmas_selecionadas_por_série

    @staticmethod
    def __gerar_turmas_por_serie(lista_turmas: list[str]) -> dict[str, list[str]] :
        turmas_por_serie = defaultdict(list)

        for turma in lista_turmas :

            serie = ''.join(filter(str.isdigit, turma))
            if serie :
                turmas_por_serie[serie].append(turma)

        return {serie : sorted(turmas) for serie, turmas in sorted(turmas_por_serie.items())}

    @staticmethod
    def __obter_séries(lista_turmas) -> list[str] :
        lista_turmas

        series_unicas = sorted(set(turma[0] for turma in lista_turmas)) 
        return series_unicas

    @staticmethod
    def __importar_dias_letivos(path, ano):
        _path = os.path.join(path, 'fonte', f'Dias Letivos {ano}.json')
        try:
            with open(_path, 'r', encoding='utf-8') as arquivo:
                dias_letivos = json.load(arquivo)
                return dias_letivos
        except FileNotFoundError as e:
            print(f'Erro em {e}')
            return []


    @staticmethod
    def _gerar_dict_dias_letivos(lista) :
        dias_splitados = [dia.split('/') for dia in lista]
        lista_meses = [dia[1] for dia in dias_splitados]
        meses_letivos = list(sorted(set(lista_meses)))

        dicionário = {chave : [dia[0] for dia in dias_splitados if dia[1] == chave] for chave in meses_letivos}

        for chave, índice in dicionário.items() :
            print(f'{chave} : {índice}')

        return dicionário


parâmetros = Parâmetros()
