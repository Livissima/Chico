from dataclasses import dataclass


@dataclass
class EstruturaDeSeleção :
    séries_selecionadas: list[str]
    turmas_selecionadas_por_série: dict[str, list[str]]