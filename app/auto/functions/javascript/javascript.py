# from app.auto.functions.javascript.scripts.ir_para_data import SCRIPT_IR_PARA_DATA
# from app.auto.functions.javascript.scripts.justificar import SCRIPT_JUSTIFICAR
# from app.auto.functions.javascript.scripts.marcar_falta_como_adm import SCRIPT_MARCAR_FALTA_COMO_ADM
# from app.auto.functions.javascript.scripts.obter_fichas import SCRIPT_OBTER_TABELAS_FICHAS
# from app.auto.functions.javascript.scripts.obter_tabelas import SCRIPT_OBTER_TABELAS_SIMPLES
# from app.auto.functions.javascript.scripts.script_selecionar import SCRIPT_SELECIONAR_DISPARANDO_EVENTO
from .scripts import *


class Javascript :
    justificar: str = SCRIPT_JUSTIFICAR
    ir_para_data: str = SCRIPT_IR_PARA_DATA
    lançar_falta_adm: str = SCRIPT_MARCAR_FALTA_COMO_ADM
    obter_fichas: str = SCRIPT_OBTER_TABELAS_FICHAS
    obter_tabelas: str = SCRIPT_OBTER_TABELAS_SIMPLES
    selecionar: str = SCRIPT_SELECIONAR_DISPARANDO_EVENTO
