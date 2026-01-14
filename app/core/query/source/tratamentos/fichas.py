import unicodedata
from pandas import DataFrame, Series, ExcelWriter


class TratamentoFichas:

    def __init__(self, leitura: list[str]):
        self.leitura = leitura
        self.df_tratado = self.gerar_df(leitura)

    def gerar_df(self, leitura: list[str]) -> DataFrame:
        tratado = self._tratar(leitura)
        return DataFrame(data=tratado)

    def _tratar(self, leitura: list[str]) -> list[dict[str, str]]:
        strings = self._normalizar_strings(leitura)
        strings_separadas = self._gerar_separadores(strings)
        lista_de_listas_de_dados = self._splitar_linha(strings_separadas)

        return [{chave: (aluno[índice]) for chave, índice in self._guia.items()} for aluno in lista_de_listas_de_dados]


    @staticmethod
    def _normalizar_strings(lista_strings: list[str]) -> list[str]:
        return [unicodedata.normalize('NFKC', linha).replace('	', ' ') for linha in lista_strings]

    def _gerar_separadores(self, linhas: list[str]) :
        linhas_com_separadores: list[str] = []
        for linha in linhas :

            for troca in self._map_para_separadores :
                linha = linha.replace(troca, ':::')

            linhas_com_separadores.append(linha)

        return linhas_com_separadores

    @staticmethod
    def _splitar_linha(linhas) -> list[str]:
        return [linha.split(':::')[1:] for linha in linhas]

    @property
    def _map_para_separadores(self) -> list[str]:
        return [
            'Dados Pessoais Matrícula SEE: ',
            'Número para chamada:',
            'Nome do Aluno(a):',
            'Nome Social:',
            'Data Nascimento:',
            'No Certidão:',
            'Certidão nasc.:',
            'Livro:',
            'Folha:',
            'Naturalidade:',
            'UF:',
            'Nacionalidade:',
            'País de origem:',
            'C.I:',
            'Orgão Expedidor:',
            'Data Expedição:',
            'CPF:',
            'Nome Responsável:',
            'Filiação Filiação 1:',
            'Profissão:',
            'RG:',
            'Filiação 2:',
            'Endereço Residencial Logradouro:',
            'Número',
            'Complemento:',
            'Bairro',
            'Município:',
            'CEP:',
            'Dados Escolares Curso:',
            'Série:',
            'Ano',
            'Turma:',
            'Turno:',
            'Data da matrícula:',
            'No Matrícula:',
            '\n',
            '::::::',
        ]



    @property
    def _guia(self) -> dict[str, int]:
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


    # Backup
    # @property
    # def _map_para_separadores(self) -> list[str]:
    #     return [
    #         'Dados Pessoais ',
    #         'Profissão:',
    #         'Matrícula SEE: ',
    #         'Número para chamada: ',
    #         'Nome do Aluno(a): ',
    #         ' Nome Social:',
    #         'Data Nascimento: ',
    #         ' Certidão nasc.: ',
    #         ' No Matrícula:',
    #         ' No Certidão:',
    #         'Livro:',
    #         'Folha:',
    #         'Naturalidade: ',
    #         ' UF: ',
    #         ' Nacionalidade: ',
    #         ' País de origem: ',
    #         'C.I:',
    #         'Orgão Expedidor: ',
    #         ' Data Expedição:',
    #         ' Nome Responsável: ',
    #         ' Filiação Filiação 1:',
    #         'CPF: ',
    #         'Filiação 2:',
    #         ' Endereço Residencial Logradouro:',
    #         'Número',
    #         'Complemento:',
    #         'Município: ',
    #         ' RG: ',
    #         'Bairro',
    #         'CEP: ',
    #         ' Dados Escolares Curso: ',
    #         'Série: ',
    #         'Ano',
    #         'Turma: ',
    #         ' Turno: ',
    #         ' Data da matrícula: ',
    #         '\n',
    #         '::::::',
    #     ]