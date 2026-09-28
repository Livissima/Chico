from pandas import DataFrame, ExcelWriter
from pypdf import PdfReader
from pathlib import Path

def ler_pdf(path: Path):
    reader = PdfReader(path)
    string_dump = ""
    for página in reader.pages:
        string_dump += página.extract_text()

    return string_dump

_path = Path(r'C:\Users\meren\Downloads', 'sistemapresençaagoset.pdf')
leitura = ler_pdf(_path)


snome = 'Nome: '
sresp = 'Responsável familiar: '
sdn = 'Dt. Nasc.: '
ssérie = 'Série: '

linhas = [linha.strip() for linha in leitura.split('\n')]

# Usamos 'in' em vez de 'startswith' para evitar problemas com formatação do PDF
nomes = [linha.replace(snome, '').replace('Dados dos Estudantes', '').title().strip() for linha in linhas if snome in linha]
responsáveis = [linha.replace(sresp, '').title().strip() for linha in linhas if sresp in linha]
dns = [linha.replace(sdn, '').strip()[0:10] for linha in linhas if sdn in linha]

# Alerta de segurança: se o PDF tiver um layout onde um aluno não tem responsável,
# as listas ainda podem ficar com tamanhos desalinhados.
# Para garantir que o DataFrame seja criado sem quebrar, você pode montá-lo assim:
dados = {
    'Estudante': nomes,
    'Responsável': responsáveis,
    'Data de Nascimento': dns
}

# Criamos o DataFrame garantindo que o Pandas lide com a diferença de tamanhos (caso falte algum dado)
df = DataFrame.from_dict(dados, orient='index').transpose()


nome_relatório = 'Formulário Sistema Presença Ago-Set 2026'
path_relatório = Path(r'C:\Users\meren\Downloads', nome_relatório)
with ExcelWriter(f'{path_relatório}.xlsx', engine='xlsxwriter') as writer:
    df.to_excel(writer, sheet_name='Lista')
