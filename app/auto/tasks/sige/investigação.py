import time
from pathlib import Path

import pandas as pd
from selenium.webdriver import Chrome

from app.auto.data.sites import PropriedadesWeb
from app.auto.functions import NavegaçãoWeb
from app.auto.functions.funções import ajustar_print_pandas
from app.auto.tasks.registrotasks import RegistroTasks
from app.config.parâmetros.estruturadeseleção import EstruturaDeSeleção

ajustar_print_pandas()



path_xlsx = Path(  #hardcoded por enquanto
    r'C:\Users\meren\OneDrive - Secretaria de Estado da Educação\Secretaria', 'Sistema Presença 2026.xlsx')

nomes_planilhas = ['Fev-Mar', 'Abr-Mai', 'Jun-Jul', 'Ago-Set']

nome_planilha_atual = nomes_planilhas[0]

planilha_atual = pd.read_excel(path_xlsx, nome_planilha_atual)

planilha_atual['Matrícula'] = planilha_atual['Matrícula'].astype(float).astype(str)

alunos_incógnitos = planilha_atual[planilha_atual['Escola'].isin(['Transferido', 'Aprovado'])]

print(alunos_incógnitos)

@RegistroTasks.registrar('investigar')
class Investigação:
    def __init__(
            self,
            navegador: Chrome,
            **kwargs
    ):
        print(f'class Downloads instanciada.')
        self.master = navegador


        self._nv = NavegaçãoWeb(navegador, 'sige')
        self._pp = PropriedadesWeb('sige')

        self._executar()


    def _executar(self):
        # self._logon()
        # self._nv.acessar_destino('ficha aluno')
        for aluno in alunos_incógnitos.iterrows():
            matrícula = str(aluno[1][0][0:11])
            # print(matrícula)

            self._nv.digitar_xpath('ficha aluno', 'matrícula', string=matrícula)

            # time.sleep(10)




        self.master.quit()


    def _logon(self) -> None:
        self.master.get(self._pp.urls)
        self.master.maximize_window()
        self._nv.digitar_xpath('misc', 'input id', string=self._pp.credenciais_padrão.id)
        self._nv.digitar_xpath('misc', 'input senha', string=self._pp.credenciais_padrão.senha)
        self._nv.clicar('xpath', 'misc', 'entrar')
        self._nv.clicar('xpath', 'misc', 'alerta')

