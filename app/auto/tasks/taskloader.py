# import importlib
# import pkgutil
# import inspect
# from pathlib import Path
# from app.auto.tasks.taskregistry import TaskRegistry
#
# class TaskLoader:
#     @classmethod
#     def carregar_tasks(cls) :
#         if cls._tasks_carregadas :
#             return
#
#         path = tasks.__path__
#         prefix = tasks.__name__ + "."
#
#         for loader, module_name, ispkg in pkgutil.walk_packages(path=path, prefix=prefix):
#             try:
#                 importlib.import_module(module_name)
#             except Exception as e:
#                 print(f"\n# # # # # #\nERRO AO CARREGAR MÓDULO!! '{module_name}'\n{e}\n# # # # # #\n")
#
#         cls._tasks_carregadas = True
#
#         print(f"Total de tasks registradas: {len(cls._tarefas)}\n")