from pathlib import Path
import os



# DIRETÓRIO_BASE_PADRÃO = Path(user_documents_dir(), 'SIGE')
#todo: Retornar o diretório base para a pasta de documentos, que é mais global. Para isso, preciso resolver a questão
# do armazenamento de parâmetros da sessão. Coloquei no OneDrive para facilitar os testes com as planilhas de frequência.
DIRETÓRIO_BASE_PADRÃO = Path(os.getenv('OneDriveCommercial'), 'SIGE')
DIRETÓRIO_SECRETARIA = Path(os.getenv('OneDriveCommercial'), 'Secretaria')

