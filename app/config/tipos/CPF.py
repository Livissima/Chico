import re
from typing import Optional

from app.config.tipos.telefone import Telefone


class CPF:
    def __init__(self, valor_cpf: str | int | float | None) -> None :
        self._valor_inserido = valor_cpf
        print(f'{self._valor_inserido = }')
        self._valor = self._validar(valor_cpf)

    def _validar(self, número: str | int | float | None) -> Optional[str] :
        _string = self._stringzar(número)
        if _string == '-' :
            return _string
        parcial = self._primeira_verificação(_string)


        return parcial

    @staticmethod
    def _stringzar(número) -> str:
        if not número:
            return '-'

        _str_numérica = re.sub(r'\D', '', str(número))
        if len(_str_numérica) == 11 :
            print(f'{_str_numérica = }')
            return _str_numérica

        return '-'

    def _primeira_verificação(self, string: str):
        dígitos = [int(dígito) for dígito in string[:9]]
        print(f'{dígitos = }\n')
        multiplicadores = list(range(2, 11))[: :-1]
        print(f'{multiplicadores = }\n')
        dicionário = dict(zip(multiplicadores, dígitos))
        for m, d in dicionário.items():
            print(f'{m = }, {d = }')
        resultados = [dígito*multiplicador for dígito, multiplicador in dicionário.items()]

        print(f'\n{resultados = }\n')
        soma = sum(resultados)
        print(f'{soma = }\n')

        resto = soma % 11

        print(f'{resto = }')

        subtração = 11 - resto
        print(f'{subtração = }')


        return resultados

    @property
    def valor(self) -> Optional[str] :
        return self._valor


if __name__ == '__main__':
    valor_CPF = 75524732153
    instância_CPF = CPF(valor_CPF).valor

    print(instância_CPF)



