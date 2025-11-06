from app.auto import Bot
from app.config.parâmetros import parâmetros

lista: list[str] = [
    "03/11/2025",
    "04/11/2025",
    "06/11/2025"
]
Bot(tarefa='siap', parâmetros_web=None, path=parâmetros.diretório_base, periodo=lista)
