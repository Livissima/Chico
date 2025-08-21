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

        consulta['Irmão 1'] = consulta['Irmão 1'].fillna('')

        return consulta['Irmão 1']




#versão anterior
# Iterar sobre cada estudante
# consulta['Irmão 1'] = None
# consulta['Irmão 2'] = None
#
# for index, row in consulta.iterrows():
#     CPF_mãe = row['Filiação 1 - CPF']
#
#     # Filtrar estudantes com o mesmo nome de mãe
#     irmãos = consulta[consulta['Filiação 1 - CPF'] == CPF_mãe]
#
#     # Verificar quantos irmãos existem
#     if len(irmãos) == 2:
#         # Se houver um irmão, atribuir o nome do irmão
#         irmãos_nomes = irmãos['Estudante'].tolist()
#         irmãos_nomes.remove(row['Estudante'])  # Remove o próprio estudante
#         consulta.at[index, 'Irmão 1'] = irmãos_nomes[0]  # Atribui o irmão
#     elif len(irmãos) == 3:
#         # Se houver dois irmãos, atribuir os nomes dos irmãos
#         irmãos_nomes = irmãos['Estudante'].tolist()
#         irmãos_nomes.remove(row['Estudante'])  # Remove o próprio estudante
#         consulta.at[index, 'Irmão 1'] = irmãos_nomes[0]  # Atribui o primeiro irmão
#         consulta.at[index, 'Irmão 2'] = irmãos_nomes[1]  # Atribui o segundo irmão