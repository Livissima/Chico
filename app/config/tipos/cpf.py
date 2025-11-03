from typing import Optional

from app.config.app_config import obter_string_numérica
from app.config.tipos.telefone import Telefone


class CPF:
    def __init__(
            self,
            valor_cpf: str | int | float | None
    ) -> None :

        self._entrada = valor_cpf
        self._validez = '-'
        self._valor = self._executar(valor_cpf)


    def _executar(self, _cpf: str | int | float | None) -> Optional[str] :
        cpf_completo = self._preparar_string(_cpf)

        if cpf_completo == '-' :
            return cpf_completo

        verificadores_calculados = self._obter_verificadores(cpf_completo)
        if verificadores_calculados == cpf_completo[-2 :] :
            self._validez = 'Válido'
            return cpf_completo

        self._validez = 'Inválido'
        return f"'{cpf_completo}'"

    def _obter_verificadores(self, cpf_completo):
        estrutura_inicial = self._estrutura(cpf_completo)
        check_um = self._gerar_verificador(estrutura_inicial)
        check_dois = self._gerar_verificador(estrutura_inicial, check_um)
        return check_um + check_dois

    @staticmethod
    def _gerar_verificador(estrutura: dict, check: str = None):
        multiplicadores: list[int] = []
        multiplicandos: list[int] = []

        if not check:
            multiplicadores = [int(dígito) for dígito in estrutura['nove']]
            multiplicandos = list(range(2, 11))[: :-1]

        if check:
            multiplicadores = [int(dígito) for dígito in estrutura['nove']] + [int(check)]
            multiplicandos = list(range(2, 12))[: :-1]

        dicionário = dict(zip(multiplicandos, multiplicadores))
        resultados = sum([dígito * multiplicador for dígito, multiplicador in dicionário.items()])
        resto = resultados % 11

        if resto in (0, 1) :
            return '0'
        else:
            return str(11 - resto)


    @staticmethod
    def _estrutura(cpf_completo) :
        #todo: desfazer isso aqui. Não é muito prático. Enche linguiça
        return {
            'nove' : cpf_completo[:9], 'verificador 1' : cpf_completo[-2],
            'verificador 2' : cpf_completo[-1], 'verificadores' : cpf_completo[-2 :],
            'completo' : cpf_completo
        }

    @property
    def validez(self):
        return self._validez

    @staticmethod
    def _preparar_string(cpf) -> str:
        str_numérica = obter_string_numérica(cpf)
        if len(str_numérica) == 11 :
            return str_numérica

        return '-'


    @property
    def valor(self) -> Optional[str] :
        return self._valor

    def __str__(self) -> str :
        return self._valor if self._valor else ""

    def __repr__(self) -> str :
        return f"CPF(valor='{self._valor}', situação='{self._validez}')"

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

    # def __bool__(self) -> bool :
    #     return self.é_valido

    def __format__(self, format_spec) :
        return format(str(self), format_spec)



if __name__ == '__main__':
    valor_CPF = 85356498722
    instância_CPF = CPF(valor_CPF)
    print(f'{instância_CPF = }')


