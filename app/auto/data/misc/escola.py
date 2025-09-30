# import json
# import os
#
# from app.config.parâmetros import parâmetros
#
#
# class Escola:
#
#     @staticmethod
#     def modulações() :
#         dados = []
#         lista_jsons = os.listdir(os.path.join(parâmetros.novo_diretório, 'fonte', 'modulações'))
#         print(f'{lista_jsons = }')
#         lista_de_listas_de_dicionários = []
#
#         for arquivo in lista_jsons :
#             if arquivo.endswith('.json') :
#                 caminho = os.path.join(parâmetros.novo_diretório, 'fonte', 'modulações', arquivo)
#                 with open(caminho, 'r', encoding='utf-8') as f :
#                     lista_de_listas_de_dicionários.append(json.load(f))
#
#         for lista in lista_de_listas_de_dicionários :
#             cpf = lista[1]['coluna_1']
#             nome = lista[1]['coluna_3']
#             vínculo = lista[3]['coluna_1']
#
#             # Filtra apenas os dicionários que têm todas as colunas necessárias
#             disciplinas = {f"disciplina_{i - 6}" : {
#                 'série' : dicionario['coluna_3'], 'turma' : dicionario['coluna_4'],
#                 'disciplina' : dicionario['coluna_8'], 'quantidade' : dicionario['coluna_9']
#             } for i, dicionario in enumerate(lista[6 :], start=6) if
#                 all(key in dicionario for key in ['coluna_3', 'coluna_4', 'coluna_8', 'coluna_9'])}
#
#             # Agora você tem um dicionário organizado com todas as disciplinas
#             print(f"CPF: {cpf}")
#             print(f"Nome: {nome}")
#             print(f"Vínculo: {vínculo}")
#             for key, disc in disciplinas.items() :
#                 print(f"{key}: {disc}")
#
# #     @property
# #     def turmas(self) -> list[str]:
# #         return ['6A', '6B', '6C', '7A', '7B', '8A', '8B', '9A']
# #
# #     @property
# #     def séries(self) -> list[str]:
# #         return [
# #             '6', '7', '8', '9'
# #         ]
# #
# #     @property
# #     def turmas_por_serie(self) -> dict[str, list[str]]:
# #         # lista_turmas = Prévias().turmas
# #         pass
# #
# #     @property
# #     def turnos(self) -> dict[str:str]:
# #         return {
# #             '1': 'matutino'
# #         }
# #
# #     @property
# #     def composições(self) -> dict[str:str]:
# #         return {
# #             '' : ''
# #         }
# #
# #     @staticmethod
# #     def gerar_turmas_por_serie(lista_turmas: list[str]) -> dict[str, list[str]] :
# #         turmas_por_serie = defaultdict(list)
# #
# #         for turma in lista_turmas :
# #             # Extrai a série (todos os dígitos no início da string)
# #             serie = ''.join(filter(str.isdigit, turma))
# #             if serie :
# #                 turmas_por_serie[serie].append(turma)
# #
# #         # Converte para dict normal e ordena
# #         return {serie : sorted(turmas) for serie, turmas in sorted(turmas_por_serie.items())}
# #
# #     @staticmethod
# #     def séries(self, lista) -> list[str] :
# #         turmas = ['6A', '6B', '6C', '7A', '7B', '8A', '8B', '9A']
# #         # Extrai o número da série de cada turma, remove duplicatas e ordena
# #         series_unicas = sorted(set(turma[0] for turma in turmas))  # Para séries de 1 dígito
# #         return series_unicas
# #