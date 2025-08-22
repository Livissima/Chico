from datetime import date
from dateutil.relativedelta import relativedelta
import pandas as pd


class Idade:
    @staticmethod
    def calcular_idade(coluna_data_de_nascimento: pd.Series) -> pd.Series:
        hoje = date.today()

        def idade_segura(data):
            try:
                if pd.isnull(data):
                    return None
                return relativedelta(hoje, data.date()).years
            except Exception:
                return None

        return coluna_data_de_nascimento.apply(idade_segura)
