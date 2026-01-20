import re
from pathlib import Path
from platformdirs import user_documents_dir
import json
import os



# DIRETÓRIO_BASE_PADRÃO = Path(user_documents_dir(), 'SIGE')
#todo: Retornar o diretório base para a pasta de documentos, que é mais global. Para isso, preciso resolver a questão
# do armazenamento de parâmetros da sessão. Coloquei no OneDrive para facilitar os testes com as planilhas de frequência.
DIRETÓRIO_BASE_PADRÃO = Path(os.getenv('OneDriveCommercial'), 'SIGE')
DIRETÓRIO_SECRETARIA = Path(os.getenv('OneDriveCommercial'), 'Secretaria')

def obter_string_numérica(número: str) -> str :
    if not número :
        return '-'
    return re.sub(r'\D', '', str(número))
