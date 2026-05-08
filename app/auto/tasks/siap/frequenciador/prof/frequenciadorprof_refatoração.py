import time
from pandas import DataFrame
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver import Chrome

from app.auto.data.dataclasses.propriedadesweb import PropriedadesWeb
from app.auto.functions.navegaçãoweb import NavegaçãoWeb
from app.auto.tasks.siap.frequenciador.prof.constantes import *
from app.config.parâmetros.getters.tempo import tempo
from app.config.settings.functions import str_exception, Print, debugar


class FrequenciadorProf :
    def __init__(self, navegador: Chrome, ausentes_na_data: DataFrame, **kwargs) :
        self._ausentes_na_data = ausentes_na_data
        self.master = navegador
        self.nv = NavegaçãoWeb(navegador, 'siap')
        self.pp = PropriedadesWeb(site='siap')
        self._executar()

    @debugar
    def _executar(self) :
        """Méthodo principal que orquestra a automação."""
        # Em vez de pegar os elementos, pegamos apenas a QUANTIDADE de disciplinas.
        qtd_disciplinas = self._obter_quantidade_disciplinas()
        Print("Quantidade de disciplinas encontradas", qtd_disciplinas)

        for índice_linha in range(qtd_disciplinas) :
            # Passamos apenas o índice. O método se encarrega de achar a linha atual.
            sucesso = self._processar_disciplina(índice_linha)
            if not sucesso :
                Print("Falha grave ao tentar processar disciplina de índice", índice_linha)

    # ---------------------------------------------------------
    # MÉTODOS DE ORQUESTRAÇÃO
    # ---------------------------------------------------------
    @debugar
    def _processar_disciplina(self, índice_linha: int) -> bool :
        """Acessa uma disciplina específica baseada no seu índice e processa os dias."""
        Print('# Iniciando processamento da disciplina índice', índice_linha)

        tentativas = 0
        while tentativas < 3 :
            try :
                # 1. Sempre que formos acessar uma disciplina, começamos do painel principal
                self._acessar_painel_e_filtrar()

                # 2. Obtemos as linhas ATUALIZADAS e clicamos na desejada
                linhas = self._obter_linhas_disciplinas_elementos()
                if índice_linha >= len(linhas) :
                    Print('Índice fora do range', índice_linha)
                    return False

                linha_atual = linhas[índice_linha]
                linha_atual.click()
                time.sleep(1)

                # 3. Entramos na aba de frequência
                self.nv.clicar('xpath', 'diário', 'frequência')

                # 4. Processamos os dias letivos dessa disciplina
                self._processar_dias_letivos_da_disciplina()
                return True  # Sucesso!

            except Exception as e :
                tentativas += 1
                Print(f'Erro na disciplina {índice_linha}. Tentativa {tentativas} falhou', str_exception(e))
                time.sleep(2)

        return False

    @debugar
    def _processar_dias_letivos_da_disciplina(self) :
        """Encontra dias pendentes no mês atual e itera sobre eles."""
        # Seleciona o mês no dropdown
        self.nv.selecionar_dropdown('xpath', 'diário', 'mês', texto=MÊS)
        self.nv.aguardar_página(1)

        # Em vez de guardar WebElements que ficam obsoletos, guardamos apenas o NÚMERO (texto) dos dias
        textos_dias_pendentes = self._obter_textos_dos_dias_pendentes()

        if not textos_dias_pendentes :
            Print('Nenhum dia pendente encontrado para esta disciplina.', '')
            return

        Print('Dias pendentes encontrados', textos_dias_pendentes)

        # Iteramos sobre a informação (texto), procurando o elemento novo a cada iteração
        for dia_texto in textos_dias_pendentes :
            self._processar_dia_individual(dia_texto)

    @debugar
    def _processar_dia_individual(self, dia_texto: str) :
        """Clica no dia específico pelo seu texto, valida erros e lança a frequência."""
        tentativas = 0
        while tentativas < 3 :
            try :
                # Procura o dia atualizado na tela com base no texto (ex: '7')
                elemento_dia = self._encontrar_dia_por_texto(dia_texto)
                if not elemento_dia :
                    Print('Não foi possível localizar o dia', dia_texto)
                    return

                Print('Clicando no dia', dia_texto)
                self.master.execute_script("arguments[0].click();", elemento_dia)
                self.nv.aguardar_página(1)

                # Verifica se a página quebrou (Server Error)
                if self._verificar_erro_na_pagina() :
                    self.master.back()
                    time.sleep(2)
                    tentativas += 1
                    continue

                # Lógica de Frequência
                self._lancar_faltas()

                # Salvar
                self.nv.clicar('xpath', 'diário', 'salvar')
                self.nv.aguardar_página(1)
                Print('Frequência salva para o dia', dia_texto)
                break

            except StaleElementReferenceException :
                tentativas += 1
                Print('Elemento obsoleto ao processar dia', dia_texto)
                time.sleep(2)
            except Exception as e :
                tentativas += 1

                Print('Erro inesperado no dia', dia_texto, str_exception(e))
                time.sleep(2)

    # ---------------------------------------------------------
    # MÉTODOS DE AÇÃO NA PÁGINA (Lógica de Negócio)
    # ---------------------------------------------------------
    def _lancar_faltas(self) :
        """Mapeia os pontinhos, cruza com a lista de ausentes e clica."""
        lista_pacotes_pontinhos = self._obter_lista_pacotes_pontinhos()
        if not lista_pacotes_pontinhos : return

        # Extrai a data do pacote para buscar no DataFrame
        data_pacote = str(lista_pacotes_pontinhos[0].get_attribute('data-data'))
        Print('Data do pacote atual', data_pacote)

        # Filtra alunos ausentes no DataFrame para a data específica
        df_filtrado = self._ausentes_na_data[self._ausentes_na_data['Data'] == data_pacote]
        matriculas_ausentes = df_filtrado['Matrícula'].tolist()
        Print('Alunos ausentes na data', len(matriculas_ausentes))

        if not matriculas_ausentes :
            Print('Nenhum aluno ausente na data. Lançando presença geral.', '')
            return

        # Coleta todas as colunas de pontinhos e age
        lista_colunas = [pacote.find_element(By.CLASS_NAME, 'itens') for pacote in lista_pacotes_pontinhos]
        self._agir_nos_pontos(lista_colunas, matriculas_ausentes)

    def _agir_nos_pontos(self, lista_colunas_pontinhos: list, ausentes: list[str]) -> None :
        """Clica nos pontinhos se o aluno for um dos ausentes."""
        for coluna_pontinhos in lista_colunas_pontinhos :
            pontinhos = coluna_pontinhos.find_elements(By.CLASS_NAME, 'item')

            # Filtra os pontinhos cuja matrícula está na lista de ausentes
            pontinhos_alvos = [p for p in pontinhos if p.get_attribute('data-matricula') in ausentes]

            for ponto_alvo in pontinhos_alvos :
                matricula = ponto_alvo.get_attribute('data-matricula')
                # Clica apenas se a falta ainda não tiver sido lançada
                if ponto_alvo.get_attribute('data-ausente') == 'False' :
                    ponto_alvo.click()
                    time.sleep(0.5)
                    Print('Falta lançada para', matricula)
                else :
                    Print('Falta já constava para', matricula)

    # ---------------------------------------------------------
    # MÉTODOS DE EXTRAÇÃO E NAVEGAÇÃO BÁSICA
    # ---------------------------------------------------------
    def _acessar_painel_e_filtrar(self) :
        """Navega até o painel inicial de frequências e aplica os filtros."""
        self.nv.clicar('xpath', 'menu sistema')
        self.nv.clicar('xpath', 'diário', '_xpath')

        # Filtros
        self.nv.digitar_xpath('diário', 'ano', string=tempo.ano_atual)
        self.nv.clicar('xpath livre', '//*[@id="FormularioPrincipal"]/div[4]/div[2]/div/div[1]/div')
        self.nv.selecionar_dropdown('xpath', 'diário', 'bimestre', valor=BIMESTRE)
        self.nv.clicar('xpath', 'diário', 'botão listar', elemento_espera=SELETOR_TABELA_UPDATE)

    def _obter_linhas_disciplinas_elementos(self) :
        """Retorna os elementos Web (tr) das disciplinas na tabela de pesquisa."""
        tabela_linhas = self.master.find_element(*SELETOR_TABELA_UPDATE)
        tabela_calendario = tabela_linhas.find_element(*SELETOR_CORPO_TABELA)
        linhas_gerais = tabela_calendario.find_elements(*SELETOR_LINHAS_GERAIS)
        return [linha for linha in linhas_gerais if linha.get_attribute('class') != 'topo']

    def _obter_quantidade_disciplinas(self) -> int :
        """Acessa o painel, filtra e retorna apenas o número total de disciplinas."""
        self._acessar_painel_e_filtrar()
        linhas = self._obter_linhas_disciplinas_elementos()
        return len(linhas)

    def _obter_textos_dos_dias_pendentes(self) -> list[str] :
        """Varre o calendário e retorna uma lista com o texto (número) dos dias não executados."""
        textos = []
        try :
            div_calendario = self.nv.obter_elemento(*SELETOR_CALENDÁRIO_ITERÁVEIS)
            corpo_tabela = div_calendario.find_element(*SELETOR_TABELA).find_element(*SELETOR_CORPO_TABELA)
            dias = corpo_tabela.find_elements(*SELETOR_TD)

            # Filtra apenas os dias relevantes e pendentes que sejam <= dia de hoje
            for dia in dias :
                if dia.get_attribute('data-executado') == 'False' :
                    if dia.text.strip() and int(dia.text) <= int(tempo.hoje_dia) :
                        textos.append(dia.text)
        except Exception as e :
            Print('Aviso ao obter textos dos dias', str_exception(e))

        return textos

    def _encontrar_dia_por_texto(self, dia_texto: str) :
        """Busca no calendário o elemento cujo texto corresponda ao dia desejado."""
        try :
            div_calendario = self.nv.obter_elemento(*SELETOR_CALENDÁRIO_ITERÁVEIS)
            corpo_tabela = div_calendario.find_element(*SELETOR_TABELA).find_element(*SELETOR_CORPO_TABELA)
            dias = corpo_tabela.find_elements(*SELETOR_TD)
            for dia in dias :
                if dia.text.strip() == dia_texto and dia.get_attribute('data-executado') :
                    return dia
        except Exception :
            return None
        return None

    def _verificar_erro_na_pagina(self) -> bool :
        """Verifica se existe uma tag <h1> contendo 'Server Error' no body."""
        try :
            body = self.master.find_element(By.TAG_NAME, 'body')
            erro = body.find_element(By.TAG_NAME, 'h1').text
            if 'Server Error' in erro :
                Print('Erro 500 detectado no sistema SIGE', '')
                return True
        except Exception :
            print('Página não deu erro.')
            # Se não encontrou h1, é porque não deu o erro.
            pass
        return False

    def _obter_lista_pacotes_pontinhos(self) -> list :
        """Obtém os pacotes de pontinhos da frequência."""
        try :
            elemento_maior = self.master.find_element(By.ID, 'cphFuncionalidade_cphCampos_ControleFrequenciaAluno')
            sub_elemento = elemento_maior.find_element(By.CLASS_NAME, 'index-1')
            elemento_empacotador = sub_elemento.find_element(By.CLASS_NAME, 'listaTableWrap')
            return elemento_empacotador.find_elements(By.CLASS_NAME, 'listaDeFrequencias')
        except Exception as e :

            Print('Erro ao obter os pontinhos de frequência', str_exception(e))
            return []
