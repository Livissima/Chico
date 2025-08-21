from pandas import DataFrame


class TratamentoGêneros:
    colunas_dict: dict[str] = {
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

        self.leitura = leitura
        self.df_tratado = self.tratar(leitura)
        # print(f'TratamentoGêneros.df: {leitura.shape}. Colunas: {list(leitura.columns)}')  ####  DEBUG  #####
        # print(f'TratamentoGêneros.df_tratado: {self.df_tratado.shape}. Colunas: {list(self.df_tratado.columns)}\n')

        # print(f'gêneros {list(leitura.columns)}')
    def tratar(self, leitura):
        # self._definir_df_base()
        df_tratado = self._concluir_df(leitura)

        ####  DEBUG  #####

        # df_tratado.to_excel(r'Tratamentos\gêneros.xlsx')  ####  DEBUG  #####

        return df_tratado



    @property
    def _colunas_base(self) -> list:
        num_columns = len(self.leitura.columns)

        # Create new column names dynamically based on the actual number of columns
        nomes_colunas = self.colunas_list + [f'Extra_{i}' for i in range(num_columns - 9)]
        # Ensure the number of new column names matches the number of columns in the DataFrame

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
