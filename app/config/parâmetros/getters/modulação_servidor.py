class ModulaçãoServidor :
    @staticmethod
    def processar(lista_de_json: list[list]) -> dict :
        """Processa a lista de conteúdos dos arquivos de modulação."""
        professores = {}
        mapeamento_series = {'6º Ano' : '1996', '7º Ano' : '1997', '8º Ano' : '1998', '9º Ano' : '1999'}

        for dados in lista_de_json :
            if len(dados) < 7 : continue  # Validação mínima

            cpf = dados[1]['coluna_1'].replace('.', '').replace('-', '')
            nome = dados[1]['coluna_3']
            vinculo = dados[3]['coluna_1']

            disciplinas = {f"disciplina_{i - 6}" : {
                'série' : mapeamento_series.get(d['coluna_3'], d['coluna_3']), 'turma' : d['coluna_4'],
                'disciplina' : d['coluna_8'], 'quantidade' : d['coluna_9']
            } for i, d in enumerate(dados[6 :], start=6) if
                all(k in d for k in ['coluna_3', 'coluna_4', 'coluna_8', 'coluna_9'])}

            professores[cpf] = {'nome' : nome, 'vínculo' : vinculo, 'disciplinas' : disciplinas}
        return professores

