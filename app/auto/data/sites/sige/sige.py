from app.auto.data.sites.sige.caminhos import Caminhos
from app.auto.data.sites.sige.css_selectors import CssSelectors
from app.auto.data.sites.sige.ids import Ids
from app.auto.data.sites.sige.xpaths import Xpaths
from app.config.env_config import ID_SIGE, SENHA_SIGE


class Sige :

    @property
    def url(self):
        return 'https://sige.educacao.go.gov.br/sige/login.asp'

    @property
    def credenciais(self) :
        return {
            'id' : ID_SIGE,
            'senha' : SENHA_SIGE
        }

    @property
    def css_selectors(self) -> dict[str, str] :
        return CssSelectors().css_selectors

    @property
    def ids(self) -> dict[str, str] :
        return Ids().ids

    @property
    def xpaths(self) :
        return Xpaths().xpaths

    @property
    def caminhos(self) -> dict[str, list[tuple]] :
        return Caminhos().caminhos


if __name__ == '__main__':
    print(Sige().xpaths)

