# class Escola:

#     @property
#     def turmas(self) -> list[str]:
#         return ['6A', '6B', '6C', '7A', '7B', '8A', '8B', '9A']
#
#     @property
#     def séries(self) -> list[str]:
#         return [
#             '6', '7', '8', '9'
#         ]
#
#     @property
#     def turmas_por_serie(self) -> dict[str, list[str]]:
#         # lista_turmas = Prévias().turmas
#         pass
#
#     @property
#     def turnos(self) -> dict[str:str]:
#         return {
#             '1': 'matutino'
#         }
#
#     @property
#     def composições(self) -> dict[str:str]:
#         return {
#             '' : ''
#         }
#
#     @staticmethod
#     def gerar_turmas_por_serie(lista_turmas: list[str]) -> dict[str, list[str]] :
#         turmas_por_serie = defaultdict(list)
#
#         for turma in lista_turmas :
#             # Extrai a série (todos os dígitos no início da string)
#             serie = ''.join(filter(str.isdigit, turma))
#             if serie :
#                 turmas_por_serie[serie].append(turma)
#
#         # Converte para dict normal e ordena
#         return {serie : sorted(turmas) for serie, turmas in sorted(turmas_por_serie.items())}
#
#     @staticmethod
#     def séries(self, lista) -> list[str] :
#         turmas = ['6A', '6B', '6C', '7A', '7B', '8A', '8B', '9A']
#         # Extrai o número da série de cada turma, remove duplicatas e ordena
#         series_unicas = sorted(set(turma[0] for turma in turmas))  # Para séries de 1 dígito
#         return series_unicas
#