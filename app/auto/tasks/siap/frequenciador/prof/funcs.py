#app/auto/tasks/siap/frequenciador/prof/funcs.py
import sys
import time
from functools import wraps
from typing import Any

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from app.auto.tasks.siap.frequenciador.prof.constantes import SELETOR_TABELA_UPDATE, BIMESTRE
from app.config.parâmetros.getters.tempo import tempo

def Print(ação: str, valor: Any, valor2: Any = None) -> None :
    # Definição de Estilos (ANSI)
    ESTILOS = {
        bool : "\033[3;35m",  # Roxo Itálico
        int : "\033[0;34m",  # Azul Negrito
        float : "\033[1;34m",  # Azul Negrito
        str : "\033[0;32m",  # Verde
        None : "\033[2;37m",  # Cinza Faint
        "AÇÃO" : "\033[0m",  # Branco Negrito
        "RESET" : "\033[0m",
        list : "\033[0;36m",  # Ciano para listas
        dict : "\033[0;33m",  # Amarelo para dicionários
        TypeError : '\033[0:47m'  #fundo cinza para exception
    }

    def formatar(v) :
        cor = ESTILOS.get(type(v), "")
        return f"{cor}{v}{ESTILOS['RESET']}"

    # Montagem da mensagem
    prefixo = f"{ESTILOS['AÇÃO']}{ação}:{ESTILOS['RESET']}"

    if valor2 is not None :
        mensagem = f"{prefixo} {formatar(valor)} – {formatar(valor2)}"
    else :
        mensagem = f"{prefixo} {formatar(valor)}"

    # Usamos o sys.stdout.write para garantir que os códigos cheguem "crus"
    sys.stdout.write(mensagem + "\n")
    sys.stdout.flush()


def debugar(func_ou_pausa=None, *, pausa: int | float = 0) :
    real_pausa = pausa
    if isinstance(func_ou_pausa, (int, float)) :
        real_pausa = func_ou_pausa
        func_ou_pausa = None

    def decorator(f) :
        @wraps(f)
        def wrapper(*args, **kwargs) :
            nome_func = f.__name__
            # print(f'   ↑↑↑↑↑↑ Iniciando função: `{nome_func}`')

            resultado = f(*args, **kwargs)

            if real_pausa > 0 :
                print(f'Pausando a execução após {nome_func} por {real_pausa}s')
                # time.sleep(real_pausa)

            # print(f'   ↓↓↓↓↓↓ Finalizando função `{nome_func}`')
            return resultado

        return wrapper

    if func_ou_pausa is None :
        return decorator
    return decorator(func_ou_pausa)

def printar_sobreescrevendo(string1, string2) -> None :
    sys.stdout.write(string1)
    sys.stdout.flush()
    sys.stdout.write(string2)
    sys.stdout.flush()


def voltar(self) -> None :
    print(f'    ... Voltando.')
    self.master.back()
    time.sleep(3)

def deu_error(erro: str | None) -> bool :
    if not erro :
        Print('deu_error', False)
        return False
    if 'Server Error' in erro :
        Print('deu_error', True)
        return True
    Print('deu_error', False)
    return False

def primeira_tentativa(tentativas: int) -> bool :
    if tentativas == 0 :
        Print('primeira_tentativa', True)
        return True
    Print('primeira_tentativa', False)
    return False


def está_fora_do_range(índice: int, escopo: list[WebElement]) -> bool :
    if índice >= len(escopo) :
        Print('está_fora_do_range', True)
        return True
    Print('está_fora_do_range', False)
    return False

@debugar
def cantar_exception(_tentativas: int, etapa: str, exception, índice: int = 0) -> int :
    exceção = getattr(exception, '__name__', exception.__class__.__name__)
    Print(f"\nException '{exceção}' na etapa `{etapa}`", {exception})
    Print(f"  ## Tentativa {_tentativas + 1} falhou em:", {índice})
    for i in range(2, -1, -1) :
        sys.stdout.write(f'\r     Tentando novamente em {i} segundos...')
        sys.stdout.flush()
        time.sleep(1)

    sys.stdout.write('\r' + ' ' * 50 + '\r')
    sys.stdout.flush()
    print('     ✓ Foi realizada uma nova tentativa.\n')
    return _tentativas + 1

@debugar
def obter_data_da_lista(lista_pacote: list[WebElement]) -> str:
    data_pacote = lista_pacote[0].get_attribute('data-data')
    Print(f'Data dos pacotes de pontinhos', data_pacote)
    return str(data_pacote)

@debugar
def preencher_filtro_de_pesquisa(self) -> None :
    sys.stdout.write(' - Preenchendo filtro de pesquisa')
    sys.stdout.flush()

    self.nv.digitar_xpath('diário', 'ano', string=tempo.ano_atual)
    self.nv.clicar('xpath livre', '//*[@id="FormularioPrincipal"]/div[4]/div[2]/div/div[1]/div')  # clicar fora
    self.nv.selecionar_dropdown('xpath', 'diário', 'bimestre', valor=BIMESTRE)
    self.nv.clicar('xpath', 'diário', 'botão listar', elemento_espera=SELETOR_TABELA_UPDATE)

    sys.stdout.write('\r' + ' - Pesquisando disciplinas...')
    sys.stdout.flush()
    print('')

@debugar
def acessar_painel_frequência(self) -> None:
    self.nv.clicar('xpath', 'menu sistema')
    self.nv.clicar('xpath', 'diário', '_xpath')

@debugar
def obter_lista_matrículas_ausentes(self, data: str) -> list[str] :
    _df = self._ausentes_na_data.copy()
    df_ausentes_na_data = _df[_df['Data'] == data]
    lista_matrículas_ausentes = df_ausentes_na_data['Matrícula'].tolist()
    Print(f'Matrículas ausentes', len(lista_matrículas_ausentes), lista_matrículas_ausentes)
    return lista_matrículas_ausentes

@debugar
def obter_colunas_pontinhos(lista_pacotes_pontinhos) -> list[WebElement]:
    return [pacote.find_element(By.CLASS_NAME, 'itens') for pacote in lista_pacotes_pontinhos]

def selecionar_mês(self, mês: str) -> None:
    Print(f'Selecionando mês', mês)
    self.nv.selecionar_dropdown('xpath', 'diário', 'mês', texto=mês)
    self.nv.aguardar_página(1)

