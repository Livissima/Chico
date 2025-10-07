import unicodedata
from pandas import DataFrame, Series


class TratamentoFichas:

    def __init__(self, leitura: list[str]):
        self.leitura = leitura
        self.df_tratado = self.gerar_df(leitura)

    def gerar_df(self, leitura: list[str]) -> DataFrame:
        tratado = self.tratar(leitura)
        return DataFrame(data=tratado)

    def tratar(self, leitura: list[str]) -> list[dict[str, str]]:
        strings = self.normalizar_strings(leitura)
        strings_separadas = self.gerar_separadores(strings)
        lista_de_listas_de_dados = self.converter_str_list(strings_separadas)

        ###debug
        # dicio_aluno = {}
        # for aluno in lista_de_listas_de_dados:
        #     if len(aluno) != 38:
        #         print(f'{aluno = }')
        #
        #     for chave, índice in self.guia.items():
        #         try:
        #             dicio_aluno = {chave : aluno[índice]}
        #
        #         except Exception as e:
        #             raise Exception(f'{aluno = }\n{índice = }\n{e = }')

        return [{chave: (aluno[índice]) for chave, índice in self.guia.items()} for aluno in lista_de_listas_de_dados]

    def gerar_separadores(self, linhas: list[str]) :
        trocas: list[str] = self.map_trocas
        linhas_limpas: list[str] = []
        for linha in linhas :
            for troca in trocas :
                linha = linha.replace(troca, ':::')
            linhas_limpas.append(linha)
        return linhas_limpas

    @staticmethod
    def normalizar_strings(lista_strings: list[str]) -> list[str]:
        return [unicodedata.normalize('NFKC', linha).replace('	', ' ') for linha in lista_strings]

    @staticmethod
    def converter_str_list(linhas) -> list[str]:
        return [linha.split(':::')[1:] for linha in linhas]

    @property
    def map_trocas(self) -> list[str]:
        return [
            'Dados Pessoais ',
            'Profissão:',
            'Matrícula SEE: ',
            'Número para chamada: ',
            'Nome do Aluno(a): ',
            ' Nome Social:',
            'Data Nascimento: ',
            ' Certidão nasc.: ',
            ' No Matrícula:',
            ' No Certidão:',
            'Livro:',
            'Folha:',
            'Naturalidade: ',
            ' UF: ',
            ' Nacionalidade: ',
            ' País de origem: ',
            'C.I:',
            'Orgão Expedidor: ',
            ' Data Expedição:',
            ' Nome Responsável: ',
            ' Filiação Filiação 1:',
            'CPF: ',
            'Filiação 2:',
            ' Endereço Residencial Logradouro:',
            'Número',
            'Complemento:',
            'Município: ',
            ' RG: ',
            'Bairro',
            'CEP: ',
            ' Dados Escolares Curso: ',
            'Série: ',
            'Ano',
            'Turma: ',
            ' Turno: ',
            ' Data da matrícula: ',
            '\n',
            '::::::',
        ]

    @property
    def guia(self) -> dict[str, int]:
        return {
            'Matrícula' : 0,
            'Número pra chamada' : 1,
            'Estudante' : 2,
            'Nome Social': 3,
            'Data de Nascimento' : 4,
            'Certidão de Nascimento: Termo' : 5,
            'Certidão de Nascimento: Livro' : 6,
            'Certidão de Nascimento: Folha' : 7,
            'Município de Naturalidade' : 8,
            'UF de Naturalidade' : 9,
            'Nacionalidade' : 10,
            'País de origem' : 11,
            'RG' : 12,
            'RG - Emissor' : 13,
            'RG - Expedição' : 14,
            'CPF Aluno' : 15,
            'Nome Responsável' : 16,
            'Filiação 1' : 17,
            'Filiação 1 - Prof' : 18,
            'Filiação 1 - CPF' : 19,
            'Filiação 1 - RG' : 20,
            'Filiação 2' : 21,
            'Filiação 2 - Prof' : 22,
            'Filiação 2 - CPF' : 23,
            'Filiação 2 - RG' : 24,
            'Endereço: Logradouro' : 25,
            'Endereço: Complemento': 26,
            'Endereço: Número' : 27,
            'Endereço: Bairro' : 28,
            'Endereço: Município' : 29,
            'Endereço: CEP' : 30,
            'Curso' : 31,
            'Série' : 33,
            'Turma' : 35,
            'Turno' : 36,
            'Data Matrícula' : 37
        }
