from pathlib import Path

from pandas import DataFrame

from app.core import ConsultaEstudantes


class ExportaçãoCSV:
    NOME_CSV = 'Contatos Google'

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

    def __init__(self, consulta: ConsultaEstudantes, path: Path):
        self._exportar(consulta, path)

    def _exportar(self, df, _path):
        dict_contatos = self._dicionarizar(df)
        df_contatos = DataFrame(data=dict_contatos, columns=self.colunas_CSV)
        df_contatos.to_csv(Path(_path, f'{self.NOME_CSV}.csv'))

    @staticmethod
    def _dicionarizar(consulta) -> dict:
        return {
            'First Name'          : consulta.apply(
                lambda linha: f"{linha['Estudante']} - Transferido" if linha['Situação'] == '(transferido)'
                else f"{linha['Estudante']} - {linha['Turma']}", axis=1
            ),
            'Birthday'            : consulta['Data de Nascimento'],
            'Labels'              : consulta['Turma'] + ' ::: * myContacts',
            'Phone 1 - Value'     : consulta['Telefone 1'] + ' ::: ' + consulta['Telefone 2'] + ' ::: ' + consulta['Telefone 3'],
            'Relation 1 - Value'  : consulta['Irmão 1'],
            'Relation 1 - Label'  : 'Irmão(ã)'
        }

