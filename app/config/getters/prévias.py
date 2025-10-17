import json
import os
from json import JSONDecodeError
from pathlib import Path


class Prévias:
    def __init__(self, path_resumo):
        self._path = Path(path_resumo, 'fonte', 'resumo.json')

        self.resumo = self._ler_resumo(self._path) or None
        self.turmas = self.resumo['Turmas']
        self.nome_ue = self.resumo['Nome UE']


    @staticmethod
    def _ler_resumo(path):
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


