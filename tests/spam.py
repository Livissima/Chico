from app.auto import Bot
from app.config.parâmetros import parâmetros

lista: list[str] = [
    # "01/10/2025",
    # "02/10/2025",
    # "03/10/2025",
    # "07/10/2025",
    # "08/10/2025",
    # "09/10/2025",
    "10/10/2025",
    "13/10/2025",
    "14/10/2025",
    "16/10/2025",
    "17/10/2025",
    "20/10/2025",
    "21/10/2025",
    # "22/10/2025"
]
Bot(tarefa='siap', path=parâmetros.diretório_base, periodo=lista)
"""
//*[@id="cphFuncionalidade_ControleFrequencia"]/div/div[4]/div[3]/div/div[2]/div[1]
//*[@id="cphFuncionalidade_ControleFrequencia"]/div/div[4]/div[3]/div/div[2]/div[2]
//*[@id="cphFuncionalidade_ControleFrequencia"]/div/div[4]/div[3]/div/div[2]/div[38]

"""