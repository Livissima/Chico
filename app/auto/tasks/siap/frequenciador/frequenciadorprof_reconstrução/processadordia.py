import time

from selenium.common import StaleElementReferenceException
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

from app.auto import PropriedadesWeb, NavegaçãoWeb
from app.auto.tasks.siap.frequenciador import ColunasAulas
from app.auto.tasks.siap.frequenciador import ProcessadorCalendário


class ProcessadorDia:
    def __init__(
            self,
            master: Chrome,
            navegação: NavegaçãoWeb,
            propriedades: PropriedadesWeb,
            índice_disciplina: int,
            elemento_disciplinas: list[WebElement]
    ):
        self._master = master
        self._pp = propriedades
        self._nv = navegação
        self.elemento = elemento_disciplinas

        self.processar(master, navegação, propriedades, índice_disciplina, elemento_disciplinas)

    def processar(self, master, nv, pp, _índice_disciplina, elemento):

        dias_pendentes = ProcessadorCalendário(master, nv, pp, _índice_disciplina, elemento).elemento

        print(f'Dias pendentes: {[dia.text for dia in dias_pendentes]}')

        if not dias_pendentes :
            print('Nenhum dia pendente encontrado')
            return

        for índice_dia in range(len(dias_pendentes)) :
            # ProcessadorDia(master, nv, pp, índice, elemento)
            self._processar_dia_individual(master, nv, pp, _índice_disciplina, elemento, índice_dia)

    def _processar_dia_individual(self, master, nv, pp, _índice_disciplina_, _elemento, índice_dia) :

        tentativas = 0
        while tentativas < 3 :
            try :
                dias_pendentes_atualizados = ProcessadorCalendário(master, nv, pp, _índice_disciplina_, _elemento).elemento
                # dias_pendentes_atualizados = self._obter_calendários_e_dias(_índice_disciplina_)

                if índice_dia >= len(dias_pendentes_atualizados) :
                    print(f"Índice de dia {índice_dia} fora do range")
                    return

                dia_atual = dias_pendentes_atualizados[índice_dia]
                print(f'Clicando no dia: {dia_atual.text}')

                self._master.execute_script("arguments[0].click();", dia_atual)
                self._nv.aguardar_página()


                erro = ''
                body = self._master.find_element(By.TAG_NAME, 'body')
                try:
                    erro = body.find_element(By.TAG_NAME, 'h1').text
                except:
                    pass

                finally:

                    print(f'{erro = }')

                if 'Server Error' in erro:
                    self._master.back()
                    time.sleep(3)
                    tentativas += 1
                    continue

                _elemento = ColunasAulas(self._master, self._nv).elemento
                lista_coluna_pontinhos = _elemento['lista colunas']



                _df = self._ausentes_na_data.copy()
                df_ausentes_na_data = _df[_df['Data Falta'] == _elemento['data']]
                lista_matrículas_ausentes = df_ausentes_na_data['Matrícula'].tolist()


                self._iterar_coluna_de_aula_do_dia(lista_coluna_pontinhos, lista_matrículas_ausentes)

                self._nv.clicar('xpath', 'diário', 'salvar')
                self._nv.aguardar_página(1)
                break

            except StaleElementReferenceException :
                tentativas += 1
                print(f"Tentativa {tentativas} falhou para dia {índice_dia}")
                time.sleep(2)