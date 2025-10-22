import re
from typing import Optional

from app.config.app_config import obter_string_numérica


class Telefone :
    def __init__(
            self,
            número: str | int | float | None
    ) -> None :

        self._entrada = número
        self._valor = self._validar(número)

    def _validar(self, número: str | int | float | None) -> Optional[str] :
        _string = self._stringzar(número)
        if _string == '-' :
            return _string
        string_normalizada = self._normalizar_comprimento(_string)

        return string_normalizada

    @staticmethod
    def _stringzar(número) -> str:
        str_numérica = obter_string_numérica(número)
        if len(str_numérica) in range(8, 13) :
            return str_numérica

        return '-'

    @staticmethod
    def _normalizar_comprimento(telefone: str) -> Optional[str] :

        if len(telefone) in (8, 9) :
            return telefone

        if len(telefone) == 10 :
            ddd = telefone[:2]
            número = telefone[2:]
            if número[0] in '6789' :
                return f"{ddd}9{número}"

        if len(telefone) == 11 :
            ddd = telefone[:2]
            número = telefone[2:]
            if número[0] in '6789' :
                return telefone

        return '-'

    @property
    def valor(self) -> Optional[str] :
        return self._valor

    @property
    def é_valido(self) -> bool :
        return self._valor is not None and len(self._valor) in range(8, 11)

    def __str__(self) -> str :
        return self._valor if self._valor else ""

    def __repr__(self) -> str :
        return f"'{self._valor}'"

    def __add__(self, other) :
        """Suporta: telefone + string"""
        return str(self) + str(other)

    def __radd__(self, other) :
        """Suporta: string + telefone"""
        return str(other) + str(self)

    def __eq__(self, other) -> bool :
        if isinstance(other, Telefone) :
            return self._valor == other._valor
        return self._valor == other

    def __hash__(self) -> int :
        return hash(self._valor)

    def __len__(self) -> int :
        return len(str(self))

    def __contains__(self, item) -> bool :
        return item in str(self)

    def __getitem__(self, index) :
        return str(self)[index]

    def format(self, *args, **kwargs) :
        return str(self).format(*args, **kwargs)

    def __bool__(self) -> bool :
        return self.é_valido

    def __format__(self, format_spec) :
        return format(str(self), format_spec)
    #
    # def __getattr__(self, item):
    #     return getattr(self._valor, item)

