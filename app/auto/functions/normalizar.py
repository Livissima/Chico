import unicodedata

def remover_acentos(texto: str) -> str:
    if texto is None:
        return ''
    nfkd = unicodedata.normalize('NFKD', str(texto))
    só_ascii = ''.join(chave for chave in nfkd if not unicodedata.combining(chave))
    return só_ascii.lower().strip()

def normalizar_dicionário(dicionário: dict | None):
    if not dicionário:
        return {}
    return {remover_acentos(chave): valor for chave, valor in dicionário.items()}

