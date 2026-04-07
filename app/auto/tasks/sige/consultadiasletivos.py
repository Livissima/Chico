import json
import os.path
from datetime import datetime
from os import PathLike
from pathlib import Path

from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By

from app.auto.tasks.taskregistry import TaskRegistry
from app.auto.functions import NavegaçãoWeb
from app.config.parâmetros import parâmetros

@TaskRegistry.registrar('consultar dias letivos')
class ConsultaDiasLetivos:
    def __init__(
            self,
            navegador: Chrome,
            ano: int,
            path: PathLike,
            **kwargs
    ):
        self.master = navegador
        self._ano = ano
        self._path = Path(path, 'fonte', f'Dias letivos {ano}.json')
        self._nv = NavegaçãoWeb(navegador, 'siap')

        self._executar(self._path, ano)

    def _executar(self, path: Path, ano: int):
        self._logon(ano)

        dias_letivos = self._obter_dias_letivos()

        self._exportar_json(path, dias_letivos)

        self.master.quit()


    def _obter_dias_letivos(self) :
        elementos_dias = self.master.find_elements(By.CLASS_NAME, 'letivo')

        dias = [dia.get_attribute('data-canonica') for dia in elementos_dias
                if dia.get_attribute('original-title') not in self._descritores_para_desprezar]

        dias = [datetime.strptime(dia, '%Y/%m/%d').strftime('%d/%m/%Y') for dia in dias]

        print(f'{dias = }')
        print(f'{len(dias) = }')

        return dias

    @staticmethod
    def _url_calendário(ano: int):
        ano_atual = datetime.now().year
        if ano not in list(range(2013, ano_atual+1)):
            raise Exception(f'O ano selecionado para consulta de dias letivos é inválido: {ano}')
        return f'https://siap.educacao.go.gov.br/imprimircalendario.aspx?anoLetivo={str(ano)}'


    @staticmethod
    def _exportar_json(path: Path, lista_dias):
        parâmetros.lista_dias_letivos = lista_dias
        with open(path, 'x', encoding='utf-8') as arquivo:
            json.dump(lista_dias, arquivo, ensure_ascii=False, indent=2)


    @property
    def _descritores_para_desprezar(self) -> list[str]:
        return [
            'Trabalho Coletivo', 'Conselho de Classe/Encerramento do Bimestre', 'Término das aulas/Conselho de classe'
        ]

    def _logon(self, ano):
        self.master.get(self._url_calendário(ano))
        self._nv.aguardar_página()
