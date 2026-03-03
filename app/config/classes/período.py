from datetime import date

class Período:
    def __init__(
            self,
            data_inicial: date,
            data_final: date
    ):
        self._entrada = ''
        self._valor = self._validar()

    def _validar(self):
        return self



data = date(2025, 10, 22)
print(data)
