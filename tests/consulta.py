import os
from app.config.parâmetros import parâmetros
from app.core import Consulta, Exportação






diretório_base = parâmetros.diretório_base
fonte = str(os.path.join(diretório_base, 'fonte'))

consulta = Consulta(diretório_fonte=fonte)
Exportação(consulta=consulta, path_destino=diretório_base)
