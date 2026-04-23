from typing import Optional, Dict, List, Tuple
from dataclasses import dataclass, field

@dataclass(frozen=True)
class Credenciais:
    id: str
    senha: str
    tipo: Optional[str] = None


@dataclass
class SiteConfig:
    nome: str
    urls: str
    xpaths: Dict = field(default_factory=dict)
    ids: Dict = field(default_factory=dict)
    css_selectors: Dict = field(default_factory=dict)
    caminhos: Dict[str, List[Tuple]] = field(default_factory=dict)
    credenciais_padrão: Credenciais | None = None
    lista_usuários: Dict[str, Credenciais] | None = None

