from typing import Iterable, Generator

import unicodedata
from pandas import DataFrame


class TratamentoFichas:

    def __init__(self, fluxo_leitura: Iterable[str]):
        self.fluxo = self._processar_pipeline(fluxo_leitura)

        self._leitura = fluxo_leitura
        self.df_tratado = self._gerar_df(fluxo_leitura)

    def _processar_pipeline(self, fluxo_leitura: Iterable[str]) -> Generator[dict, None, None]:
        for linha in fluxo_leitura:
            linha_limpa = unicodedata.normalize('NFKC', linha).replace('  ', ' ')

            for troca in self._map_para_separadores:
                linha_limpa = linha_limpa.replace(troca, ":::")

            partes = [p.strip() for p in linha_limpa.split(':::')[1:]]

            if len(partes) >= len(self._guia):
                yield {chave: partes[índice] for chave, índice in self._guia.items()}


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
