import json
import os.path
from typing import Any
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

from app.auto.data.sites.propriedades import Propriedades
from app.auto.functions.navegação import Navegação
from app.config.parâmetros import parâmetros


class Sondagem:

    def __init__(
            self,
            navegador: Chrome,
            destino: str,
            **kwargs
    ):
        print(f'class Sondagem instanciada.')
        self.master = navegador
        self.destino_comum = destino

        self.nv = Navegação(navegador, 'sige')
        self.pp = Propriedades('sige')
        self._logon()
        self._resumo = self._resumir
        self.exportar(self._resumo)
        parâmetros.resumo = self._resumo
        parâmetros.nome_ue = self._resumo['Nome UE']
        self.master.quit()


        print(json.dumps(self._resumo, indent=4, ensure_ascii=False))

    def _logon(self):
        self.master.get(self.pp.url)
        self.master.maximize_window()
        self.nv.digitar_xpath('misc', 'input id', string=self.pp.credenciais['id'])
        self.nv.digitar_xpath('misc', 'input senha', string=self.pp.credenciais['senha'])
        self.nv.clicar('xpath', 'misc', 'entrar')
        self.nv.clicar('xpath', 'misc', 'alerta')
        # self.nome_ue = self.obter_nome_ue()

        # parâmetros.nome_ue = self.master.find_element(By.CSS_SELECTOR, '#topo > div.topo-logo > div > h3:nth-child(2)').text.split(" - ")[0]

    def _gerar_elemento_tabela(self):

        self.nv.caminhar('turmas')
        self.nv.clicar('xpath', 'resumo', 'turmas', 'ativas')
        self.nv.digitar_xpath('resumo', 'turmas', 'input data', string=self.pp.hoje)
        self.nv.clicar('id', 'gerar')
        self.nv.aguardar_página()

        elemento_tabela = self.nv.master.find_element(By.CSS_SELECTOR, 'body > table.tabela')

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

    @property
    def _resumir(self) -> dict[str, int | str]:
        resumo = {}
        elemento = self._gerar_elemento_tabela()
        tabela_completa = self._obter_tabela_do_elemento(elemento)

        def obter_o_que_der(operacao, default='Erro'):
            try:
                resultado = operacao()

                if isinstance(resultado, list) and len(resultado) == 0:
                    return default

                return resultado
            except (KeyError, ValueError, TypeError, ZeroDivisionError):
                return default


        chaves  = list(obter_o_que_der(lambda: tabela_completa["Turma"]))
        valores = list(obter_o_que_der(lambda: tabela_completa["Código"]))
        turmas = dict(zip(chaves, valores))


        resumo["Nome UE"] = obter_o_que_der(lambda: self.obter_nome_ue())
        resumo["Códigos Turmas"] = obter_o_que_der(lambda: list(turmas.values()))
        resumo["Composições"] = obter_o_que_der(lambda: ', '.join(list(set(tabela_completa["Composição"]))))
        resumo["Turnos"] = obter_o_que_der(lambda: list(set(tabela_completa["Turno"])))
        resumo["Tipos"] = obter_o_que_der(lambda: list(set(tabela_completa["Tipo Turma"])))
        resumo["Excedente autorizado"] = obter_o_que_der(lambda: sum([int(valor) for valor in tabela_completa["Excedente Autorizado"]]))
        resumo["Excedente ocupado"] = obter_o_que_der(lambda: sum([valor for valor in map(int, tabela_completa["Vagas"]) if valor < 0]) * -1)
        resumo["Capacidade física"] = obter_o_que_der(lambda: sum([int(valor) for valor in tabela_completa["Capacidade física"]]))
        resumo["Capacidade legal"] = obter_o_que_der(lambda: sum([int(valor) for valor in tabela_completa["Capacidade legal"]]))

        resumo["Capacidade Total"] = obter_o_que_der(lambda: resumo["Capacidade física"] + resumo["Excedente autorizado"])
        resumo["Efetivados"] = obter_o_que_der(lambda: sum([int(valor) for valor in tabela_completa["Efetivados"]]))
        resumo["Vagas disponíveis"] = obter_o_que_der(lambda: resumo["Capacidade legal"] - resumo["Efetivados"])
        resumo["Vagas absolutas"] = obter_o_que_der(lambda: resumo["Capacidade Total"] - resumo["Efetivados"])

        resumo["Balanço Físico"] = obter_o_que_der(lambda: f'{(resumo["Efetivados"] / resumo["Capacidade física"]) * 100:.1f} %' if resumo["Capacidade física"] != 0 else "0.0 %")
        resumo["Balanço absoluto"] = obter_o_que_der(lambda: f'{(resumo["Efetivados"] / resumo["Capacidade Total"]) * 100:.1f} %' if resumo["Capacidade Total"] != 0 else "0.0 %")

        resumo["Turmas Ativas"] = obter_o_que_der(lambda: ', '.join(sorted(tabela_completa["Turma"])))
        resumo["Turmas"] = obter_o_que_der(lambda: sorted(turmas.keys()))

        return resumo

    @staticmethod
    def exportar(resumo: dict):
        path = os.path.join(parâmetros.novo_diretório, 'fonte', 'resumo.json')
        with open(path, 'w', encoding='utf-8') as arquivo:
            json.dump(resumo, arquivo, ensure_ascii=False, indent=2)
        return arquivo

    def obter_nome_ue(self) -> str:
        nome_ue = self.master.find_element(By.XPATH, '/html/body/table[1]/tbody/tr[4]').text.split(" - ")[1]
        print(nome_ue)
        return nome_ue
