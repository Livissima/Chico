from app.auto.data.sites.sige.caminhos import Caminhos
from app.auto.data.sites.sige.css_selectors import CssSelectors
from app.auto.data.sites.sige.ids import Ids
from app.auto.data.sites.sige.urls import Urls
from app.auto.data.sites.sige.xpaths import Xpaths
from app.auto.data.sites.tipagem import SiteConfig
from app.config.settings.env_config import ID_SIGE, SENHA_SIGE


Sige = SiteConfig(
    nome='sige',
    urls=Urls().tela_login,
    xpaths=Xpaths().xpaths,
    ids=Ids().ids,
    css_selectors=CssSelectors().css_selectors,
    caminhos=Caminhos().caminhos,
    credenciais_padrão={'id' : ID_SIGE, 'senha' : SENHA_SIGE}
)
