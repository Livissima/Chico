# from dataclasses import dataclass
# from os import PathLike
# from typing import List, Dict
#
# from app.config.parâmetros.getters.turmasséries import TurmasSéries
#
#
# @dataclass(frozen=True)
# class ConfiguraçãoBase :
#     diretorio_base: str | PathLike
#     ano_letivo: int
#     nome_ue: str
#     turmas_disponiveis: tuple[str]
#     series_disponiveis: tuple[str]
#     lista_dias_letivos: tuple
#     dicionario_dias_letivos: dict
#     modulacoes: dict
#     resumo: dict
#
#
# class GerenciadorEstado :
#     def __init__(self, config_base: ConfiguraçãoBase) :
#         self.config_base = config_base
#         self._turmas_selecionadas = list(config_base.turmas_disponiveis)
#         self._series_selecionadas = self._calcular_series_selecionadas()
#         self._turmas_por_serie = self._calcular_turmas_por_serie()
#
#     def _calcular_series_selecionadas(self) -> List[str] :
#         return TurmasSéries.gerar_lista_de_séries(self._turmas_selecionadas)
#
#     def _calcular_turmas_por_serie(self) -> Dict[str, List[str]] :
#         return TurmasSéries.gerar_dicionário_turmas_por_série(self._turmas_selecionadas)
#
#     def selecionar_turmas(self, novas_turmas: List[str]) :
#         turmas_invalidas = [t for t in novas_turmas if t not in self.config_base.turmas_disponiveis]
#         if turmas_invalidas :
#             raise ValueError(f"Turmas inválidas: {turmas_invalidas}")
#
#         self._turmas_selecionadas = novas_turmas
#         self._series_selecionadas = self._calcular_series_selecionadas()
#         self._turmas_por_serie = self._calcular_turmas_por_serie()
#
#     @property
#     def turmas_selecionadas(self) -> List[str] :
#         return self._turmas_selecionadas.copy()
#
#     @property
#     def series_selecionadas(self) -> List[str] :
#         return self._series_selecionadas.copy()
#
#     @property
#     def turmas_selecionadas_por_serie(self) -> Dict[str, List[str]] :
#         return self._turmas_por_serie.copy()
