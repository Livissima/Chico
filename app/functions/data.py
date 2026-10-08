import json
import warnings
from pathlib import Path
from typing import Any
from openpyxl import __name__ as openpyxl_name
import pandas as pd


def ler_json(caminho: Path) -> dict:
    try:
        with open(caminho, 'r', encoding='utf-8') as arquivo:
            return json.load(arquivo)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


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


def ajustar_print_pandas():
    pd.set_option('display.max_columns', None)
    pd.set_option('display.expand_frame_repr', False)  # Evita quebra do DataFrame em múltiplas linhas
    pd.set_option('display.width', None)  # Ajusta automaticamente à largura do terminal
    warnings.filterwarnings('ignore', category=UserWarning, module=openpyxl_name)
