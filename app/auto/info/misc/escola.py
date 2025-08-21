class Escola:

    # todo: Criar métodos que consigam modificar os dicionários e listas de séries e turmas, para flexibilizar por escola.
    #  Para viabilizar isso, eu precisaria rodar uma automação que fizesse uma varredura em algum relatório de turmas do sige.
    @property
    def turmas(self) -> list[str]:
        return ['6A', '6B', '6C', '7A', '7B', '8A', '8B', '9A']

    @property
    def séries(self) -> list[str]:
        return [
            '6', '7', '8', '9'
        ]

    @property
    def turmas_por_serie(self) -> dict[str, list[str]]:
        return {
            '6': ['6A', '6B', '6C'],
            '7': ['7A', '7B'],
            '8': ['8A', '8B'],
            '9': ['9A']
        }

    @property
    def turnos(self) -> dict[str:str]:
        return {
            '1': 'matutino'
        }

    @property
    def composições(self) -> dict[str:str]:
        return {
            '' : ''
        }
