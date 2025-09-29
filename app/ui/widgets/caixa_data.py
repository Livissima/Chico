from customtkinter import CTkFrame, CTk
from .dropdown import Dropdown
from ...config.parâmetros import parâmetros


class CaixaData(CTkFrame):
    def __init__(self, master, controller):
        super().__init__(master)

        self._dias_letivos = parâmetros.lista_dias_letivos
        self.master = master
        self.controller = controller

        self.__inserir_widgets()
        print(f'Caixa Data inserida')

    def __inserir_widgets(self):
        self._inserir_dia()
        self._inserir_mês()
        self._inserir_ano()

    def _inserir_dia(self):

        pass

    def _inserir_mês(self):
        pass

    def _inserir_ano(self):
        self.dd_ano_teste = Dropdown(
            self,
            alternativas=list(map(str, list(range(2013, 2026)))),
        )
        pass

    def datas(self):
        datas = self._dias_letivos
        datas_splitadas = [data.split('/') for data in datas]
        print(f'{datas = }')


        pass



