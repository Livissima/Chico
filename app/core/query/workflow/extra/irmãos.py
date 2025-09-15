from pandas import DataFrame


class Irmão:
    def __init__(self, consulta: DataFrame):
        self.localizar_irmãos(consulta)


#TODO: arrumar essa porcaria toda, de forma que aceite ambas as filiações como parâmetros e gere apropriadamente
# os dois irmãos.
# Talvez seja mais apropriado retornar apenas a coluna, como em `consulta['Irmão']`

    @staticmethod
    def localizar_irmãos(consulta):
        for índice, row in consulta.iterrows():
            cpf_mãe = row['Filiação 1 - CPF']

            irmãos = consulta[consulta['Filiação 1 - CPF'] == cpf_mãe]

            if len(irmãos) == 2:
                nomes_irmãos = irmãos['Estudante'].tolist()
                nomes_irmãos.remove(row['Estudante'])
                consulta.at[índice, 'Irmão 1'] = nomes_irmãos[0]
            elif len(irmãos) == 3:
                nomes_irmãos = irmãos['Estudante'].tolist()
                nomes_irmãos.remove(row['Estudante'])
                consulta.at[índice, 'Irmão 1'] = nomes_irmãos[0]

        irmão = None
        try:
            irmão = consulta['Irmão 1'] = consulta['Irmão 1'].fillna('')
        except KeyError as e:
            print(f'erro com irmão: {e}')

        return irmão