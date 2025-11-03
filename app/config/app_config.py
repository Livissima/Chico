import re
from pathlib import Path
from platformdirs import user_documents_dir



DIRETÓRIO_BASE_PADRÃO = Path(user_documents_dir(), 'SIGE')


def obter_string_numérica(número) -> str :
    if not número :
        return '-'

    string_numérica = re.sub(r'\D', '', str(número))

    return string_numérica
