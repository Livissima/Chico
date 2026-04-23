import json
import os.path
from pathlib import Path
from typing import Any
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

from app.config.settings.functions import escrever_json
from app.auto.tasks.registrotasks import RegistroTasks
from app.auto.data.sites.propriedadesweb import PropriedadesWeb
from app.auto.functions.navegaçãoweb import NavegaçãoWeb
from app.config.parâmetros import parâmetros
from app.config.parâmetros.getters.tempo import tempo

@RegistroTasks.registrar('sondagem')
class Sondagem:

    def __init__(self, navegador: Chrome, **kwargs) :

        print(f'class Sondagem instanciada.')
        _path = Path(parâmetros.diretório_base, 'fonte', 'resumo.json')
        self.master = navegador
        # self.destino_comum = destino

        self._nv = NavegaçãoWeb(navegador, 'sige')
        self._pp = PropriedadesWeb('sige')

        self._executar(_path)


    def _executar(self, path: Path):
        self._logon()
        elemento_base = self._obter_elemento_base()
        tabela = self._extrair_tabela_do_elemento(elemento_base)
        resumo = self._gerar_resumo(tabela)

        self.exportar(path, resumo)

        parâmetros.resumo = resumo
        parâmetros.nome_ue = resumo['Nome UE']

        self.master.quit()

        print(f'Sucesso!\n{json.dumps(resumo, indent=4, ensure_ascii=False)}')

    def _logon(self):
        self.master.get(self._pp.urls)
        self.master.maximize_window()
        self._nv.digitar_xpath('misc', 'input id', string=self._pp.credenciais_padrão.id)
        self._nv.digitar_xpath('misc', 'input senha', string=self._pp.credenciais_padrão.senha)
        self._nv.clicar('xpath', 'misc', 'entrar')
        self._nv.clicar('xpath', 'misc', 'alerta')

    def _obter_elemento_base(self):
        self._nv.acessar_destino('sondagem')
        print(f'caminhado para sondagem')

        self._nv.clicar('xpath', 'resumo', 'turmas', 'ativas')
        print(f'Clicado em turmas ativas')

        self._nv.digitar_xpath('resumo', 'turmas', 'input data', string=tempo.hoje)
        print(f'xpath digitado')

        self._nv.clicar('id', 'gerar')
        print(f'clicado em gerar')

        print(f'Aguardando')
        self._nv.aguardar_página(1)

        print(f'Localizando elemento')

        elemento_base = self._nv.master.find_element(By.CSS_SELECTOR, 'body > table.tabela')
        print(f'{elemento_base = }')

        return elemento_base

    @staticmethod
    def _extrair_tabela_do_elemento(elemento: WebElement) -> dict[str | Any, list[Any]] :
        cabeçalhos = ['Composição', 'Série', 'Turno', 'Código', 'Turma', 'Horário', 'Funcionamento', 'Sala',
                      'Tipo Turma', 'Tipo Atendimento', 'Local Diferenciado', 'Data Criação', 'Situação',
                      'Capacidade legal', 'Capacidade física', 'Efetivados', 'Não Efetivados', 'Vagas',
                      'Excedente Autorizado']

        tabela_turmas = {cabeçalho : [] for cabeçalho in cabeçalhos}

        todas_linhas = elemento.find_elements(By.TAG_NAME, 'tr')

        print(f"Total de linhas encontradas: {len(todas_linhas)}")

        for i, linha in enumerate(todas_linhas) :
            celulas = linha.find_elements(By.TAG_NAME, 'td')
            print(f"Linha {i}: {len(celulas)} células")

            if len(celulas) < 19 :
                print(f"Pulando linha {i} (cabeçalho ou linha inválida)")
                continue

            linha_dados = []
            for celula in celulas :
                texto = celula.text.strip()
                texto = texto.replace('&nbsp;', '').replace('\u00a0', '').strip()
                linha_dados.append(texto if texto else "0")  # Usar "0" para valores vazios

            for j, cabecalho in enumerate(cabeçalhos) :
                if j < len(linha_dados) :
                    if cabecalho in ['Capacidade legal', 'Capacidade física', 'Efetivados', 'Não Efetivados', 'Vagas',
                                     'Excedente Autorizado'] :
                        try :
                            valor = int(linha_dados[j]) if linha_dados[j] else 0
                            tabela_turmas[cabecalho].append(valor)
                        except ValueError :
                            tabela_turmas[cabecalho].append(0)
                    else :
                        tabela_turmas[cabecalho].append(linha_dados[j])
                else :
                    tabela_turmas[cabecalho].append(None)

        print(f"Extraídas {len(tabela_turmas['Código'])} turmas")

        if tabela_turmas['Turma'] :
            print("Turmas extraídas:", tabela_turmas['Turma'])
        else :
            print("Nenhuma turma extraída - verificando estrutura da tabela:")
            print(elemento.get_attribute('outerHTML'))

        return tabela_turmas

    def _gerar_resumo(self, tabela) -> dict[str, int | str]:
        resumo = {}
        # elemento = self._obter_elemento_base()
        # tabela_completa = self._extrair_tabela_do_elemento(elemento)

        def obter_o_que_der(operacao, default='Erro'):
            try:
                resultado = operacao()

                if isinstance(resultado, list) and len(resultado) == 0:
                    return default

                return resultado
            except (KeyError, ValueError, TypeError, ZeroDivisionError):
                return default

        chaves  = list(obter_o_que_der(lambda: tabela["Turma"]))
        valores = list(obter_o_que_der(lambda: tabela["Código"]))
        turmas = dict(zip(chaves, valores))

        resumo["Nome UE"] = obter_o_que_der(lambda: self.__obter_nome_ue())
        resumo["Códigos Turmas"] = obter_o_que_der(lambda: list(turmas.values()))
        resumo["Composições"] = obter_o_que_der(lambda: ', '.join(list(set(tabela["Composição"]))))
        resumo["Turnos"] = obter_o_que_der(lambda: list(set(tabela["Turno"])))
        resumo["Tipos"] = obter_o_que_der(lambda: list(set(tabela["Tipo Turma"])))
        resumo["Excedente autorizado"] = obter_o_que_der(lambda: sum([int(valor) for valor in tabela["Excedente Autorizado"]]))
        resumo["Excedente ocupado"] = obter_o_que_der(lambda: sum([valor for valor in map(int, tabela["Vagas"]) if valor < 0]) * -1)
        resumo["Capacidade física"] = obter_o_que_der(lambda: sum([int(valor) for valor in tabela["Capacidade física"]]))
        resumo["Capacidade legal"] = obter_o_que_der(lambda: sum([int(valor) for valor in tabela["Capacidade legal"]]))

        resumo["Capacidade Total"] = obter_o_que_der(lambda: resumo["Capacidade física"] + resumo["Excedente autorizado"])
        resumo["Efetivados"] = obter_o_que_der(lambda: sum([int(valor) for valor in tabela["Efetivados"]]))
        resumo["Vagas disponíveis"] = obter_o_que_der(lambda: resumo["Capacidade legal"] - resumo["Efetivados"])
        resumo["Vagas absolutas"] = obter_o_que_der(lambda: resumo["Capacidade Total"] - resumo["Efetivados"])

        resumo["Balanço Físico"] = obter_o_que_der(lambda: f'{(resumo["Efetivados"] / resumo["Capacidade física"]) * 100:.1f} %' if resumo["Capacidade física"] != 0 else "0.0 %")
        resumo["Balanço absoluto"] = obter_o_que_der(lambda: f'{(resumo["Efetivados"] / resumo["Capacidade Total"]) * 100:.1f} %' if resumo["Capacidade Total"] != 0 else "0.0 %")

        resumo["Turmas Ativas"] = obter_o_que_der(lambda: ', '.join(sorted(tabela["Turma"])))
        resumo["Turmas"] = obter_o_que_der(lambda: sorted(turmas.keys()))

        return resumo

    @staticmethod
    def exportar(path: Path, resumo: dict):
        escrever_json(resumo, path)

    def __obter_nome_ue(self) -> str:
        nome_ue = self.master.find_element(By.XPATH, '/html/body/table[1]/tbody/tr[4]').text.split(" - ")[1]
        print(nome_ue)
        return nome_ue
