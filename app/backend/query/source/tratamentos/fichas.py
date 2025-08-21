from pandas import DataFrame, Series


class TratamentoFichas:
    #todo: Dividir responsabilidades.

    def __init__(self, leitura: DataFrame):
        # print(f'TratamentoFichas instanciada')
        self.df = leitura
        # print(f"TratamentoFichas.df_integrado: {list(self.df_integrado.columns)}\n")
        self.df_tratado = self.tratar(df_leitura=leitura)


    def tratar(self, df_leitura):
        df_base = self.definir_df_base(df_leitura)

        dict_series_iniciais = self.definir_series(df_base)

        dict_splits = self.dicionário_splits(dict_series_iniciais)

        dict_colunas = self.definir_colunas(dict_splits)

        df_tratado = DataFrame(dict_colunas)

        df_tratado = self.ajustar_df(df_tratado)
        # print(f'Fichas.df_tratado: \n{df_tratado.head(15)}\n\n')

        return df_tratado

    @staticmethod
    def definir_df_base(df_leitura: DataFrame) -> DataFrame:
        #todo: reler
        df_base = df_leitura
        colunas_recebidas: list[str] = list(df_base.columns)
        colunas_esperadas: list[str] = ['Unnamed: 0', 'ESTADO DE GOIÁS', 'Unnamed: 1', 'Unnamed: 2', 'Unnamed: 3']
        if colunas_recebidas != colunas_esperadas :
            diferencas = [
                f"Esperado: '{e}' | Recebido: '{r}'" for e, r in zip(colunas_esperadas, colunas_recebidas) if e != r
            ]
            # Verifica se há colunas extras ou faltando
            if len(colunas_recebidas) != len(colunas_esperadas) :
                diferencas.append(
                    f"Tamanhos diferentes: esperadas {len(colunas_esperadas)} colunas, recebidas {len(colunas_recebidas)}")

            raise ValueError(f'Colunas não correspondem:\n' + '\n'.join(diferencas))
        df_base.columns = [str(i) for i in range(1, 6)]
        return df_base


    @staticmethod
    def definir_series(df_base) -> dict:
        def seriar(
                coluna1: str = None,
                coluna2: str = None,
                shift1: int = 0,
                shift2: int = 0
        ) -> Series:

            if coluna1 and not coluna2:
                return df_base[coluna1].shift(shift1).astype(str)
            elif coluna1 and coluna2:
                serie1 = df_base[coluna1].shift(shift1).astype(str)
                serie2 = df_base[coluna2].shift(shift2).astype(str)
                return serie1 + serie2
            else:
                return ""

        dict_series_base =  {
            'A'     : (A  := seriar('1')),
            'B'     : (B  := seriar('2')),
            'C'     : (C  := seriar('3')),
            'D'     : (D  := seriar('4')),
            'A_B'   : (A_B := A.str[::-1] + B),
            'AB'    : (AB := A + B),
            'CD'    : (CD := seriar('3', '4')),
            'B__'   : (B__ := (seriar('2', shift1=-5).str[::-1])),
            'B__A'  : (B__A := B__ + A)

        }

        # DataFrame(dict_series_base).to_excel(fr'fichas\series_iniciais.xlsx')
        return dict_series_base



    @staticmethod
    def dicionário_splits(series: dict) -> dict:
        def splitar(serie, separador: str):
            if isinstance(serie, str):
                # Caso seja o nome de uma coluna original no dicionário
                série = series[serie]
            else:
                # Caso seja resultado de um split anterior (DataFrame ou Series)
                série = serie

            split = série.str.split(separador, expand=True)
            return split

        dicionário_splits = {
            'turma'                 : splitar('A', 'Turma: '),
            'matrícula'             : splitar('A', 'SEE: '),
            'número chamada'        : splitar('B', 'Número para chamada: '),
            'estudante'             : splitar('A', r'\(a\): '),
            'cpf aluno'             : splitar('B', 'CPF: '),
            'data nascimento'       : splitar('A', 'Nascimento: '),
            'data matrícula'        : splitar('A', 'Data da matrícula: '),
            'endereço logradouro'   : splitar('A', 'Logradouro: '),
            'endereço complemento'  : splitar('A', 'Complemento:'),
            'endereço número'       : splitar('A_B', ':oruodargoLNúmero'),
            'endereço bairro'       : splitar('B', 'Bairro '),
            'endereço município'    : splitar('A', 'Município: '),
            'endereço cep'          : splitar('B', 'CEP: '),
            'responsável'           : splitar('A', 'Nome Responsável:'),
            'filiação 1'            : splitar('A', 'Filiação 1: '),
            'filiação 1 cpf'        : splitar('B__A', 'oremúNCPF: '),
            'filiação 1 prof'       : splitar('A_B', ':1 oãçailiFProfissão:'),
            'filiação 2'            : splitar('A', 'Filiação 2: '),
            'filiação 2 cpf'        : splitar('B__A', ':PECCPF: '),
            'filiação 2 prof'       : splitar('A_B', ' :2 oãçailiFProfissão:'),

            'cn base 1'             : (cn_base := splitar('B', 'Livro:')),

            'cn termo'              : splitar(cn_base[0], 'Certidão nasc.:'),
            'cn livro'              : splitar('B', 'Livro:'),
            'cn folha'              : splitar('CD', 'Folha:'),

            'cn grande'             : splitar(cn_base[0], 'No Matrícula: '),

            'naturalidade município': splitar('A', 'Naturalidade: '),
            'ufx'                   : (ufx := splitar('B', 'Nacionalidade')),
            'uf'                    : splitar(ufx[0], 'UF:'),
            'rg'                    : splitar('A', 'C.I:'),
            'rg emissor'            : splitar('B', 'Orgão Expedidor: '),
            'nacionalidade' : splitar('CD', 'País de origem:'),
            'turno' : splitar('B', 'Turno: ')
        }
        # print(dicionário_splits['filiação1_cpfx'])
        return dicionário_splits

    @staticmethod
    def definir_colunas(dicionário_splits: dict):
        def colunar(
                chave: str,
                shift: int = 0,
                índice: int = 1) -> Series:
            return dicionário_splits[chave][índice].shift(shift)

        dicionário_colunas_finais = {
            #Todo: Localizar o momento que há um "empurrão" parcial nas colunas verticalmente
            'Turma'                           : colunar('turma', -27),
            'Matrícula'                       : colunar('matrícula', -6),
            'Nº'                              : colunar('número chamada', -6),
            'Estudante'                       : colunar('estudante', -7),
            'Data de Nascimento'              : colunar('data nascimento', -8),
            'CPF Aluno'                       : colunar('cpf aluno', -11),
            'Data Matrícula'                  : colunar('data matrícula', -28),
            'Endereço: Logradouro'            : colunar('endereço logradouro', -21, 1),
            'Endereço: Complemento'           : colunar('endereço complemento', -22),
            'Endereço: Número'                : colunar('endereço número', -21),
            'Endereço: Bairro'                : colunar('endereço bairro', -22),
            'Endereço: Município'             : colunar('endereço município', -23, 1),
            'Endereço: CEP'                   : colunar('endereço cep', -23),
            'Nome Responsável'                : colunar('responsável', -12),
            'Filiação 1'                      : colunar('filiação 1', -15),
            'Filiação 1 - CPF'                : colunar('filiação 1 cpf', -16),
            'Filiação 1 - Profissão'          : colunar('filiação 1 prof', -15),
            'Filiação 2'                      : colunar('filiação 2', -17),
            'Filiação 2 - CPF'                : colunar('filiação 2 cpf', -18),
            'Filiação 2 - Profissão'          : colunar('filiação 2 prof', -17),
            'Certidão de Nascimento - Modelo novo' : colunar('cn grande', -8),
            'Certidão de Nascimento: Termo'   : colunar('cn termo', -8),
            'Certidão de Nascimento: Livro'   : colunar('cn livro', -8),
            'Certidão de Nascimento: Folha'   : colunar('cn folha', -8),
            'UF de Naturalidade'              : colunar('uf', -9),
            'Município de Naturalidade'       : colunar('naturalidade município', -9),
            'Nacionalidade'                   : colunar('nacionalidade', -9),
            'Turno'                           : colunar('turno', -27),
            'RG do Aluno'                     : colunar('rg', -10),
            'RG do Aluno: Emissor'            : colunar('rg emissor', -10),
        }
        return dicionário_colunas_finais



    @staticmethod
    def ajustar_df(df_tratado: DataFrame) -> DataFrame:
        # df_integrado = df_tratado.drop(columns=self.colunas_iniciais)
        df = df_tratado.reset_index(drop=True)
        df = df.dropna(axis=0, how='all', ignore_index=True)
        return df


    # def __getattr__(self, item):
    #     return getattr(self.df_tratado, item)

