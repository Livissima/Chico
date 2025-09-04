import json
import os
from pathlib import Path


class Prévias:
    def __init__(self, path_resumo):
        self.path = Path(path_resumo, 'fonte', 'resumo.json')

        self.resumo = self.resumir(self.path)
        self.turmas = self.resumo['Turmas']
        self.nome_ue = self.resumo['Nome UE']


    @staticmethod
    def resumir(path):
        if Path(path).exists():
            with open(path, 'r', encoding='utf-8') as arquivo:
                resumo = json.load(arquivo)
            return resumo
        else:
            return {
                "Turmas": []
            }

