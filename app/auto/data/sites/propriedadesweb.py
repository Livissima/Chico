from app.auto.data.sites.google.google import Google
from app.auto.data.sites.netescola.netescola import NetEscola
from app.auto.data.sites.siap import Siap
from app.auto.data.sites.sige import Sige
from app.auto.data.sites.siteconfig import SiteConfig


class PropriedadesWeb(SiteConfig) :
    def __new__(cls, site: str | None = None):
        _sites = {
            'sige' : Sige,
            'siap' : Siap,
            'netescola' : NetEscola,
            'google' : Google
        }

        config = _sites.get(site.lower())

        if not config:
            raise ValueError(f'Site {site} não encontrado no registro.')

        return config

#class PropriedadesWeb
    # #todo: Esta classe está extremamente acoplada com dezenas de outras classes.
    # # Pensei em fazer uma singleton, mas os atributos dependem do argumento passado na instanciação
    #
    # def __init__(self, site: str | None = None) :
    #     _site = self.__sites.get(site.lower())()
    #
    #     for attr in self.atributos :
    #         setattr(self, attr, getattr(_site, attr, None))
    #
    # @property
    # def __sites(self) :
    #     return {
    #         'sige' : Sige,
    #         'siap' : Siap,
    #         'netescola' : NetEscola,
    #         'google' : Google
    #     }
    #
    # @property
    # def atributos(self) :
    #     return ['url', 'xpaths', 'caminhos', 'credenciais', 'ids', 'css_selectors']
    #
    # def __getattr__(self, item) :
    #     return getattr(self.site, item)
