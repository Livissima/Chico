import json
import os
from json import JSONDecodeError
from pathlib import Path


class Prévias:
    def __init__(self, path_resumo):
        self.path = Path(path_resumo, 'fonte', 'resumo.json')

        self.resumo = self.ler_resumo(self.path) or None
        self.turmas = self.resumo['Turmas']
        self.nome_ue = self.resumo['Nome UE']


    @staticmethod
    def ler_resumo(path):
        try:
            if Path(path).exists():
                with open(path, 'r', encoding='utf-8') as arquivo:
                    resumo = json.load(arquivo)
                return resumo
            else:
                return {
                    "Turmas": [],
                    "Nome UE": "",
                    "Códigos Turmas" : []
                }
        except JSONDecodeError:
            return {
                    "Turmas": [],
                    "Nome UE": "",
                    "Códigos Turmas" : []
                }


