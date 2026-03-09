import pandas as pd
import os
from pathlib import Path

# Configuração dos caminhos
path_pasta_backup = Path(r'C:\Users\meren\Desktop\Fotos')
path_pasta_original = Path(r'C:\Users\meren\Pictures\Camera Roll')
path_db = Path(r'C:\Users\meren\OneDrive - Secretaria de Estado da Educação\SIGE\Database.xlsx')

# Carregar database para referência dos nomes dos alunos
database = pd.read_excel(path_db)
database = database[['Matrícula', 'Estudante']]

# Criar dicionário para lookup (matrícula -> nome)
mapa_matriculas = {}
for _, row in database.iterrows() :
    matricula = str(row['Matrícula']).strip()
    nome = str(row['Estudante']).strip()
    mapa_matriculas[matricula] = nome


# Função para coletar todos os arquivos .jpg de uma pasta (incluindo subpastas)
def coletar_arquivos_jpg(pasta_raiz) :
    arquivos = set()
    arquivos_com_caminho = {}

    for arquivo in pasta_raiz.rglob("*.jpg") :
        nome_arquivo = arquivo.stem  # Nome sem extensão
        arquivos.add(nome_arquivo)
        arquivos_com_caminho[nome_arquivo] = arquivo

    return arquivos, arquivos_com_caminho


print("Coletando arquivos...")
print("-" * 50)

# Coletar arquivos de ambas as pastas
arquivos_backup, backup_com_caminho = coletar_arquivos_jpg(path_pasta_backup)
arquivos_original, original_com_caminho = coletar_arquivos_jpg(path_pasta_original)

print(f"Total de arquivos no Backup: {len(arquivos_backup)}")
print(f"Total de arquivos no Original: {len(arquivos_original)}")
print()

# Encontrar diferenças
so_no_backup = arquivos_backup - arquivos_original
so_no_original = arquivos_original - arquivos_backup
em_ambos = arquivos_backup & arquivos_original


# Função para obter nome do aluno a partir da matrícula
def get_nome_aluno(matricula) :
    return mapa_matriculas.get(matricula, "NÃO ENCONTRADO NA PLANILHA")


print("=" * 60)
print("ARQUIVOS QUE ESTÃO APENAS NO BACKUP")
print("=" * 60)
if so_no_backup :
    for matricula in sorted(so_no_backup) :
        caminho = backup_com_caminho[matricula]
        nome_aluno = get_nome_aluno(matricula)
        print(f"📁 {matricula}.jpg")
        print(f"   👤 Aluno: {nome_aluno}")
        print(f"   📍 Caminho: {caminho}")
        print()
    print(f"Total: {len(so_no_backup)} arquivos")
else :
    print("Nenhum arquivo exclusivo do backup encontrado.\n")

print("=" * 60)
print("ARQUIVOS QUE ESTÃO APENAS NO ORIGINAL")
print("=" * 60)
if so_no_original :
    for matricula in sorted(so_no_original) :
        caminho = original_com_caminho[matricula]
        nome_aluno = get_nome_aluno(matricula)
        print(f"📁 {matricula}.jpg")
        print(f"   👤 Aluno: {nome_aluno}")
        print(f"   📍 Caminho: {caminho}")
        print()
    print(f"Total: {len(so_no_original)} arquivos")
else :
    print("Nenhum arquivo exclusivo do original encontrado.\n")

print("=" * 60)
print("RESUMO")
print("=" * 60)
print(f"📊 Arquivos em ambas as pastas: {len(em_ambos)}")
print(f"📊 Arquivos apenas no Backup: {len(so_no_backup)}")
print(f"📊 Arquivos apenas no Original: {len(so_no_original)}")
print(f"📊 Total geral de arquivos únicos: {len(arquivos_backup) + len(arquivos_original) - len(em_ambos)}")

# Opcional: Salvar relatório em arquivo texto
if so_no_backup or so_no_original :
    salvar_relatorio = input("\nDeseja salvar este relatório em um arquivo? (s/n): ").lower()
    if salvar_relatorio == 's' :
        with open('relatorio_comparacao_pastas.txt', 'w', encoding='utf-8') as f :
            f.write("RELATÓRIO DE COMPARAÇÃO DE PASTAS\n")
            f.write("=" * 60 + "\n\n")

            f.write("ARQUIVOS APENAS NO BACKUP:\n")
            f.write("-" * 40 + "\n")
            for matricula in sorted(so_no_backup) :
                caminho = backup_com_caminho[matricula]
                nome_aluno = get_nome_aluno(matricula)
                f.write(f"{matricula}.jpg - Aluno: {nome_aluno}\n")
                f.write(f"  Caminho: {caminho}\n\n")

            f.write("\nARQUIVOS APENAS NO ORIGINAL:\n")
            f.write("-" * 40 + "\n")
            for matricula in sorted(so_no_original) :
                caminho = original_com_caminho[matricula]
                nome_aluno = get_nome_aluno(matricula)
                f.write(f"{matricula}.jpg - Aluno: {nome_aluno}\n")
                f.write(f"  Caminho: {caminho}\n\n")

            f.write("\n" + "=" * 60 + "\n")
            f.write("RESUMO:\n")
            f.write(f"Arquivos em ambas: {len(em_ambos)}\n")
            f.write(f"Apenas no Backup: {len(so_no_backup)}\n")
            f.write(f"Apenas no Original: {len(so_no_original)}\n")

        print(f"✅ Relatório salvo como 'relatorio_comparacao_pastas.txt'")