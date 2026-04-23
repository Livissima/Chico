from app.auto.data.sites.netescola.urls import Urls
from app.auto.data.sites.netescola.xpaths import Xpaths
from app.auto.data.sites.siteconfig import SiteConfig

NetEscola = SiteConfig(
    nome='netescola',
    urls=Urls().tela_login,
    xpaths=Xpaths().xpaths
)
