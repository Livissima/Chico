import re

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
