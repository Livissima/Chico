import json
import os
from app.config.parâmetros import parâmetros


def _obter_modulações() :
    dados = []
    lista_jsons = os.listdir(os.path.join(parâmetros.novo_diretório, 'fonte', 'modulações'))
    print(f'{lista_jsons = }')
    lista_de_listas_de_dicionários = []

    for arquivo in lista_jsons :
        if arquivo.endswith('.json') :
            caminho = os.path.join(parâmetros.novo_diretório, 'fonte', 'modulações', arquivo)
            with open(caminho, 'r', encoding='utf-8') as f :
                lista_de_listas_de_dicionários.append(json.load(f))

    for lista in lista_de_listas_de_dicionários :
        cpf = lista[1]['coluna_1']
        nome = lista[1]['coluna_3']
        vínculo = lista[3]['coluna_1']

        # Filtra apenas os dicionários que têm todas as colunas necessárias
        disciplinas = {f"disciplina_{i - 6}" : {
            'série' : dicionario['coluna_3'], 'turma' : dicionario['coluna_4'], 'disciplina' : dicionario['coluna_8'],
            'quantidade' : dicionario['coluna_9']
        } for i, dicionario in enumerate(lista[6 :], start=6) if all(key in dicionario for key in [
            'coluna_3', 'coluna_4', 'coluna_8', 'coluna_9'
        ])}

        # Agora você tem um dicionário organizado com todas as disciplinas
        print(f"CPF: {cpf}")
        print(f"Nome: {nome}")
        print(f"Vínculo: {vínculo}")
        for key, disc in disciplinas.items() :
            print(f"{key}: {disc}")
        # dicts_regencia = {prof :
        #                       {'série' : serie, 'turma' : turma, 'disciplina' : disciplina}
        #                   for prof, serie, turma, disciplina in zip(series, turmas, disciplinas)}


    #
    #     print(cpf, nome, vínculo, série0, turma0, disciplina0, qntd0)
    #     print(f'{i[7:] = }')
    # print(f'{lista_de_listas_de_dicionários = }')
_obter_modulações()
