from pathlib import Path
from dataclasses import dataclass, field
from typing import Dict, List, Any
from app.config.settings.app_config import DIRETÓRIO_BASE_PADRÃO
from .getters.turmasséries import TurmasSéries

ANO_ATUAL = 2026


@dataclass
class Parâmetros :
    diretório_base: Path
    nome_ue: str = ""
    turmas_disponíveis: List[str] = field(default_factory=list)
    séries_disponíveis: List[str] = field(default_factory=list)
    turma_por_série: Dict[str, List[str]] = field(default_factory=dict)

    turmas_selecionadas: List[str] = field(default_factory=list)
    estado_checkbox_turmas: Dict[str, bool] = field(default_factory=dict)
    estado_checkbox_alvos: Dict[str, bool] = field(default_factory=dict)

    lista_dias_letivos: List[str] = field(default_factory=list)
    dicionário_dias_letivos: Dict[str, List[str]] = field(default_factory=dict)
    modulações: Dict[str, Any] = field(default_factory=dict)

    resumo: Dict[str, Any] = field(default_factory=dict)

    @property
    def séries_selecionadas(self) -> list :
        return TurmasSéries.gerar_lista_de_séries(self.turmas_selecionadas)

    @property
    def turmas_selecionadas_por_série(self) -> dict :
        return TurmasSéries.gerar_dicionário_turmas_por_série(self.turmas_selecionadas)


parâmetros = Parâmetros(diretório_base=Path(DIRETÓRIO_BASE_PADRÃO))