import re
from datetime import date

from app.config.app_config import obter_string_numérica


class DataReal:
    #todo terminar de construir o tipo
    def __init__(
            self,
            data: str | int | tuple | date
    ):
        self._entrada = data
        self._valor = self._validar(self._entrada)

    @staticmethod
    def _validar(entrada) -> str:

        if isinstance(entrada, (str, int)):
            return obter_string_numérica(entrada)

        # if isinstance(entrada, tuple):
        #     return self._validar_tupla(entrada)

        return ''

    def _validar_tupla(self, tupla: tuple):
        # if len(tupla) > 3 :
        #     return ''
        #
        # if len(tupla[0]) == 2 and len(tupla[1]) == 2:
        #
        #     if tupla[0][0] in (1, 2, 3) and tupla[1] in list(range(1, 13))
        raise NotImplemented



