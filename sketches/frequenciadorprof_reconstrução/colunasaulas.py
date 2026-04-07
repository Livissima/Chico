import time

from selenium.common import StaleElementReferenceException
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

from app.auto import NavegaçãoWeb
from app.config.parâmetros.getters.tempo import tempo


class ColunasAulas:
    def __init__(self, master: Chrome, navegação):
        self._master = master
        self._nv = navegação

        self.elemento = self.elementar()

    def elementar(self):
        elemento_maior = self._master.find_element(By.ID, 'cphFuncionalidade_cphCampos_ControleFrequenciaAluno')

        sub_elemento = elemento_maior.find_element(By.CLASS_NAME, 'index-1')
        elemento_empacotador = sub_elemento.find_element(By.CLASS_NAME, 'listaTableWrap')

        lista_pacotes_pontinhos = elemento_empacotador.find_elements(By.CLASS_NAME, 'listaDeFrequencias')
        data_pacote = lista_pacotes_pontinhos[0].get_attribute('data-data')
        print(f'{data_pacote = }')

        lista_coluna_pontinhos = [pacote.find_element(By.CLASS_NAME, 'itens') for pacote in lista_pacotes_pontinhos]

        return {
            'lista colunas' : lista_coluna_pontinhos,
            'data' : data_pacote
        }



    # def _obter_calendários_e_dias(self, índice_linha) :
    #     tentativas = 0
    #     while tentativas < 4 :
    #
    #         try :
    #             seletor_calendário = (By.ID, 'cphFuncionalidade_cphCampos_CalendarioMensal')
    #             div_calendário = self._nv.obter_elemento(*seletor_calendário)
    #             tabela_calendário = div_calendário.find_element(By.TAG_NAME, 'table')
    #             corpo_tabela = tabela_calendário.find_element(By.TAG_NAME, 'tbody')
    #             dias = corpo_tabela.find_elements(By.TAG_NAME, 'td')
    #             dias_relevantes = [dia for dia in dias if dia.get_attribute('data-executado')]
    #             dias_ok = [dia for dia in dias_relevantes if dia.get_attribute('data-executado') == 'True']
    #             dias_pendentes = [dia for dia in dias_relevantes if dia.get_attribute('data-executado') == 'False']
    #
    #             return dias_relevantes
    #
    #         except Exception as e :
    #
    #             print(f'Erro na obtenção de calendário. Tentando novamente... {e}')
    #             tentativas += 1
    #
    #             if tentativas >= 4 :
    #                 raise Exception('Não deu para obter o calendário.') from e
    #
    #             linhas = self._obter_linhas_disciplinas()
    #             # return linhas
    #             self._processar_linha_disciplina(índice_linha, linhas)
    #
    #     return None
    #
    # def _processar_linha_disciplina(self, índice_linha, linhas) :
    #     linhas_resultado = None
    #     tentativas = 0
    #     while tentativas < 3 :
    #         try :
    #             if tentativas > 0 :
    #                 linhas_resultado = self._obter_linhas_disciplinas()
    #
    #             if tentativas == 0:
    #                 linhas_resultado = linhas
    #
    #             if índice_linha >= len(linhas_resultado) :
    #                 print(f"Índice {índice_linha} fora do range")
    #                 return
    #
    #             linha_atual = linhas_resultado[índice_linha]
    #             linha_atual.click()
    #             time.sleep(1)
    #
    #             self._nv.clicar('xpath', 'diário', 'frequência')
    #             print(f'\n → → → em frequência na linha {índice_linha + 1}')
    #
    #             self._processar_dias_linha(índice_linha)
    #             break
    #
    #         except StaleElementReferenceException :
    #             tentativas += 1
    #             print(f"Tentativa {tentativas} falhou para linha {índice_linha}")
    #             time.sleep(2)
    #
    # def _processar_dias_linha(self, índice_linha) :
    #     self._nv.selecionar_dropdown('diário', 'mês', texto='Setembro')
    #     self._nv.aguardar_página(1)
    #
    #     dias_pendentes = self._obter_calendários_e_dias(índice_linha)
    #
    #     print(f'Dias pendentes: {[dia.text for dia in dias_pendentes]}')
    #
    #     if not dias_pendentes :
    #         print('Nenhum dia pendente encontrado')
    #         return
    #
    #     for índice_dia in range(len(dias_pendentes)) :
    #         self._processar_dia_individual(índice_linha, índice_dia)
    #
    # def _processar_dia_individual(self, índice_linha, índice_dia) :
    #
    #     tentativas = 0
    #     while tentativas < 3 :
    #         try :
    #             dias_pendentes_atualizados = self._obter_calendários_e_dias(índice_linha)
    #
    #             if índice_dia >= len(dias_pendentes_atualizados) :
    #                 print(f"Índice de dia {índice_dia} fora do range")
    #                 return
    #
    #             dia_atual = dias_pendentes_atualizados[índice_dia]
    #             print(f'Clicando no dia: {dia_atual.text}')
    #
    #             self._master.execute_script("arguments[0].click();", dia_atual)
    #             self._nv.aguardar_página()
    #
    #
    #             erro = ''
    #             body = self._master.find_element(By.TAG_NAME, 'body')
    #             try:
    #                 erro = body.find_element(By.TAG_NAME, 'h1').text
    #             except:
    #                 pass
    #
    #             finally:
    #
    #                 print(f'{erro = }')
    #
    #             if 'Server Error' in erro:
    #                 self._master.back()
    #                 time.sleep(3)
    #                 tentativas += 1
    #                 continue
    #
    #
    #             elemento_maior = self._master.find_element(By.ID, 'cphFuncionalidade_cphCampos_ControleFrequenciaAluno')
    #
    #             sub_elemento = elemento_maior.find_element(By.CLASS_NAME, 'index-1')
    #             elemento_empacotador = sub_elemento.find_element(By.CLASS_NAME, 'listaTableWrap')
    #
    #             lista_pacotes_pontinhos = elemento_empacotador.find_elements(By.CLASS_NAME, 'listaDeFrequencias')
    #             data_pacote = lista_pacotes_pontinhos[0].get_attribute('data-data')
    #             print(f'{data_pacote = }')
    #
    #             lista_coluna_pontinhos = [pacote.find_element(By.CLASS_NAME, 'itens') for pacote in
    #                                       lista_pacotes_pontinhos]
    #
    #
    #             _df = self._ausentes_na_data.copy()
    #             df_ausentes_na_data = _df[_df['Data Falta'] == data_pacote]
    #             lista_matrículas_ausentes = df_ausentes_na_data['Matrícula'].tolist()
    #
    #
    #             self._iterar_coluna_de_aula_do_dia(lista_coluna_pontinhos, lista_matrículas_ausentes)
    #
    #             self._nv.clicar('xpath', 'diário', 'salvar')
    #             self._nv.aguardar_página(1)
    #             break
    #
    #         except StaleElementReferenceException :
    #             tentativas += 1
    #             print(f"Tentativa {tentativas} falhou para dia {índice_dia}")
    #             time.sleep(2)