import os
import time
import shutil
import base64
from selenium.webdriver.chrome.webdriver import WebDriver


class Impressão:
    def __init__(
            self,
            navegador: WebDriver,
            pasta_temp: str,
            tipos_para_pastas: dict[str, str],
            timeout: int = 15
    ):
        self._navegador = navegador
        self._pasta_temporária = pasta_temp
        self._tipos_para_pastas = tipos_para_pastas
        self._timeout = timeout

    def imprimir_e_mover(self, tipo: str, nome: str = None):
        if tipo not in self._tipos_para_pastas:
            raise ValueError(f'Tipo desconhecido em Impressão: {tipo}')

        destino_pasta = self._tipos_para_pastas[tipo]

        nome_arquivo = f'{nome}.pdf'
        caminho_destino = os.path.join(destino_pasta, nome_arquivo)
        os.makedirs(destino_pasta, exist_ok=True)
        self._salvar_com_cdp(caminho_destino)
        print(f'    PDF "{nome_arquivo}" salvo em "{caminho_destino}"')

    def _salvar_com_cdp(self, caminho_pdf: str):
        resultado = self._navegador.execute_cdp_cmd(
            cmd='Page.printToPDF',
            cmd_args= {
                'landscape' : False,
                'displayHeaderFooter' : False,
                'printBackground' : False,
                'preferCSSPageSize' : False,
                'paperWidth' : 16.5,  # A3 horizontal (420mm)
                'paperHeight' : 11.7  # A3 horizontal (297mm)
        })

        with open(caminho_pdf, 'wb') as f:
            f.write(base64.b64decode(resultado['data']))

    def _esperar_pdf(self) -> str:
        início = time.time()
        while time.time() - início < self._timeout:
            for nome in os.listdir(self._pasta_temporária):
                if not nome.lower().endswith('.pdf'):
                    continue
                caminho = os.path.join(self._pasta_temporária, nome)

                if not caminho.endswith('.crdownload') and os.path.exists(caminho):
                    return caminho

            time.sleep(0.5)

        raise TimeoutError(f'Nenhum PDF apareceu em {self._pasta_temporária}')

    @staticmethod
    def _mover_pdf(caminho_origem: str, pasta_destino: str, nome_pdf):
        os.makedirs(pasta_destino, exist_ok=True)

        if nome_pdf:
            nome_final = f'{nome_pdf}.pdf'
        else:
            nome_final = os.path.basename(caminho_origem)

        caminho_final = os.path.join(pasta_destino, nome_final)
        shutil.move(caminho_origem, caminho_final)
        print(f'PDF: "{nome_final}" movido para: "{caminho_final}"')