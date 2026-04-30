from dataclasses import dataclass, field
from typing import Any, Literal

from selenium.webdriver.edge.webdriver import WebDriver

from app.auto.data.dataclasses.propriedadesweb import PropriedadesWeb
from app.auto.data.dataclasses.siteconfig import SiteConfig
from app.auto.functions import NavegaçãoWeb


@dataclass
class Navegabilidade:
    site: Literal['sige', 'siap', 'netescola']
    navegador: WebDriver
    propriedades: PropriedadesWeb
    parâmetros_extras: Any
    config: SiteConfig
    navegação_web: NavegaçãoWeb = field(default_factory=NavegaçãoWeb(navegador, config))

