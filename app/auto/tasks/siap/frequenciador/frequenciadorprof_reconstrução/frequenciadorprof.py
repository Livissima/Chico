from pandas import DataFrame

from app.auto.data.sites.propriedadesweb import PropriedadesWeb
from app.auto.functions.navegaçãoweb import NavegaçãoWeb
from selenium.webdriver import Chrome

from app.auto.tasks.siap.frequenciador import LinhasDisciplinas
from app.auto.tasks.siap.frequenciador import ProcessadorDisciplina


class FrequenciadorProf :

    def __init__(self, navegador: Chrome, ausentes_na_data: DataFrame, **kwargs) :
        self._ausentes_na_data = ausentes_na_data

        self.master = navegador

        self.nv = NavegaçãoWeb(navegador, 'siap')
        self.pp = PropriedadesWeb(site='siap')
        self._executar()
        # self.master.quit()


    def _executar(self) :
        linhas_resultado = LinhasDisciplinas(self.master, self.nv).elemento
        print(f'Encontradas {len(linhas_resultado)} linhas')

        for índice_linha in range(len(linhas_resultado)) :
            # self._processar_linha_disciplina(índice_linha, linhas_resultado)
            ProcessadorDisciplina(self.master, self.pp, self.nv, índice_linha, linhas_resultado)

