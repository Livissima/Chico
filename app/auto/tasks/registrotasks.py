from typing import Type, Dict, Any

class RegistroTasks :
    REGISTRO: Dict[str, Type[Any]] = {}

    @classmethod
    def registrar(cls, task: str):
        def wrapper(classe_envelopada) :
            cls.REGISTRO[task] = classe_envelopada
            return classe_envelopada

        return wrapper
