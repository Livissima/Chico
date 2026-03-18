from abc import ABC, abstractmethod
from selenium.webdriver import Chrome

from app.auto import NavegaçãoWeb
from app.auto.data.sites.tipagem import SiteConfig


class TarefaBase(ABC):
    def __init__(self, navegador: Chrome, config: SiteConfig):
        self.driver = navegador
        self.config = config
        self.nv = NavegaçãoWeb(navegador, config)

    def executar(self, **kwargs):
        try:
            self._logon()
            self._rotina_específica(**kwargs)
        finally:
            self.driver.quit()

    def _logon(self):
        self.driver.get(self.config.url)
        if self.config.nome == 'sige':
            creds = self.config.credenciais["admin"]
            self.nv.digitar_xpath('misc', 'input id', string=creds.id)
            self.nv.digitar_xpath('misc', 'input senha', string=creds.senha)
            self.nv.clicar('xpath', 'misc', 'entrar')
            self.nv.clicar('xpath', 'misc', 'alerta')

    @abstractmethod
    def _rotina_especifica(self, **kwargs) :
        """Cada task implementa só o que ela faz de diferente."""
        pass
