import pandas as pd
from pathlib import Path
import re

# Configuração dos caminhos
pasta_estudantes = Path(r'C:\Users\meren\OneDrive - Secretaria de Estado da Educação\Secretaria\Estudantes')
path_db = Path(r'C:\Users\meren\OneDrive - Secretaria de Estado da Educação\SIGE\Database.xlsx')


def extrair_matricula_da_pasta(nome_pasta) :
    """
    Extrai o número de matrícula do nome da pasta
    Formato esperado: "Nome do Estudante   ~   123456789"
    """
    # Procurar por padrão de matrícula (números após ~)
    match = re.search(r'~\s*(\d+)', nome_pasta)
    if match :
        return match.group(1)
    return None


def tem_dois_ou_mais_digitos(nome_arquivo) :
    """
    Verifica se o nome do arquivo (sem extensão) contém pelo menos 2 dígitos
    """
    nome_sem_extensao = Path(nome_arquivo).stem
    quantidade_digitos = sum(c.isdigit() for c in nome_sem_extensao)
    return quantidade_digitos >= 2


print("Carregando database...")
# Carregar database
database = pd.read_excel(path_db)
database = database[['Turma', 'Matrícula', 'Estudante']]
# Converter matrícula para string para facilitar comparação
database['Matrícula'] = database['Matrícula'].astype(str).str.strip()

print("Analisando estrutura de pastas...\n")

# Listas para armazenar os resultados
dados_relatorio = []

# Percorrer toda a estrutura
total_pastas = 0

for pasta_letra in sorted(pasta_estudantes.iterdir()) :
    if not pasta_letra.is_dir() :
        continue

    for pasta_aluno in sorted(pasta_letra.iterdir()) :
        if not pasta_aluno.is_dir() :
            continue

        total_pastas += 1
        nome_completo_pasta = pasta_aluno.name
        caminho_relativo = f"{pasta_letra.name}/{pasta_aluno.name}"

        # Extrair matrícula do nome da pasta
        matricula = extrair_matricula_da_pasta(nome_completo_pasta)

        # Coletar todos os PDFs da pasta
        arquivos_pdf = list(pasta_aluno.glob("*.pdf"))

        # CASO 1: Pasta vazia
        if not arquivos_pdf :
            dados_relatorio.append({
                'Pasta' : caminho_relativo, 'Matrícula' : matricula, 'Estudante' : None,  # Será preenchido depois
                'Turma' : None,  # Será preenchido depois
                'Motivo' : 'Pasta vazia', 'Arquivos_problema' : 'Nenhum arquivo encontrado'
            })
            continue

        # CASO 2: Verificar arquivos com 2+ dígitos
        arquivos_com_digitos = []
        for arquivo in arquivos_pdf :
            if tem_dois_ou_mais_digitos(arquivo.name) :
                arquivos_com_digitos.append(arquivo.name)

        if arquivos_com_digitos :
            dados_relatorio.append({
                'Pasta' : caminho_relativo, 'Matrícula' : matricula, 'Estudante' : None, 'Turma' : None,
                'Motivo' : 'Arquivos não padronizados', 'Arquivos_problema' : ', '.join(sorted(arquivos_com_digitos))
            })

print(f"Total de pastas analisadas: {total_pastas}")
print(f"Pastas com problemas: {len(dados_relatorio)}")

# Criar DataFrame com os resultados
df_relatorio = pd.DataFrame(dados_relatorio)

# Se houver resultados, fazer o merge com o database
if not df_relatorio.empty :
    print("\nEnriquecendo dados com informações do database...")

    # Fazer merge com database usando a matrícula
    df_relatorio = df_relatorio.merge(database[['Matrícula', 'Estudante', 'Turma']], on='Matrícula', how='left',
        suffixes=('', '_db'))

    # Preencher nome do estudante com o valor do database quando disponível
    # Se não encontrar no database, manter o nome extraído da pasta
    df_relatorio['Estudante'] = df_relatorio['Estudante_db'].combine_first(df_relatorio['Estudante'])

    # Garantir que Turma está preenchida (mesmo que seja NaN)
    df_relatorio['Turma'] = df_relatorio['Turma_db']

    # Remover colunas auxiliares
    df_relatorio = df_relatorio.drop(['Estudante_db', 'Turma_db'], axis=1)

    # Identificar matrículas não encontradas no database
    df_relatorio['Matrícula_encontrada_db'] = ~df_relatorio['Estudante'].isna()
else :
    print("\nNenhum problema encontrado!")

# Ordenar por Turma e depois por Estudante
if not df_relatorio.empty :
    # Preencher valores vazios com string vazia para ordenação
    df_relatorio['Turma'] = df_relatorio['Turma'].fillna('ZZZ_Sem_Turma')
    df_relatorio['Estudante'] = df_relatorio['Estudante'].fillna('Nome não encontrado')

    # Ordenar
    df_relatorio = df_relatorio.sort_values(['Turma', 'Estudante'])

    # Reverter NaN para None (opcional, para o Excel ficar mais limpo)
    df_relatorio['Turma'] = df_relatorio['Turma'].replace('ZZZ_Sem_Turma', None)
    df_relatorio['Estudante'] = df_relatorio['Estudante'].replace('Nome não encontrado', None)

# Estatísticas por motivo
print("\n" + "=" * 60)
print("ESTATÍSTICAS POR MOTIVO")
print("=" * 60)
motivos = df_relatorio['Motivo'].value_counts()
for motivo, count in motivos.items() :
    print(f"{motivo}: {count}")

# Matrículas não encontradas no database
nao_encontradas = df_relatorio[df_relatorio['Estudante'].isna()]
if not nao_encontradas.empty :
    print(f"\n⚠️  Matrículas não encontradas no database: {len(nao_encontradas)}")

# Preparar DataFrame final para exportação
df_export = df_relatorio.copy()

# Reordenar colunas para melhor visualização
colunas_ordenadas = ['Turma', 'Estudante', 'Matrícula', 'Motivo', 'Arquivos_problema', 'Pasta']
colunas_existentes = [col for col in colunas_ordenadas if col in df_export.columns]
df_export = df_export[colunas_existentes]

# Exportar para Excel
caminho_excel = pasta_estudantes.parent / 'Relatório pastas estudantes.xlsx'
try :
    with pd.ExcelWriter(caminho_excel, engine='openpyxl') as writer :
        # Planilha principal com todos os problemas
        df_export.to_excel(writer, sheet_name='Pastas com problemas', index=False)

        # Planilha com estatísticas
        estatisticas = pd.DataFrame({
            'Métrica' : ['Total de pastas analisadas', 'Pastas com problemas', 'Pastas vazias',
                         'Pastas com arquivos não padronizados', 'Matrículas não encontradas no DB'],
            'Valor' : [total_pastas, len(df_relatorio), len(df_relatorio[df_relatorio['Motivo'] == 'Pasta vazia']),
                       len(df_relatorio[df_relatorio['Motivo'] == 'Arquivos não padronizados']), len(nao_encontradas)]
        })
        estatisticas.to_excel(writer, sheet_name='Estatísticas', index=False)

        # Se houver matrículas não encontradas, criar uma planilha separada
        if not nao_encontradas.empty :
            nao_encontradas[['Pasta', 'Matrícula']].to_excel(writer, sheet_name='Matrículas não encontradas',
                index=False)

    print(f"\n✅ Relatório exportado com sucesso para: {caminho_excel}")

    # Mostrar preview
    print("\n" + "=" * 60)
    print("PREVIEW DO RELATÓRIO (primeiras 10 linhas)")
    print("=" * 60)
    print(df_export.head(10).to_string())

except Exception as e :
    print(f"\n❌ Erro ao exportar Excel: {e}")

    # Fallback: salvar como CSV
    caminho_csv = pasta_estudantes.parent / 'Relatório pastas estudantes.csv'
    df_export.to_csv(caminho_csv, index=False, encoding='utf-8-sig')
    print(f"✅ Relatório salvo como CSV em: {caminho_csv}")

print("\n" + "=" * 60)
print("PROCESSO CONCLUÍDO!")
print("=" * 60)