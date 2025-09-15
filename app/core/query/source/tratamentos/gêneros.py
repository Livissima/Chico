from pandas import DataFrame


class TratamentoGêneros:
    colunas_dict: dict[str, str] = {
        'Matrícula': 'Matrícula',
        'Nome do aluno': 'Estudante',
        'Sexo': 'Gênero',
    }
    colunas_list: list[str] = [
        'O.', 'Matrícula', 'Nome do aluno', 'Sexo', 'Idade', 'Data nascimento', 'Documentação',
        'Data Sit.', 'Situação'
    ]

    colunas_finais: list[str] = ['Matrícula', 'Gênero']

    def __init__(self, leitura: DataFrame):

        self.leitura = DataFrame(leitura)
        self.df_tratado = self.tratar(self.leitura)

    def tratar(self, leitura):
        df_tratado = self._concluir_df(leitura)
        return df_tratado

    @property
    def _colunas_base(self) -> list:
        num_columns = len(self.leitura.columns)
        nomes_colunas = self.colunas_list + [f'Extra_{i}' for i in range(num_columns - 9)]
        if len(nomes_colunas) != num_columns:
            print(f"Warning: Expected {num_columns} columns but got {len(nomes_colunas)} new names.")

        return nomes_colunas

    def _concluir_df(self, leitura):
        df = leitura
        df.columns = self._colunas_base
        df = df.rename(columns=self.colunas_dict)
        df = df[self.colunas_finais]
        df = df.dropna(axis=0, how='all', ignore_index=True)
        return df

    def __getattr__(self, item):
        return getattr(self.df_tratado, item)
