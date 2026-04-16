import json
import re
import warnings
from openpyxl import __name__ as openpyxl_name
import pandas as pd
import unicodedata
from pathlib import Path


def obter_string_numérica(número: str) -> str :
    if not número :
        return '-'
    return re.sub(r'\D', '', str(número))

def normalizar_diacrítica(texto) -> str:
    import unicodedata

    return ''.join(
        c for c in unicodedata.normalize('NFKD', texto)
        if not unicodedata.combining(c)
    )

def ler_json(caminho: Path) -> dict:
    try:
        with open(caminho, 'r', encoding='utf-8') as arquivo:
            return json.load(arquivo)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def normalizar_unicode(texto: str) -> str:
    if texto is None:
        return ''
    nfkd = unicodedata.normalize('NFKD', str(texto))
    só_ascii = ''.join(chave for chave in nfkd if not unicodedata.combining(chave))
    return só_ascii.lower().strip()

def normalizar_dicionário(dicionário: dict | None):
    if not dicionário:
        return {}
    return {normalizar_unicode(chave): valor for chave, valor in dicionário.items()}

def ajustar_print_pandas():
    pd.set_option('display.max_columns', None)
    pd.set_option('display.expand_frame_repr', False)  # Evita quebra do DataFrame em múltiplas linhas
    pd.set_option('display.width', None)  # Ajusta automaticamente à largura do terminal
    warnings.filterwarnings('ignore', category=UserWarning, module=openpyxl_name)

def escrever_json(conteúdo, _path, indent: int = 0):
    with open(_path, 'w', encoding='utf-8') as arquivo :
        json.dump(conteúdo, arquivo, ensure_ascii=False, indent=indent)


