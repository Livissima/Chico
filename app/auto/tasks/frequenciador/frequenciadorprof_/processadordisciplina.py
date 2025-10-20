import time

from selenium.common import StaleElementReferenceException
from selenium.webdriver import Chrome
from selenium.webdriver.remote.webelement import WebElement

from app.auto import Propriedades, NavegaçãoWeb
from app.auto.tasks.frequenciador.frequenciadorprof_ import ProcessadorDia


class ProcessadorDisciplina:
    def __init__(
            self,
            master: Chrome,
            propriedades: Propriedades,
            navegação: NavegaçãoWeb,
            índice_linha: int,
            lista_elementos_disciplinas: list[WebElement]
    ):
        self.master = master
        self.pp = propriedades
        self.nv = navegação
        self.elemento = lista_elementos_disciplinas

        self.processar(índice_linha, lista_elementos_disciplinas)

    def processar(self, índice_linha, elementos):
        linhas_resultado = None
        tentativas = 0
        while tentativas < 3 :
            try :
                if tentativas > 0 :
                    linhas_resultado = self.elemento

                if tentativas == 0 :
                    linhas_resultado = elementos

                if índice_linha >= len(linhas_resultado) :
                    print(f"Índice {índice_linha} fora do range")
                    return

                linha_atual = linhas_resultado[índice_linha]
                linha_atual.click()
                time.sleep(1)

                self.nv.clicar('xpath', 'diário', 'frequência')
                print(f'\n → → → em frequência na linha {índice_linha + 1}')

                # self._processar_dias_linha(índice_linha)
                ProcessadorDia(self.master, self.pp, self.nv, índice_linha, elementos)
                break

            except StaleElementReferenceException :
                tentativas += 1
                print(f"Tentativa {tentativas} falhou para linha {índice_linha}")
                time.sleep(2)