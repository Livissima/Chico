import warnings
from openpyxl import __name__ as openpyxl_name
import pandas as pd
import unicodedata

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
