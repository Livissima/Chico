from dataclasses import dataclass, field
from typing import List, Optional, Any
import re

@dataclass
class CampoSchema:
    chave: str
    rótulo: str
    tipo: str = 'text'
    largura_coluna: float = 1.0
    obrigatório: bool = False
    cumprimento_mínimo: int | None = None
    cumprimento_máximo: int | None = None
    opções: List[str] = field(default_factory=list)
    valor_padrão: Any = ''
    tipo_dado: str = 'str'

    def validar(self, valor: Any) -> str | None :
        valor_str = str(valor).strip() if valor is not None else ""

        if self.obrigatório and not valor_str:
            return f'O campo {self.rótulo} é obrigatório.'

        if not valor_str:
            return None

        if self.cumprimento_mínimo and len(valor_str) < self.cumprimento_mínimo:
            return f'{self.rótulo} deve ter no mínimo {self.cumprimento_mínimo} caracteres. {len(valor_str)} inseridos.'

        if self.cumprimento_máximo and len(valor) > self.cumprimento_máximo:
            return f'{self.rótulo} deve ter no máximo {self.cumprimento_máximo} caracteres. {len(valor_str)} inseridos.'

        return None

@dataclass
class LinhaFormulário:
    proporções: List[float]
    campos: List[CampoSchema]

@dataclass
class SeçãoFormulário:
    título: str
    linhas: List[LinhaFormulário]