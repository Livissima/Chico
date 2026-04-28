from os import listdir
from typing import Literal
import json
from pathlib import Path

class Leitura :

    def __init__(
            self,
            _path: str | Path,
            tipo_de_relatório: Literal['fichas', 'contatos', 'gêneros', 'situações', 'servidores'] | str
    ) :
        print(f'Leitura: {tipo_de_relatório = }')

        self._tipo_de_relatório = tipo_de_relatório
        self._path_dados = _path
        self.fluxo_inicial = self._ler(_path)


    def _ler(self, _path) :
        for nome_arquivo in listdir(_path):
            yield from self.ler_json(nome_arquivo, _path)


    @staticmethod
    def ler_json(_nome_arquivo: str, _path):
        caminho_completo = Path(_path, _nome_arquivo)

        with open(caminho_completo, encoding='utf-8') as arquivo :
            dados = json.load(arquivo)
            yield from dados




