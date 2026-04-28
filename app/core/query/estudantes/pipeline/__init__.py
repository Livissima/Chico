import pandas as pd

from .consultaestudantes import ConsultaEstudantes
from .formatação import Formatação
from .integraçãodeextras import IntegraçãoDeExtras
#

import warnings
from openpyxl import __name__ as openpyxl_name

pd.set_option('display.max_columns', None)
pd.set_option('display.expand_frame_repr', False)  # Evita quebra do DataFrame em múltiplas linhas
pd.set_option('display.width', None)  # Ajusta automaticamente à largura do terminal
warnings.filterwarnings('ignore', category=UserWarning, module=openpyxl_name)
