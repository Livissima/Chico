from app.config.app_config import DIRETÓRIO_BASE_PADRÃO
from collections import defaultdict
from app.ui.utils.prévias import Prévias


class Parâmetros:
    def __init__(self):
        self._séries_selecionadas = None
        self._turmas_selecionadas_por_série = None
        self._estado_turmas = {}
        self.novo_diretório = DIRETÓRIO_BASE_PADRÃO

        self.turmas_disponíveis = Prévias(self.novo_diretório).turmas
        self.séries_disponíveis = self.obter_séries(self.turmas_disponíveis)
        self.turmas_disponíveis_por_série = self.gerar_turmas_por_serie(self.turmas_disponíveis)

        for turma in self.turmas_disponíveis:
            self._estado_turmas[turma] = True

        self._turmas_selecionadas = self.turmas_disponíveis



    @property
    def turmas_selecionadas(self):
        return self._turmas_selecionadas

    @turmas_selecionadas.setter
    def turmas_selecionadas(self, value):
        self._turmas_selecionadas = value
        self._séries_selecionadas = self.obter_séries(value)
        self._turmas_selecionadas_por_série = self.gerar_turmas_por_serie(value)

    @property
    def séries_selecionadas(self):
        return self._séries_selecionadas

    @property
    def turmas_selecionadas_por_série(self):
        return self._turmas_selecionadas_por_série

    @staticmethod
    def gerar_turmas_por_serie(lista_turmas: list[str]) -> dict[str, list[str]] :
        turmas_por_serie = defaultdict(list)

        for turma in lista_turmas :
            # Extrai a série (todos os dígitos no início da string)
            serie = ''.join(filter(str.isdigit, turma))
            if serie :
                turmas_por_serie[serie].append(turma)

        # Converte para dict normal e ordena
        return {serie : sorted(turmas) for serie, turmas in sorted(turmas_por_serie.items())}

    @staticmethod
    def obter_séries(lista_turmas) -> list[str] :
        lista_turmas

        series_unicas = sorted(set(turma[0] for turma in lista_turmas)) 
        return series_unicas

parâmetros = Parâmetros()
