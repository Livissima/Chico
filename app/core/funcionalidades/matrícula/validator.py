from typing import List, Dict, Any, Tuple
from elements.templates import SeçãoFormulário

class FormValidator:

    @staticmethod
    def validar(seções: List[SeçãoFormulário], dados: Dict[str, Any]) -> Tuple[bool, List[str]]:
        erros = []
        for seção in seções:
            for linha in seção.linhas:
                for campo in linha.campos:
                    valor = dados.get(campo.chave)
                    erro = campo.validar(valor)

                    if erro: erros.append(erro)

        é_valido = len(erros) == 0
        return é_valido, erros