import pandas as pd
import os
from pathlib import Path

# Configuração dos caminhos
path_pasta_raiz = Path(r'C:\Users\meren\Desktop\Fotos')
path_db = Path(r'C:\Users\meren\OneDrive - Secretaria de Estado da Educação\SIGE\Database.xlsx')

# Carregar e preparar o database
database = pd.read_excel(path_db)
database = database[['Matrícula', 'Estudante']]

# Criar um dicionário para facilitar a busca (nome do estudante -> matrícula)
# Remover espaços extras e padronizar para comparação
mapa_estudantes = {}
for _, row in database.iterrows() :
    nome_limpo = str(row['Estudante']).strip().upper()  # Padronizar para maiúsculas
    matricula = str(row['Matrícula']).strip()
    mapa_estudantes[nome_limpo] = matricula

# Contadores para relatório final
total_renomeados = 0
total_nao_encontrados = 0
nao_encontrados_lista = []

# Percorrer todas as subpastas
for pasta_atual in path_pasta_raiz.iterdir() :
    if pasta_atual.is_dir() :  # Verificar se é uma pasta
        print(f"\nProcessando pasta: {pasta_atual.name}")

        # Percorrer todos os arquivos .jpg e .jpeg na pasta atual
        for extensao in ['*.jpg', '*.jpeg'] :
            for arquivo in pasta_atual.glob(extensao) :
                nome_arquivo = arquivo.stem  # Nome sem extensão
                extensao_original = arquivo.suffix  # Extensão original (.jpg ou .jpeg)
                nome_arquivo_limpo = nome_arquivo.strip().upper()

                # Verificar se o nome está no database
                if nome_arquivo_limpo in mapa_estudantes :
                    matricula = mapa_estudantes[nome_arquivo_limpo]

                    # Criar novo nome do arquivo mantendo a extensão original
                    novo_nome = pasta_atual / f"{matricula}{extensao_original}"

                    # Verificar se já existe um arquivo com este nome
                    if not novo_nome.exists() :
                        # Renomear o arquivo
                        arquivo.rename(novo_nome)
                        print(f"  Renomeado: {nome_arquivo}{extensao_original} -> {matricula}{extensao_original}")
                        total_renomeados += 1
                    else :
                        print(
                            f"  AVISO: Arquivo {matricula}{extensao_original} já existe! Pulando {nome_arquivo}{extensao_original}")
                        total_nao_encontrados += 1
                        nao_encontrados_lista.append(f"{pasta_atual.name}/{nome_arquivo}{extensao_original}")
                else :
                    print(f"  AVISO: Estudante '{nome_arquivo}' não encontrado na planilha!")
                    total_nao_encontrados += 1
                    nao_encontrados_lista.append(f"{pasta_atual.name}/{nome_arquivo}{extensao_original}")

# Relatório final
print("\n" + "=" * 50)
print("RELATÓRIO FINAL")
print("=" * 50)
print(f"Total de arquivos renomeados com sucesso: {total_renomeados}")
print(f"Total de arquivos não encontrados na planilha: {total_nao_encontrados}")

if nao_encontrados_lista :
    print("\nArquivos não encontrados na planilha:")
    for item in nao_encontrados_lista :
        print(f"  - {item}")

print("\nProcesso concluído!")