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
        série0 = lista[6]['coluna_3']
        turma0 = lista[6]['coluna_4']
        disciplina0 = lista[6]['coluna_8']
        qntd0 = lista[6]['coluna_9']

        série1 = lista[7]['coluna_3']
        turma1 = lista[7]['coluna_4']
        disciplina1 = lista[7]['coluna_8']
        qntd1 = lista[7]['coluna_9']

        print(f"{lista = }")


        # dicts_regencia = {prof :
        #                       {'série' : serie, 'turma' : turma, 'disciplina' : disciplina}
        #                   for prof, serie, turma, disciplina in zip(series, turmas, disciplinas)}


    #
    #     print(cpf, nome, vínculo, série0, turma0, disciplina0, qntd0)
    #     print(f'{i[7:] = }')
    # print(f'{lista_de_listas_de_dicionários = }')
_obter_modulações()
