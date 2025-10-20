import re
from typing import Optional


class Telefone :
    def __init__(self, número: str | int | None) -> None :
        self._raw_value = número
        self._valor = self._validar_e_normalizar(número)

    def _validar_e_normalizar(self, número: str | int | None) -> Optional[str] :
        try :
            if número is None :
                return None

            if isinstance(número, (int, float)) :
                número = str(int(número))

            if not isinstance(número, str) or número.strip() == '' :
                return None

            string_limpa = self._limpar(número.strip())
            if not string_limpa :
                return None

            return self._normalizar_comprimento(string_limpa)
        except Exception :
            return None

    @staticmethod
    def _limpar(número: str) -> str :
        return re.sub(r'[^0-9]', '', número)

    @staticmethod
    def _normalizar_comprimento(telefone: str) -> Optional[str] :
        if not telefone :
            return None


        if len(telefone) == 10 :
            ddd = telefone[:2]
            numero = telefone[2 :]
            if numero[0] in '6789' :
                return f"{ddd}9{numero}"
            return telefone

        elif len(telefone) == 11 :
            ddd = telefone[:2]
            numero = telefone[2 :]
            if numero[0] in '6789' :
                return telefone
            return f"{ddd}9{numero}"

        # Para números com mais dígitos, retorna como está (pode ser internacional)
        return telefone if 10 <= len(telefone) <= 13 else None

    @property
    def valor(self) -> Optional[str] :
        return self._valor

    @property
    def é_valido(self) -> bool :
        return self._valor is not None and len(self._valor) in (10, 11)

    def __str__(self) -> str :
        return self._valor if self._valor else ""

    def __repr__(self) -> str :
        return f"Telefone('{self._raw_value}') -> '{self._valor}'"

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

