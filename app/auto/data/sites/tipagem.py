import datetime
from typing import Optional, Dict, Any

class TipagemPropriedades:
    url: Optional[str] = None
    xpaths: Optional[Dict[str, Any]] = None
    caminhos: Optional[Dict[str, Any]] = None
    credenciais: Optional[Dict[str, Any]] = None
    ids: Optional[Dict[str, Any]] = None
    css_selectors: Optional[Dict[str, Any]] = None
    hoje: str
    agora: datetime.datetime
