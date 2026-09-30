import os
from pathlib import Path


def abrir_pdfs_recursivo(caminho_base) :
    # Converte para um objeto Path do pathlib
    pasta = Path(caminho_base)

    # Verifica se o diretório existe
    if not pasta.exists() :
        print(f"O caminho {caminho_base} não foi encontrado.")
        return

    # O método rglob('*.pdf') busca recursivamente por arquivos PDF em todas as subpastas
    for arquivo_pdf in pasta.rglob('*.pdf') :
        try :
            print(f"Abrindo: {arquivo_pdf}")
            # No Windows, os.startfile abre o arquivo com o programa padrão associado (.pdf)
            os.startfile(arquivo_pdf)
        except Exception as e :
            print(f"Erro ao abrir o arquivo {arquivo_pdf.name}: {e}")


# Executando a função para o diretório informado
caminho_obra = r"C:\Users\meren\Desktop\Obra"
abrir_pdfs_recursivo(caminho_obra)