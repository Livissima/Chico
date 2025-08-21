import pandas as pd


class Social:

    def __init__(self, path_df_social):
        self.df_social = self._obter_social(path_df_social)

    @staticmethod
    def _obter_social(path_df):
        return pd.read_excel(path_df)

    def __getattr__(self, item):
        return getattr(self.df_social, item)


if __name__ == '__main__':
    path = r'C:\Users\meren\OneDrive - Secretaria de Estado da Educação\Secretaria\2025\Dados\Estudantes\Base de dados\Etnia e religião.xlsx'
    instancia = Social(path)
    print(instancia.df_social)