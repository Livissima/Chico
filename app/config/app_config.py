import os
import re
from pathlib import Path
from platformdirs import user_documents_dir



DIRETÓRIO_BASE_PADRÃO = Path(str(os.path.join(Path(user_documents_dir()), 'SIGE')))


def obter_string_numérica(número) -> str :
    if not número :
        return '-'

    _str_numérica = re.sub(r'\D', '', str(número))

    return _str_numérica

