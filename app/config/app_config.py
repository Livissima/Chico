import os
from pathlib import Path
from platformdirs import user_documents_dir



DIRETÓRIO_BASE_PADRÃO = Path(str(os.path.join(Path(user_documents_dir()), 'SIGE')))
