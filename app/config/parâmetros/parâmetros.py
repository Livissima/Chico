from os import PathLike
from typing import List, Dict, Optional

from app.config.app_config import DIRETÓRIO_BASE_PADRÃO
from app.config.parâmetros.gerenciadordeestado import GerenciadorEstado
from app.config.parâmetros.iniciadorconfiguraçãobase import IniciadorConfiguraçãoBase


class Parâmetros :
    _instancia = None

    def __init__(self, novo_diretorio: Optional[str | PathLike] = None) :
        if Parâmetros._instancia is not None :
            raise Exception("Singleton! Use Parâmetros.obter()")

        self._diretório_base: PathLike = novo_diretorio or DIRETÓRIO_BASE_PADRÃO

        self._config_base = IniciadorConfiguraçãoBase.configuração(self._diretório_base)
        self._estado = GerenciadorEstado(self._config_base)


    @classmethod
    def obter(cls, novo_diretorio: Optional[str] = None) -> "Parâmetros" :
        if cls._instancia is None :
            # Primeira criação
            diretorio = novo_diretorio or DIRETÓRIO_BASE_PADRÃO
            cls._instancia = cls(diretorio)
        elif novo_diretorio and novo_diretorio != cls._instancia._diretório_base :

            cls._instancia = cls(novo_diretorio)

        return cls._instancia

    @property
    def turmas_selecionadas(self) -> List[str] :
        return self._estado.turmas_selecionadas

    @turmas_selecionadas.setter
    def turmas_selecionadas(self, value: List[str]) :
        self._estado.selecionar_turmas(value)

    @property
    def séries_selecionadas(self) -> List[str] :
        return self._estado.series_selecionadas

    @property
    def turmas_selecionadas_por_série(self) -> Dict[str, List[str]] :
        return self._estado.turmas_selecionadas_por_serie

    @property
    def diretório_base(self) -> PathLike :
        return self._diretório_base

    @property
    def turmas_disponíveis(self) -> tuple[str] :
        return self._config_base.turmas_disponiveis

    @property
    def nome_ue(self) -> str :
        return self._config_base.nome_ue

    @property
    def lista_dias_letivos(self) -> tuple :
        return self._config_base.lista_dias_letivos

    @property
    def dicionário_dias_letivos(self) -> dict :
        return self._config_base.dicionario_dias_letivos

    @property
    def modulações(self) -> dict :
        return self._config_base.modulacoes

    @property
    def resumo(self) -> dict :
        return self._config_base.resumo

parâmetros = Parâmetros.obter()
