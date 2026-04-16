#todo: módulo 99% funcional. É só organizar agora e corrigir o erro com os CEPMG e superar o hardcoding

from pathlib import Path
import pandas as pd
from selenium.webdriver import Chrome
from selenium.common.exceptions import NoAlertPresentException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from app.auto.data.sites import PropriedadesWeb
from app.auto.functions import NavegaçãoWeb
from app.config.settings.functions import ajustar_print_pandas, escrever_json
from app.auto.tasks.registrotasks import RegistroTasks
from app.config.parâmetros.getters.tempo import Tempo, tempo


ajustar_print_pandas()

path_xlsx = Path(  #hardcoded por enquanto
    r'C:\Users\meren\OneDrive - Secretaria de Estado da Educação\Secretaria', 'Sistema Presença 2026.xlsx')

nomes_planilhas = ['Fev-Mar', 'Abr-Mai', 'Jun-Jul', 'Ago-Set']

nome_planilha_atual = nomes_planilhas[0]

planilha_atual = pd.read_excel(path_xlsx, nome_planilha_atual)

planilha_atual['Matrícula'] = planilha_atual['Matrícula'].astype(float).astype(str)

alunos_incógnitos = planilha_atual[planilha_atual['Escola'] == 'Transferido']


@RegistroTasks.registrar('investigar')
class Investigação :
    def __init__(self, navegador: Chrome, **kwargs) :
        print(f'class Downloads instanciada.')
        self.master = navegador

        self._nv = NavegaçãoWeb(navegador, 'sige')
        self._pp = PropriedadesWeb('sige')

        self._executar()
        self.master.quit()

    def _executar(self) :
        self._logon()
        url_página = 'https://sige.educacao.go.gov.br/sige/modulos/AtualizaAluno/Ave_SolicitaAluno_cad.asp?optOrigemAluno=1'
        resultados_finais = {}

        for aluno in alunos_incógnitos.itertuples() :
            self._nv.acessar_destino(url_página)
            matrícula = aluno.Matrícula[0 :11]
            nome_estudante = aluno.Estudante
            resultado = self._investigar_indivíduo(matrícula, nome_estudante)
            resultados_finais.update(resultado)

        escrever_json(resultados_finais, r'C:\Users\meren\PycharmProjects\Chico\tests\transferidos.json')

    def _investigar_indivíduo(self, matrícula, nome_estudante) :
        print(f"Investigando '{nome_estudante}'.")

        self._nv.digitar_xpath('misc', 'data matrícula', string=tempo.hoje)
        self._nv.clicar('xpath livre', '/html/body/div[8]/form/table[2]/tbody/tr[4]/td[2]/table/tbody/tr/td[2]/input')
        self._nv.digitar_xpath('misc', 'matrícula', string=matrícula)

        botão_busca = self.master.find_element('xpath', '/html/body/div[8]/form/div/table/tbody/tr[3]/td/table/tbody/tr[1]/td[2]/a[2]/span')
        botão_busca.click()

        try:
            WebDriverWait(self.master, 3).until(EC.alert_is_present())

            alerta = self.master.switch_to.alert
            texto_alerta = self._filtrar_texto(alerta.text)

            alerta.accept()
            print('{'f"{nome_estudante} : {texto_alerta}"'}')
            return {nome_estudante : texto_alerta}

        except TimeoutException:
            print('{'f"{nome_estudante} : 'Não localizado'"'}')
            return {nome_estudante : 'Não localizado.'}



    def _logon(self) -> None :
        self.master.get(self._pp.urls)
        self.master.maximize_window()
        self._nv.digitar_xpath('misc', 'input id', string=self._pp.credenciais_padrão.id)
        self._nv.digitar_xpath('misc', 'input senha', string=self._pp.credenciais_padrão.senha)
        self._nv.clicar('xpath', 'misc', 'entrar')
        self._nv.clicar('xpath', 'misc', 'alerta')

    @staticmethod
    def _filtrar_texto(texto: str) -> str:
        if texto.startswith('O(A) aluno(a)  está com a situação '):

            texto_inteiro = texto.split('\n')
            segunda_linha = texto_inteiro[1]
            split_segunda_linha = segunda_linha.split(' - ')  #isso está excluindo os nomes dos CEPMG. Condicionar a linha com 2 traços
            escola = split_segunda_linha[1]
            return escola
        return texto

