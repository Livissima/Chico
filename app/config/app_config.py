import os
from pathlib import Path
from platformdirs import user_documents_dir



DIRETÓRIO_BASE_PADRÃO = str(os.path.join(Path(user_documents_dir()), 'SIGE'))
