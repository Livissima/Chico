import base64
import os.path

import requests
from pandas import read_excel
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By

from app.auto.data.sites.propriedades import Propriedades
from app.auto.functions.navegação import Navegação
from app.ui.config.parâmetros import parâmetros


class ScrapingSige:
    """
    Ideia de tarefa para visitar as fichas de todos os estudantes e extrair todos os dados disponíveis em "ficha do aluno"
    """
    def __init__(
            self,
            navegador: Chrome,
            turmas: list[str]
    ):
        self.master = navegador

        self.nv = Navegação(navegador, 'sige')
        self.pp = Propriedades('sige')
        self.path = os.path.join(parâmetros.novo_diretório, 'fonte', 'fotos')
        self.leitura_df = read_excel(
            os.path.join(parâmetros.novo_diretório, 'Database.xlsx'), sheet_name='Base Ativa'
        )
        self.logon()

        self.obter_fotos(turmas)

    def logon(self):
        self.master.get(self.pp.url)
        self.master.maximize_window()
        self.nv.digitar_xpath('misc', 'input id', string=self.pp.credenciais['id'])
        self.nv.digitar_xpath('misc', 'input senha', string=self.pp.credenciais['senha'])

        self.nv.clicar('xpath', 'misc', 'entrar')
        self.nv.clicar('xpath', 'misc', 'alerta')

    def obter_fotos(self, turmas: list):
        self.nv.caminhar('ficha aluno')

        df = self.leitura_df[['Turma', 'Estudante', 'Matrícula']]
        df = df[df['Turma'].isin(turmas)]

        for linha in df.itertuples():
            turma = linha.Turma
            matrícula = linha.Matrícula
            estudante = linha.Estudante


            self.nv.aguardar()
            self.nv.digitar_xpath('ficha aluno', 'matrícula', string=matrícula)
            self.nv.clicar('xpath', 'ficha aluno', 'click fora')
            self.nv.aguardar()
            # input_nome = self.master.find_elements('ID', 'txtNome')
            self.nv.aguardar_preenchimento('txtNome')

            self.download_foto(
                estudante=estudante,
                path_destino=os.path.join(self.path, f'{turma}')
            )
            self.nv.aguardar()
            # self.nv.caminhar('ficha aluno')
            # self.master.
            self.nv.clicar('xpath', 'ficha aluno', 'limpar')
            self.nv.aguardar(1)
            # self.master.find_element(By.XPATH, '/html/body/div[8]/form/table[1]/tbody/tr[2]/td/table/tbody/tr[2]/td[2]/input[1]').clear()
            # self.nv.clicar('xpath', 'ficha aluno', 'click fora')
            # self.master.refresh()
            # self.nv.aguardar(1)


    def download_foto(self, estudante, path_destino) :
        elemento = self.master.find_element(By.CSS_SELECTOR, '#fotoAluno')
        url_elemento = elemento.get_attribute('src')

        if url_elemento.startswith('data:image/png;base64,') :
            base64_data = url_elemento.split(',')[1]

            image_data = base64.b64decode(base64_data)

            os.makedirs(path_destino, exist_ok=True)

            destino = os.path.join(path_destino, f'{estudante}.png')
            with open(destino, 'wb') as file :
                file.write(image_data)
                print(f'Foto de {estudante} baixada.')
        else :
            try :
                response = requests.get(url_elemento)
                if response.status_code == 200 :
                    destino = os.path.join(path_destino, f'{estudante}.jpg')
                    with open(destino, 'wb') as file :
                        file.write(response.content)
                        print(f'Foto de {estudante} baixada.')
                else :
                    print(f'Erro ao baixar foto de {estudante}: Status code {response.status_code}')
            except Exception as e :
                print(f'Erro ao baixar foto de {estudante}: {e}')