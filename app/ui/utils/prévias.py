import os

from pandas import read_csv, read_excel, DataFrame


class Prévias:
    def __init__(self, path_resumo):
        self.path = os.path.join(path_resumo, 'Resumo.csv')

        self.resumo = self.resumir(self.path)
        self.turmas = self.resumo['Turmas']


    @staticmethod
    def resumir(path):
        resumo = read_csv(path)
        return resumo

