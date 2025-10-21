import json
import os
from os import PathLike
from pathlib import Path


class ModulaçãoServidor:

    def __init__(self, path: PathLike):
        self._path = Path(path, 'fonte', 'modulações')
        self.modulações = self._obter_modulações(self._path)

    def _obter_modulações(self, path: Path) :
        leitura = self.obter_lista_jsons(path)

        if not leitura:
            return {}

        lista_de_listas = self._ler(path, leitura)
        dicionário_modulações = self._tratar_modulações(lista_de_listas)
        return dicionário_modulações

    @staticmethod
    def obter_lista_jsons(path) -> list[str]:
        if path.exists():
            return os.listdir(path)
        return []

    @staticmethod
    def _ler(path: PathLike, lista: list) :

        lista_jsons = lista
        lista_de_listas_de_dicionários = []

        for arquivo in lista_jsons :
            if arquivo.endswith('.json'):
                caminho = Path(path, arquivo)
                with open(caminho, 'r', encoding='utf-8') as f:
                    lista_de_listas_de_dicionários.append(json.load(f))

        return lista_de_listas_de_dicionários


    @staticmethod
    def _tratar_modulações(lista_de_listas_de_dicionários) -> dict :
        professores = {}
        disciplinas = {}
        mapeamento_series = {'6º Ano' : '1996', '7º Ano' : '1997', '8º Ano' : '1998', '9º Ano' : '1999'}

        for lista in lista_de_listas_de_dicionários :
            cpf = lista[1]['coluna_1']
            cpf = cpf.replace('.', '').replace('-', '')
            nome = lista[1]['coluna_3']
            vínculo = lista[3]['coluna_1']

            disciplinas = {f"disciplina_{i - 6}" : {
                'série' : mapeamento_series.get(dicionario['coluna_3'], dicionario['coluna_3']),
                'turma' : dicionario['coluna_4'],
                'disciplina' : dicionario['coluna_8'],
                'quantidade' : dicionario['coluna_9']
            } for i, dicionario in enumerate(lista[6 :], start=6) if
                all(key in dicionario for key in ['coluna_3', 'coluna_4', 'coluna_8', 'coluna_9'])}


            professores[cpf] = {
                'nome' : nome, 'vínculo' : vínculo, 'disciplinas' : disciplinas
            }

        return professores

