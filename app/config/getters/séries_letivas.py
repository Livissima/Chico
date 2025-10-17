from collections import defaultdict


class TurmasSéries:

    def __init__(self, prévias):
        self.lista_séries = self.gerar_lista_de_séries(prévias.turmas)
        self.dicionário_turmas_por_série = self.gerar_dicionário_turmas_por_série(self.lista_séries)



    @staticmethod
    def gerar_dicionário_turmas_por_série(lista_turmas: list[str]) -> dict[str, list[str]] :
        turmas_por_serie = defaultdict(list)

        for turma in lista_turmas :

            serie = ''.join(filter(str.isdigit, turma))
            if serie :
                turmas_por_serie[serie].append(turma)

        return {serie : sorted(turmas) for serie, turmas in sorted(turmas_por_serie.items())}

    @staticmethod
    def gerar_lista_de_séries(lista_turmas) -> list[str] :
        séries_únicas_e_ordenadas = sorted(set(turma[0] for turma in lista_turmas))
        return séries_únicas_e_ordenadas
