import datetime
from app.auto.data.sites.google import Google
from app.auto.data.sites.netescola import NetEscola
from app.auto.data.sites.siap import Siap
from app.auto.data.sites.sige import Sige
from app.auto.data.sites.tipagem import TipagemPropriedades


class Propriedades(TipagemPropriedades) :
    #todo: repensar essa classe depois. A forma que ela é instanciada na navegação é estranha.
    # A navegação usa ela sempre, enquanto outras classes usam navegação e propriedade. Talvez deva haver propriedades de navegação.
    # a localização deste módulo também me incomoda (junto com os sites)
    # acho que devia ser propriedades

    def __init__(self, site: str | None = None) :
        _site = self.__sites.get(site.lower())()

        for attr in self.atributos :
            setattr(self, attr, getattr(_site, attr, None))

        self.hoje = datetime.datetime.now().strftime('%d/%m/%Y')
        self.agora = datetime.datetime.now()

    @property
    def __sites(self) :
        return {
            'sige' : Sige, 'siap' : Siap, 'netescola' : NetEscola, 'google' : Google
        }

    @property
    def atributos(self) :
        return ['url', 'xpaths', 'caminhos', 'credenciais', 'ids', 'css_selectors']

    def __getattr__(self, item) :
        return getattr(self.site, item)
