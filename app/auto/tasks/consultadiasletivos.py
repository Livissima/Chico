import json
import os.path
from datetime import datetime
from os import PathLike
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By

from ..functions import NavegaçãoWeb
from ...config.parâmetros import parâmetros


class ConsultaDiasLetivos:
    def __init__(
            self,
            navegador: Chrome,
            ano: int,
            path: PathLike,
            **kwargs
    ):
        self.master = navegador
        self.ano = ano
        self.path = os.path.join(path, 'fonte', f'Dias letivos {self.ano}.json')
        self.nv = NavegaçãoWeb(navegador, 'siap')

        self._executar()

    def _executar(self):
        self.master.get(self._url_calendário(self.ano))
        self.nv.aguardar_página()
        dias_letivos = self._obter_dias_letivos()
        self._exportar_json(dias_letivos)
        self.master.quit()

    def _obter_dias_letivos(self) :
        elementos_dias = self.master.find_elements(By.CLASS_NAME, 'letivo')
        dias_letivos_sem_aula = [
            'Trabalho Coletivo', 'Conselho de Classe/Encerramento do Bimestre', 'Término das aulas/Conselho de classe'
        ]
        dias = [dia.get_attribute('data-canonica') for dia in elementos_dias
                if dia.get_attribute('original-title') not in dias_letivos_sem_aula]

        dias = [datetime.strptime(dia, '%Y/%m/%d').strftime('%d/%m/%Y') for dia in dias]

        print(f'{dias = }')
        print(f'{len(dias) = }')

        return dias

    @staticmethod
    def _url_calendário(ano: int):
        ano_atual = datetime.now().year
        if ano in list(range(2013, ano_atual+1)):
            return f'https://siap.educacao.go.gov.br/imprimircalendario.aspx?anoLetivo={str(ano)}'
        else:
            raise Exception(f'O ano selecionado para consulta de dias letivos é inválido: {ano}')

    def _exportar_json(self, lista_dias):
        parâmetros.lista_dias_letivos = lista_dias
        with open(self.path, 'w', encoding='utf-8') as arquivo:
            json.dump(lista_dias, arquivo, ensure_ascii=False, indent=2)



