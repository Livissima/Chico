import json

from json import JSONDecodeError
from os import PathLike
from pathlib import Path

from app.config.settings.functions import ler_json


class Prévias:
    def __init__(self, path_resumo: Path):
        self._validar_path(path_resumo)
        self._path = Path(path_resumo, 'fonte', 'resumo.json')

        self.resumo = self._ler_resumo(self._path) or None
        self.turmas = self.resumo['Turmas']
        self.nome_ue = self.resumo['Nome UE']

    @staticmethod
    def _validar_path(path_resumo: Path):
        diretório_fonte = Path(path_resumo, 'fonte')
        if not diretório_fonte.exists():
            diretório_fonte.mkdir(parents=True, exist_ok=True)



    @staticmethod
    def _ler_resumo(path: Path) -> dict[str, list | str]:
        try:
            if Path(path).exists():
                resumo = ler_json(path)
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


