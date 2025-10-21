from .ir_para_data import SCRIPT_IR_PARA_DATA
from .justificar import SCRIPT_JUSTIFICAR
from .marcar_falta_como_adm import SCRIPT_MARCAR_FALTA_COMO_ADM
from .obter_fichas import SCRIPT_OBTER_TABELAS_FICHAS
from .obter_tabelas import SCRIPT_OBTER_TABELAS_SIMPLES
from .script_selecionar import SCRIPT_SELECIONAR_DISPARANDO_EVENTO


class JS:

    @property
    def ir_para_data(self) -> str:
        return SCRIPT_IR_PARA_DATA

    @property
    def justificar(self) -> str:
        return SCRIPT_JUSTIFICAR

    @property
    def lançar_falta(self) -> str:
        return SCRIPT_MARCAR_FALTA_COMO_ADM

    @property
    def obter_fichas(self) -> str:
        return SCRIPT_OBTER_TABELAS_FICHAS

    @property
    def obter_tabelas(self) -> str:
        return SCRIPT_OBTER_TABELAS_SIMPLES

    @property
    def selecionar(self) -> str:
        return SCRIPT_SELECIONAR_DISPARANDO_EVENTO

