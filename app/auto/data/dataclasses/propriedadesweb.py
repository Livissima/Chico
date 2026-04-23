# from app.auto.data.sites.google.google import Google
from app.auto.data.sites import NetEscola
from app.auto.data.sites.siap import Siap
from app.auto.data.sites.sige import Sige
from app.auto.data.dataclasses.siteconfig import SiteConfig


class PropriedadesWeb(SiteConfig) :
    def __new__(cls, site: str):
        _sites = {
            'sige' : Sige,
            'siap' : Siap,
            'netescola' : NetEscola,
            # 'google' : Google
        }

        config = _sites.get(site.lower())

        if not config:
            raise ValueError(f'Site {site} não encontrado no registro.')

        return config

