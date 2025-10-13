import datetime

from app.auto.data.sites.google import Google
from app.auto.data.sites.netescola import NetEscola
from app.auto.data.sites.siap import Siap
from app.auto.data.sites.sige import Sige


class Propriedades:
    #todo: repensar essa classe depois. A forma que ela é instanciada na navegação é estranha.
    # A navegação usa ela sempre, enquanto outras classes usam navegação e propriedade. Talvez deva haver propriedades de navegação.
    # a localização deste módulo também me incomoda (junto com os sites)
    # acho que devia ser propriedades

    sites = {
        'sige' : Sige,
        'siap' : Siap,
        'netescola' : NetEscola,
        'google' : Google
    }

    def __init__(self, site: str | None = None) :
        _site = self.sites.get(site.lower())()

        atributos = ['url', 'xpaths', 'caminhos', 'credenciais', 'ids', 'css_selectors']
        for attr in atributos :
            setattr(self, attr, getattr(_site, attr, None))

        self.hoje = datetime.datetime.now().strftime('%d/%m/%Y')
        self.agora = datetime.datetime.now()

    def __getattr__(self, item):
        return getattr(self.site, item)

