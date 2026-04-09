import base64
import os.path
import requests
from pandas import read_excel
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By

from app.auto.tasks.taskregistry import TaskRegistry
from app.auto.data.sites.propriedadesweb import PropriedadesWeb
from app.auto.functions.navegaçãoweb import NavegaçãoWeb
from app.config.parâmetros import parâmetros

@TaskRegistry.registrar('fotos')
class DownloadFotosEstudantes:

    def __init__(
            self,
            navegador: Chrome,
            turmas: list[str],
            **kwargs
    ):
        self.master = navegador

        self._nv = NavegaçãoWeb(navegador, 'sige')
        self._pp = PropriedadesWeb('sige')
        self._path = os.path.join(parâmetros.diretório_base, 'fonte', 'fotos')
        self._leitura_df = read_excel(
            os.path.join(parâmetros.diretório_base, 'Database.xlsx'), sheet_name='Base Ativa'
        )
        self._logon()

        self._obter_fotos(turmas)

    def _logon(self):
        self.master.get(self._pp.urls)
        self.master.maximize_window()
        self._nv.digitar_xpath('misc', 'input id', string=self._pp.credenciais_padrão['id'])
        self._nv.digitar_xpath('misc', 'input senha', string=self._pp.credenciais_padrão['senha'])

        self._nv.clicar('xpath', 'misc', 'entrar')
        self._nv.clicar('xpath', 'misc', 'alerta')

    def _obter_fotos(self, turmas: list):
        self._nv.acessar_destino('ficha aluno')

        df = self._leitura_df[['Turma', 'Estudante', 'Matrícula']]
        df = df[df['Turma'].isin(turmas)]

        for linha in df.itertuples():
            turma = linha.Turma
            matrícula = linha.Matrícula
            estudante = linha.Estudante


            self._nv.aguardar_página()
            self._nv.digitar_xpath('ficha aluno', 'matrícula', string=matrícula)
            self._nv.clicar('xpath', 'ficha aluno', 'click fora')
            self._nv.aguardar_página()

            self._nv.aguardar_preenchimento('txtNome')

            self._download_foto(
                estudante=estudante,
                path_destino=os.path.join(self._path, f'{turma}')
            )
            self._nv.aguardar_página()

            self._nv.clicar('xpath', 'ficha aluno', 'limpar')
            self._nv.aguardar_página(1)

    def _download_foto(self, estudante, path_destino) :
        elemento = self.master.find_element(By.CSS_SELECTOR, '#fotoAluno')
        url_elemento = elemento.get_attribute('src')
        print(f'{url_elemento = }')

        os.makedirs(path_destino, exist_ok=True)  # ← mover para cá

        if not url_elemento.startswith('data:image/png;base64,') :
            try :
                response = requests.get(url_elemento)

                if response.status_code != 200 :
                    raise Exception(f'Erro ao baixar foto de {estudante}: Status code {response.status_code}')

                destino = os.path.join(path_destino, f'{estudante}.jpg')

                with open(destino, 'wb') as file :
                    file.write(response.content)

                print(f'Foto de {estudante} baixada.')
                return

            except Exception as e :
                print(f'Erro ao baixar foto de {estudante}: {e}')
                return  # ← importante também

        base64_data = url_elemento.split(',')[1]
        image_data = base64.b64decode(base64_data)

        destino = os.path.join(path_destino, f'{estudante}.png')

        with open(destino, 'wb') as file :
            file.write(image_data)

        print(f'Foto de {estudante} baixada.')

