from app.auto.data.sites.siap.caminhos import Caminhos
from app.auto.data.sites.siap.css_selectors import CssSelectors
from app.auto.data.sites.siap.ids import Ids
from app.auto.data.sites.siap.urls import SiapUrls
from app.auto.data.sites.siap.xpaths import Xpaths
from app.auto.data.dataclasses.siteconfig import SiteConfig
from app.config.settings.env_config import CREDENCIAIS_SIAP

Siap = SiteConfig(
    nome = 'siap',
    urls=SiapUrls().tela_login,
    xpaths=Xpaths().xpaths,
    ids=Ids().ids,
    css_selectors=CssSelectors().css_selectors,
    caminhos=Caminhos().caminhos,
    lista_usuários=CREDENCIAIS_SIAP
)
