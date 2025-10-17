import json
import os


class ModulaçãoServidor:

    def __init__(self, novo_diretório):
        self.modulações = self._obter_modulações(novo_diretório)


    def _obter_modulações(self, novo_diretório) :
        lista_de_listas = self._ler(novo_diretório)
        dicionário_modulações = self._tratar_modulações(lista_de_listas)
        return dicionário_modulações

    @staticmethod
    def _ler(novo_diretório):

        lista_jsons = os.listdir(os.path.join(novo_diretório, 'fonte', 'modulações'))

        lista_de_listas_de_dicionários = []

        for arquivo in lista_jsons :
            if arquivo.endswith('.json') :
                caminho = os.path.join(novo_diretório, 'fonte', 'modulações', arquivo)
                with open(caminho, 'r', encoding='utf-8') as f :
                    lista_de_listas_de_dicionários.append(json.load(f))

        return lista_de_listas_de_dicionários


    @staticmethod
    def _tratar_modulações(lista_de_listas_de_dicionários):
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

