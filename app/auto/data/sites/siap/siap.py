from app.auto.data.sites.siap.caminhos import Caminhos
from app.auto.data.sites.siap.css_selectors import CssSelectors
from app.auto.data.sites.siap.ids import Ids
from app.auto.data.sites.siap.urls import Urls
from app.auto.data.sites.siap.xpaths import Xpaths
from app.config.env_config import CREDENCIAIS_SIAP


class Siap:

    @property
    def url(self):
        return Urls().url_principal

    @property
    def credenciais(self):
        return CREDENCIAIS_SIAP

    @property
    def xpaths(self) -> dict:
        return Xpaths().xpaths

    @property
    def ids(self) -> dict[str, str]:
        return Ids().ids

    @property
    def caminhos(self) -> dict[str, list[tuple]]:
        return Caminhos().caminhos

    @property
    def css_selectors(self) -> dict[str, str]:
        return CssSelectors().css_selectors






