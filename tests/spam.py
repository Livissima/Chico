from app.auto import Bot
from app.config.parâmetros import parâmetros

lista: list[str] = [
    # "01/10/2025",
    # "02/10/2025",
    # "03/10/2025",
    # "07/10/2025",
    # "08/10/2025",
    # "09/10/2025",
    # "10/10/2025",
    # "13/10/2025",
    "14/10/2025",
    "16/10/2025",
    "17/10/2025",
    "20/10/2025",
    "21/10/2025",
    "22/10/2025",
    "23/10/2025",
    "29/10/2025",
    "30/10/2025",
    "31/10/2025"
]
Bot(tarefa='siap', parâmetros_web=None, path=parâmetros.diretório_base, periodo=lista)
