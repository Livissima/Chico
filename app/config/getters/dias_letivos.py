import json
import os


class DiasLetivos:

    def __init__(self, path, ano):
        self.lista_dias_letivos = self._dias_letivos(path, ano)[0]
        self.dicionário_dias_letivos = self._dias_letivos(path, ano)[1]

    def _dias_letivos(self, path, ano):
        lista_dias_letivos = self._ler_json_dias_letivos(path, ano)
        dicionário_dias_letivos = self._gerar_dict_dias_letivos(lista_dias_letivos)
        return lista_dias_letivos, dicionário_dias_letivos

    @staticmethod
    def _ler_json_dias_letivos(path, ano) :
        _path = os.path.join(path, 'fonte', f'Dias Letivos {ano}.json')
        try :
            with open(_path, 'r', encoding='utf-8') as arquivo :
                dias_letivos = json.load(arquivo)
                return dias_letivos
        except FileNotFoundError as e :
            print(f'Erro em {e}')
            return []

    @staticmethod
    def _gerar_dict_dias_letivos(leitura) :
        dias_splitados = [dia.split('/') for dia in leitura]
        lista_meses = [dia[1] for dia in dias_splitados]
        meses_letivos = list(sorted(set(lista_meses)))

        dicionário = {chave : [dia[0] for dia in dias_splitados if dia[1] == chave] for chave in meses_letivos}
        return dicionário
