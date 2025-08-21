from pandas import DataFrame


class Filtro:
    def __init__(self, consulta: DataFrame):
        self.consultas_filtradas: dict[str, DataFrame] = self.filtrar()

    def filtrar(self):
        pass