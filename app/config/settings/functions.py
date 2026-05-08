import json
import os
import re
import sys
import time
import warnings
from functools import wraps
from typing import Any

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


def escrever_json(conteúdo: Any, caminho_arquivo: str | Path, indent: int = 4) :

    path = Path(caminho_arquivo)
    path.parent.mkdir(parents=True, exist_ok=True)

    try :
        with open(path, 'w', encoding='utf-8') as arquivo :
            json.dump(
                conteúdo,
                arquivo,
                ensure_ascii=False,
                indent=indent,
                default=str
            )

    except (TypeError, OverflowError) as e :
        print(f"Erro ao serializar JSON: {e}")

    except IOError as e :
        print(f"Erro de E/S ao salvar o arquivo: {e}")


def truncar_diretório(path: str | Path) -> str:
    diretório = str(path).split('\\')
    diretório = os.path.join(*diretório[0 :3], '...', '...', *diretório[-2 :])
    diretório = diretório.replace(':', ':\\')
    return diretório


def str_exception(e: TypeError | Exception) -> str:
    return str(e).split('\n')[0]


def Print(ação: str, valor: Any, valor2: Any = None) -> None :
    """Função utilitária para prints coloridos no terminal."""
    ESTILOS = {
        bool : "\033[3;35m", int : "\033[0;34m", float : "\033[1;34m", str : "\033[0;32m", None : "\033[2;37m",
        "AÇÃO" : "\033[0m", "RESET" : "\033[0m", list : "\033[0;36m", dict : "\033[0;33m",
    }

    def formatar(v) :
        cor = ESTILOS.get(type(v), "")
        return f"{cor}{v}{ESTILOS['RESET']}"

    prefixo = f"{ESTILOS['AÇÃO']}{ação}:{ESTILOS['RESET']}"

    if valor2 is not None :
        mensagem = f"{prefixo} {formatar(valor)} – {formatar(valor2)}"
    else :
        mensagem = f"{prefixo} {formatar(valor)}"

    sys.stdout.write(mensagem + "\n")
    sys.stdout.flush()


def debugar(func_ou_pausa=None, *, pausa: int | float = 0) :
    """Decorador para rastrear execução de funções e pausar se necessário."""
    real_pausa = pausa
    if isinstance(func_ou_pausa, (int, float)) :
        real_pausa = func_ou_pausa
        func_ou_pausa = None

    def decorator(f) :
        @wraps(f)
        def wrapper(*args, **kwargs) :
            resultado = f(*args, **kwargs)
            if real_pausa > 0 :
                time.sleep(real_pausa)
            return resultado

        return wrapper

    if func_ou_pausa is None :
        return decorator
    return decorator(func_ou_pausa)
