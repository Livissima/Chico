from typing import Literal
from selenium.webdriver import Chrome
# from app.auto import Propriedades
from app.auto.functions.navegaçãoweb_.navegaçãowebmobilidade import NavegaçãoWebMobilidade
from app.auto.functions.navegaçãoweb_.navegaçãowebscraping import NavegaçãoWebScraping
from app.auto.functions.navegaçãoweb_.navegaçãowebsiap import NavegaçãoWebSiap
from app.auto.functions.navegaçãoweb_.navegaçãowebsige import NavegaçãoWebSige
from app.auto.functions.navegaçãoweb_.tipagemnavegação import TipagemNavegação


class NavegaçãoWeb(TipagemNavegação) :
    # Mova para atributo de CLASSE (não property)
    _CONFIG_INSTÂNCIAS = {
        'sige' : {
            'sige' : NavegaçãoWebSige, 'mobilidade' : NavegaçãoWebMobilidade, 'scraping' : NavegaçãoWebScraping
        }, 'siap' : {
            'siap' : NavegaçãoWebSiap, 'mobilidade' : NavegaçãoWebMobilidade, 'scraping' : NavegaçãoWebScraping
        }, 'google' : {
            'mobilidade' : NavegaçãoWebMobilidade, 'scraping' : NavegaçãoWebScraping
        }, 'netescola' : {
            'mobilidade' : NavegaçãoWebMobilidade, 'scraping' : NavegaçãoWebScraping
        }
    }

    def __init__(self, master: Chrome, site: Literal['sige', 'siap', 'google', 'netescola'] | str) :
        self.master = master
        # self._pp = Propriedades(site)  # ⚠️ IMPORTANTE: Esta linha estava faltando!
        self._módulos = {}

        # Use o atributo de classe diretamente
        config = self._CONFIG_INSTÂNCIAS.get(site.lower(), {})

        print(f"🔧 Configurando navegação para: {site}")
        print(f"📦 Módulos a carregar: {list(config.keys())}")

        for nome_módulo, classe in config.items() :
            try :
                if classe in [NavegaçãoWebMobilidade, NavegaçãoWebScraping] :
                    self._módulos[nome_módulo] = classe(master, site)
                else :
                    self._módulos[nome_módulo] = classe(master)
                print(f"✅ Módulo '{nome_módulo}' carregado: {self._módulos[nome_módulo]}")
            except Exception as e :
                print(f"❌ Erro ao carregar módulo '{nome_módulo}': {e}")

        # Debug: verificar métodos disponíveis
        self._verificar_métodos()

    def _verificar_métodos(self) :
        """Método de debug para verificar quais métodos estão disponíveis"""
        print("=== 🔍 MÉTODOS DISPONÍVEIS ===")
        for nome_módulo, módulo in self._módulos.items() :
            métodos = [m for m in dir(módulo) if not m.startswith('_') and callable(getattr(módulo, m))]
            print(f"📦 {nome_módulo}: {métodos}")
        print("===============================")

    def __getattr__(self, item) :
        print(f"🔍 Buscando método: {item}")

        for nome_módulo, módulo in self._módulos.items() :
            if hasattr(módulo, item) :
                método = getattr(módulo, item)
                print(f"✅ Método '{item}' encontrado em '{nome_módulo}', tipo: {type(método)}")

                # Verifique se é callable
                if callable(método) :
                    print(f"📞 Método '{item}' é callable")
                else :
                    print(f"⚠️ Método '{item}' NÃO é callable")

                return método

        raise AttributeError(f"'{self.__class__.__name__}' não possui o atributo '{item}'")

    # REMOVA a property _config_instâncias - isso está causando confusão

