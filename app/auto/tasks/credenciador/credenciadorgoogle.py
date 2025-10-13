import sys
import time
from typing import Literal
from selenium.webdriver import Edge
import pandas as pd
from pandas import DataFrame

from app.auto.functions.navegaçãoweb import NavegaçãoWeb
from app.auto.data.sites.propriedades import Propriedades


class CredenciadorGoogle:


    def __init__(
            self,
            navegador,
            estudante,
            matrícula,
            email,
            dn,
            nova_senha,
            **kwargs
    ) :
        print(f'class GerenciadorGoogle instanciada.')

        self.master: Edge = navegador
        self.nv = NavegaçãoWeb(navegador, 'google')
        self.pp = Propriedades(site='google')

        self.gerenciar(
            estudante=estudante,
            matrícula=matrícula,
            email=email,
            dn=dn,
            nova_senha=nova_senha
        )


    def gerenciar(self, estudante, matrícula, email, dn, nova_senha) :
        print(f'{estudante = }')

        self.nv.acessar_página(self.pp.url)

        self.nv.digitar_xpath('input email', string=email)
        print(f'Email digitado: {email}')
        self.nv.clicar('xpath', 'avançar email')

        self.nv.digitar_xpath('input senha', string='123456789')
        self.nv.clicar('xpath', 'avançar senha')
        print(f'Senha digitada: 123456789')

        self.nv.digitar_xpath('input nova senha', string=nova_senha)
        self.nv.digitar_xpath('input confirmar nova senha', string=nova_senha)
        print(f'Nova senha digitada nos 2 campos: {nova_senha}')

        self.nv.clicar('xpath', 'avançar nova senha')
        print(f'Estudante {estudante} concluido.')


        self.nv.aguardar_página()
        self.master.delete_all_cookies()

        self.master.refresh()
        time.sleep(1)




    #
    # #################################################
    #
    #         alerta = None
    #         dict_senhas = dict(enumerate([senha_padrão, senha_padrão2, senha_dn, senha_alt]))
    #
    #         for índice, senha in dict_senhas.items() :
    #             alerta = None
    #             print(f'Tentando {senha}')
    #
    #             self._tentar_senha(senha)
    #             self._checar_alerta(índice, dict_senhas)
    #
    #             print('O Loop ```for índice, senha in dict_senhas.items() :``` , do método `self.gerenciar_google()`, chegou ao fim')
    #
    #
    #
    #
    #     def _decidir(self, alerta, índice, dict_senhas):
    #
    #         if alerta is not None:
    #             if índice+1 in dict_senhas.keys() :
    #                 print(f'Erramos. tentando {dict_senhas[índice + 1]}')
    #                 self._tentar_senha(dict_senhas[índice + 1])
    #                 self._checar_alerta(índice, dict_senhas)
    #             else:
    #                 print('Tentamos tudo e não deu. Seguindo.')
    #         if alerta is None :
    #             print('Acertamos. Seguindo.')
    #
    #
    #
    #     def _checar_alerta(self, i, _dict_senhas):
    #         alerta = None
    #
    #         try :
    #             alerta = self.master.find_element(By.XPATH, '//*[@id="c0"]/div[2]/span')
    #         except NoSuchElementException :
    #             pass
    #
    #         self._decidir(alerta, i, _dict_senhas)
    #
    #
    #     def _tentar_senha(self, senha) :
    #         self.nv.digitar_xpath('input senha', string=senha)
    #         self.nv.clicar('xpath', 'avançar senha')

    #################################################################################
