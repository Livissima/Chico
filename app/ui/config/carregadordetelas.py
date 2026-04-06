import importlib
import pkgutil
from app.ui import screens
from app.ui.config.registrodetelas import RegistradorDeTelas

class CarregadorDeTelas:
    _telas_carregadas: bool = False

    @classmethod
    def carregar_telas(cls):
        #todo: Elaborar uma classe própria para carregar esses dados dos decorators, para então passar a informação
        # para o alternador de telas

        if cls._telas_carregadas:
            return

        path = screens.__path__
        prefix = screens.__name__ + "."

        for loader, module_name, ispkg in pkgutil.walk_packages(path=path, prefix=prefix):
            try:
                importlib.import_module(module_name)
            except Exception as e:
                print(f"\n# # # # # #\nERRO AO CARREGAR MÓDULO!! '{module_name}'\n{e}\n# # # # # #\n")

        cls._telas_carregadas = True

        print(f"Total de telas registradas: {len(RegistradorDeTelas.REGISTRO_DE_TELAS)}\n   → {list(RegistradorDeTelas.REGISTRO_DE_TELAS)}")
