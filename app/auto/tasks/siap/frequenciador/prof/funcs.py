from dataclasses import dataclass
from functools import wraps
import sys
import time
from functools import wraps
from typing import Callable, Any

from selenium.webdriver.remote.webelement import WebElement

from app.auto.tasks.siap.frequenciador.prof.constantes import SELETOR_TABELA_UPDATE, BIMESTRE
from app.config.parâmetros.getters.tempo import tempo


def voltar(self) :
    self.master.back()
    time.sleep(3)


def deu_error(erro: str | None) -> bool :
    if not erro :
        return False
    if 'Server Error' in erro :
        return True
    return False


def primeira_tentativa(tentativas: int) -> bool :
    if tentativas == 0 :
        return True
    return False


def está_fora_do_range(índice: int, escopo: list[WebElement]) -> bool :
    if índice >= len(escopo) :
        return True
    return False


def cantar_exception(_tentativas: int, etapa: str, exception, índice: int = 0) -> int :
    exceção = getattr(exception, '__name__', exception.__class__.__name__)
    print(f"Exception '{exceção}' no processamento de {etapa}: {exception}\n "
          f"  ## Tentativa {_tentativas + 1} falhou em {índice}.")
    for i in range(2, -1, -1) :
        sys.stdout.write(f'\r     Tentando novamente em {i} segundos...')
        sys.stdout.flush()
        time.sleep(1)

    sys.stdout.write('\r' + ' ' * 50 + '\r')
    sys.stdout.flush()
    print('     ✓ Foi realizada uma nova tentativa.\n')
    return _tentativas + 1


def obter_data_da_lista(lista_pacote: list[WebElement]) :
    data_pacote = lista_pacote[0].get_attribute('data-data')
    print(f'{data_pacote = }')
    return data_pacote


def preencher_filtro_de_linhas(self) :
    self.nv.digitar_xpath('diário', 'ano', string=tempo.ano_atual)
    self.nv.clicar('xpath livre', '//*[@id="FormularioPrincipal"]/div[4]/div[2]/div/div[1]/div')  # clicar fora
    self.nv.selecionar_dropdown('xpath', 'diário', 'bimestre', valor=BIMESTRE)
    self.nv.clicar('xpath', 'diário', 'botão listar', elemento_espera=SELETOR_TABELA_UPDATE)


def acessar_painel_frequência(self) :
    self.nv.clicar('xpath', 'menu sistema')
    self.nv.clicar('xpath', 'diário', '_xpath')


def obter_lista_matrículas_ausentes(self, data) :
    _df = self._ausentes_na_data.copy()
    df_ausentes_na_data = _df[_df['Data'] == data]
    lista_matrículas_ausentes = df_ausentes_na_data['Matrícula'].tolist()
    return lista_matrículas_ausentes


def debugar(func=None, *, pausa: int | float = 0) :
    def decorator(f) :
        @wraps(f)
        def wrapper(*args, **kwargs) :
            nome_func = f.__name__
            print(f'   ↑↑↑↑↑↑ Iniciando função: `{nome_func}`')

            resultado = f(*args, **kwargs)

            if pausa > 0 :
                print(f'Pausando a execução após {nome_func} por {pausa}s')
                time.sleep(pausa)

            print(f'   ↓↓↓↓↓↓ Saindo da função `{nome_func}`')
            return resultado

        return wrapper

    # O "segredo" está aqui:
    if func is None :
        # Caso @debugar(pausa=20) -> retorna o decorator para ser aplicado depois
        return decorator
    else :
        # Caso @debugar -> aplica o decorator imediatamente na func
        return decorator(func)