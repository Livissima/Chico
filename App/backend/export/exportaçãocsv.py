import os

from pandas import DataFrame


class ExportaçãoCSV:

    colunas_CSV: list[str] = [
        "First Name", "Middle Name", "Last Name", "Phonetic First Name", "Phonetic Middle Name", "Phonetic Last Name",
        "Name Prefix", "Name Suffix",
        "Nickname", "File As", "Organization Name", "Organization Title", "Organization Department", "Birthday",
        "Notes", "Photo", "Labels",
        "E-mail 1 - Label", "E-mail 1 - Value", "Phone 1 - Label", "Phone 1 - Value", "Relation 1 - Label",
        "Relation 1 - Value", "Relation 2 - Label", "Relation 2 - Value"
    ]

    colunas_relevantes: list[str] = [
        'Estudante', 'Data de Nascimento', 'Turma', 'Telefone 1', 'Telefone 2', 'Telefone 3', 'Irmão 1', 'Irmão 2'
    ]

    def __init__(self, consulta: DataFrame, path: str):
        self.path = os.path.join(path, 'Contatos Google.csv')
        self.consulta = consulta

        self.csv = self.atribuir(self.consulta)


        self._exportar()



    def atribuir(self, consulta):

        colunas_dict: dict = {

            # 'First Name'          : consulta.apply(
            #     lambda row: f"{row['Estudante']} - Transferido" if row['Situação'] == '(transferido)'
            #     else f"{row['Estudante']} - {row['Turma']}", axis=1
            # ),
            'First Name'          : consulta.apply(
                lambda row: f"{row['Estudante']} - Transferido" if row['Situação'] == '(transferido)'
                else f"{row['Estudante']} - {row['Turma']}", axis=1
            ),
            'Birthday'            : consulta['Data de Nascimento'],
            'Labels'              : consulta['Turma'] + ' ::: * myContacts',
            'Phone 1 - Value'     : consulta['Telefone 1'] + ' ::: ' + consulta['Telefone 2'] + ' ::: ' + consulta['Telefone 3'],
            'Relation 1 - Value'  : consulta['Irmão 1'],
            'Relation 1 - Label'  : 'Irmão(ã)'
        }
        return DataFrame(data=colunas_dict, columns=self.colunas_CSV)

    def _exportar(self):
        self.csv.to_csv(self.path)

