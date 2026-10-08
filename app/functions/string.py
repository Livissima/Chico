import os
import re
import unicodedata


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


def truncar_diretório(_dir: str) -> str:
    _diretório = _dir.split('\\')
    _diretório = os.path.join(*_diretório[0 :3], '...', '...', *_diretório[-2 :])
    _diretório = _diretório.replace(':', ':\\')
    return _diretório


