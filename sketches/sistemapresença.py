from pandas import DataFrame, ExcelWriter
from pypdf import PdfReader
from pathlib import Path

from app.config.parâmetros import parâmetros


def ler_pdf(path: Path):
    reader = PdfReader(path)
    string_dump = ""
    for página in reader.pages:
        string_dump += página.extract_text()

    return string_dump

_path = Path(r'C:\Users\meren\Downloads', 'formulario_completo_52034860-1.pdf')
leitura = ler_pdf(_path)


snome = 'Nome: '
sresp = 'Responsável familiar: '
sdn = 'Dt. Nasc.: '
ssérie = 'Série: '

linhas = leitura.split('\n')
nomes = [linha.replace(snome, '').replace('Dados dos Estudantes', '').title() for linha in linhas if snome in linha]
responsáveis = [linha.replace(sresp, '').title() for linha in linhas if linha.startswith(sresp)]
dns = [linha.replace(sdn, '')[0:10] for linha in linhas if linha.startswith(sdn)]

for linha in linhas: print(linha)
dados = [nomes, responsáveis, dns]

df = DataFrame()
df['Estudante'] = nomes
df['Responsável'] = responsáveis
df['Data de Nascimento'] = dns


nome_relatório = 'Relação de estudantes - Sistema Presença'
path_relatório = Path(r'C:\Users\meren\OneDrive - Secretaria de Estado da Educação\Secretaria', nome_relatório)
with ExcelWriter(f'{path_relatório}.xlsx', engine='xlsxwriter') as writer:
    df.to_excel(writer, sheet_name='Lista')
