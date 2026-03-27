#app/auto/tasks/sige/downloaddadosservidores.py
import json

from app.auto.data.sites.propriedadesweb import PropriedadesWeb
from app.auto.functions.navegaçãoweb import NavegaçãoWeb
from selenium.webdriver import Chrome
from pathlib import Path
import time

from app.config.parâmetros.getters.tempo import tempo


class DownloadDadosServidores:
    _nome_relatório_simples = 'lista_servidores'

    def __init__(
            self,
            navegador: Chrome,
            path: Path,
            **kwargs
    ):
        print(f'class Servidores instanciada.')
        self._master = navegador
        self._path = Path(path, 'fonte')
        self._caminho_completo = Path(self._path, f'{self._nome_relatório_simples}.json')

        self._nv = NavegaçãoWeb(navegador, 'sige')
        self._pp = PropriedadesWeb('sige')
        self._logon()
        self._executar()

        self._master.quit()

    def _logon(self) -> None:
        self._master.get(self._pp.urls)
        self._master.maximize_window()
        self._nv.digitar_xpath('misc', 'input id', string=self._pp.credenciais['id'])
        self._nv.digitar_xpath('misc', 'input senha', string=self._pp.credenciais['senha'])
        self._nv.clicar('xpath', 'misc', 'entrar')
        self._nv.clicar('xpath', 'misc', 'alerta')

    def _executar(self) -> None:
        if not self._caminho_completo.exists():
            print(f'\nBase de servidores não encontrada. Gerando base...\n')
            self._processar_base_inicial()

        self._pesquisar_dados_pessoais()

    def _pesquisar_dados_pessoais(self):
        print('\n ## Pesquisando dados pessoais')
        url_dados = 'https://sige.educacao.go.gov.br/sige/modulos/Dossie/Relatorios/ddv_funcionario_con.asp#'
        json_servidores = self._carregar_json()
        path_destino = Path(self._path, 'Servidores')
        print(f'{json_servidores = }')

        for nome, cpf in json_servidores.items():
            self._master.get(url_dados)
            self._nv.digitar_xpath('misc', 'cpf servidor', string=cpf)
            self._nv.clicar('id livre', 'gerarRel')
            self._nv.download_json(nome, path_destino)


    def _processar_base_inicial(self):
        lista_nominal_servidores_atuais = self._obter_lista_de_votantes()
        todos_servidores = self._obter_todos_os_servidores_da_história_da_ue()

        relação_servidor_cpf = {
           servidor['Nome'] : servidor['CPF'] for servidor in todos_servidores if len(servidor['CPF']) == 14 and servidor['Nome'] != 'Nome' and servidor['Nome'] in lista_nominal_servidores_atuais
        }
        self._descarregar_json(relação_servidor_cpf)

    def _obter_lista_de_votantes(self) -> list[str]:
        url_votantes = 'https://sige.educacao.go.gov.br/sige/modulos/Academico/Relatorios/Ave_relatorioVotantes_con.asp#'
        xpath_opção_servidores = '/html/body/div[8]/form/table/tbody/tr/td/table/tbody/tr[5]/td/input'

        self._master.get(url_votantes)
        self._nv.clicar('xpath livre', xpath_opção_servidores)
        self._nv.digitar_xpath('misc', 'data eleição', string=tempo.hoje)
        self._nv.clicar('id livre', 'gerarRel')
        votantes = self._nv.obter_tabelas()
        lista_nominal = sorted([votante['Nome'] for votante in votantes if votante['Nome'] != 'Nome'])
        return lista_nominal


    def _obter_todos_os_servidores_da_história_da_ue(self):
        url_todos_os_servidores = 'https://sige.educacao.go.gov.br/sige/modulos/Dossie/ddv_funcionario_con.asp'
        self._master.get(url_todos_os_servidores)
        todos_os_servidores = self._nv.obter_tabelas()
        return todos_os_servidores

    def _carregar_json(self) -> dict[str, str]:
        with open(self._caminho_completo, 'r', encoding='utf-8') as arquivo :
            return json.load(arquivo)

    def _descarregar_json(self, relação_servidores: dict[str, str]) -> None:
        with open(self._caminho_completo, 'w', encoding='utf-8') as arquivo:
            return json.dump(relação_servidores, arquivo, ensure_ascii=False, indent=2)


