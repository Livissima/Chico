import json
import os.path
from pathlib import Path
from typing import Any
from pandas import DataFrame
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

from app.auto.data.sites.propriedades import Propriedades
from app.auto.functions.impressão import Impressão
from app.auto.functions.navegação import Navegação
from app.ui.config.parâmetros import parâmetros


class Sondagem:

    def __init__(
            self,
            navegador: Chrome,
            destino: str,
    ):
        print(f'class Sondagem instanciada.')
        self.master = navegador
        self.destino_comum = destino

        self.nv = Navegação(navegador, 'sige')
        self.pp = Propriedades('sige')
        self._logon()
        self._resumo = self._resumir()
        self.exportar(self._resumo)
        self.master.quit()

        print(json.dumps(self._resumo, indent=4, ensure_ascii=False))

    def _logon(self):
        self.master.get(self.pp.url)
        self.master.maximize_window()
        self.nv.digitar_xpath('misc', 'input id', string=self.pp.credenciais['id'])
        self.nv.digitar_xpath('misc', 'input senha', string=self.pp.credenciais['senha'])
        self.nv.clicar('xpath', 'misc', 'entrar')
        self.nv.clicar('xpath', 'misc', 'alerta')

    def _gerar_elemento_tabela(self):

        self.nv.caminhar('turmas')
        self.nv.clicar('xpath', 'resumo', 'turmas', 'ativas')
        self.nv.digitar_xpath('resumo', 'turmas', 'input data', string=self.pp.hoje)
        self.nv.clicar('id', 'gerar')
        self.nv.aguardar()

        elemento_tabela = self.nv._master.find_element(By.CSS_SELECTOR, 'body > table.tabela')

        return elemento_tabela

    @staticmethod
    def _obter_tabela_do_elemento(elemento: WebElement) -> dict[str | Any, list[Any]]:

        cabeçalhos = ['Composição', 'Série', 'Turno', 'Código', 'Turma', 'Horário', 'Funcionamento', 'Sala',
                      'Tipo Turma', 'Tipo Atendimento', 'Local Diferenciado', 'Data Criação', 'Situação',
                      'Capacidade legal', 'Capacidade física', 'Efetivados', 'Não Efetivados', 'Vagas',
                      'Excedente Autorizado']

        tabela_turmas = {cabeçalho : [] for cabeçalho in cabeçalhos}

        todas_linhas = elemento.find_elements(By.TAG_NAME, 'tr')

        for linha in todas_linhas :
            celulas = linha.find_elements(By.TAG_NAME, 'td')

            if not celulas or linha.get_attribute('onclick') is None :
                continue

            linha_dados = []
            for celula in celulas :
                texto = celula.text.strip()
                texto = texto.replace('&nbsp;', '').replace('\u00a0', '').strip()
                if texto :
                    linha_dados.append(texto)

            if len(linha_dados) >= len(cabeçalhos) :
                for i, cabecalho in enumerate(cabeçalhos) :
                    if i < len(linha_dados) :
                        tabela_turmas[cabecalho].append(linha_dados[i])
                    else :
                        tabela_turmas[cabecalho].append(None)
            elif len(linha_dados) > 0 :
                print(f"Linha ignorada com {len(linha_dados)} colunas")

        print(f"Extraídas {len(tabela_turmas['Código'])} turmas")

        return tabela_turmas

    def _resumir(self) -> dict[str, int | str]:
        resumo = {}
        elemento = self._gerar_elemento_tabela()
        tabela_completa = self._obter_tabela_do_elemento(elemento)

        resumo["Turmas"]               = sorted(tabela_completa["Turma"])
        resumo["Composições"]          = list(set(tabela_completa["Composição"]))
        resumo["Turnos"]               = list(set(tabela_completa["Turno"]))
        resumo["Tipos"]                = list(set(tabela_completa["Tipo Turma"]))
        resumo["Excedente autorizado"] = sum([int(valor) for valor in tabela_completa["Excedente Autorizado"]])
        resumo["Capacidade física"]    = sum([int(valor) for valor in tabela_completa["Capacidade física"]])
        resumo["Capacidade legal"]     = sum([int(valor) for valor in tabela_completa["Capacidade legal"]])
        resumo["Capacidade Total"]     = resumo["Capacidade física"] + resumo["Excedente autorizado"]
        resumo["Efetivados"]           = sum([int(valor) for valor in tabela_completa["Efetivados"]])
        resumo["Vagas disponíveis"]    = sum([int(valor) for valor in tabela_completa["Vagas"]])
        resumo["Vagas absolutas"]      = resumo["Capacidade Total"] - resumo["Efetivados"]
        resumo["Balanço Físico"]       = f'{(resumo["Efetivados"] / resumo["Capacidade física"])*100:.1f} %'
        resumo["Balanço absoluto"]     = f'{(resumo["Efetivados"] / resumo["Capacidade Total"])*100:.1f} %'

        return resumo

    @staticmethod
    def exportar(resumo: dict):
        path = os.path.join(parâmetros.novo_diretório, 'fonte', 'resumo.json')
        with open(path, 'w', encoding='utf-8') as arquivo:
            json.dump(resumo, arquivo, ensure_ascii=False, indent=2)
        return arquivo
