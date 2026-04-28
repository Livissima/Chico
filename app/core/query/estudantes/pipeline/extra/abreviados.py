
from app.core.query.estudantes.pipeline.extra.common import preposições_nominais



class Abreviados:

    @staticmethod
    def abreviar(linha):
        partes_nome = [
            nome.title() for nome in linha['Estudante'].split() if
            nome.lower() not in preposições_nominais
        ]

        if len(partes_nome) >= 3 :
            nome = [partes_nome[0], f'{partes_nome[1][0]}.', partes_nome[-1]]
        else:
            nome = partes_nome

        nome_final = ' '.join(nome)



        print(f'{nome_final = }')
        return nome_final


