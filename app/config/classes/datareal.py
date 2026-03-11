#
# from datetime import date
# from typing import Optional, SupportsIndex
#
# from app.config.app_config import obter_string_numérica
#
#
# class DataReal:
#     #todo terminar de construir o tipo
#     def __init__(
#             self,
#             data: str | int | tuple | date
#     ):
#         self._entrada = data
#         self._validez = '-'
#         self._valor = self._executar(self._entrada)
#
#
#     def _executar(self, entrada: str | int | float | date | None) -> Optional[str] :
#         data = self._preparar_data(entrada)
#
#
#
#
#
#
#
#         self._validez = 'Inválido'
#         return f"'{data}'"
#
#     def _preparar_data(self, data: str | int | float | date | None):
#         if isinstance(data, date) :
#             return data
#
#         if isinstance(data, str):
#             return self._preparar_string(data)
#
#
#
#
#     def _preparar_string(self, data: str):
#         if r'/' in data and len(data) == 10 :
#             lista = data.split(r'/')
#             dia = lista[0]
#             mês = lista[1]
#             ano = lista[2]
#
#             if (len(dia), len(mês), len(ano)) != (2, 2, 4) :
#                 return '-'
#
#             return date(int(ano), int(mês), int(dia))
#
#         if len(data) == 8  and r'/' not in data :
#             return obter_string_numérica(data)
#
#
#
#
#
# if __name__ == '__main__' :
#     valor_str = '20/03/95'
#     instância_data = DataReal(valor_str)._valor
#
#     print(instância_data)
#
#
#
#
