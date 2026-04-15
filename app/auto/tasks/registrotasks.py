# app/auto/registry/task_registry.py
import importlib
import pkgutil
import inspect
from typing import Type, Callable, Any, Dict, get_type_hints
from dataclasses import dataclass, field

from app.auto import tasks


@dataclass
class TaskSignature :
    name: str
    required: Dict[str, type] = field(default_factory=dict)
    optional: Dict[str, type] = field(default_factory=dict)
    aceita_extras: bool = False

    def validar(self, kwargs: dict) -> tuple[bool, str] :
        faltando = set(self.required.keys()) - set(kwargs.keys())
        if faltando :
            return False, f"Argumentos obrigatórios faltando: {faltando}"

        permitidos = set(self.required.keys()) | set(self.optional.keys())
        invalidos = set(kwargs.keys()) - permitidos

        # ← NOVO: só reclama se não tem **kwargs
        if invalidos and not self.aceita_extras :
            return False, f"Argumentos inesperados: {invalidos}"

        return True, ""


class RegistroTasks :

    _tarefas: Dict[str, Type] = {}
    _assinaturas: Dict[str, TaskSignature] = {}
    _tasks_carregadas: bool = False

    @classmethod
    def registrar(cls, nome: str) :

        def wrapper(task_class: Type) -> Type :
            assinatura = cls._extrair_assinatura(nome, task_class)

            cls._tarefas[nome] = task_class
            cls._assinaturas[nome] = assinatura

            print(f"✅ Task registrada: '{nome}'.")
            print(f"   └─ Obrigatórios: {list(assinatura.required.keys())}")
            print(f"   └─ Opcionais: {list(assinatura.optional.keys())}")

            return task_class

        return wrapper

    @staticmethod
    def _extrair_assinatura(nome: str, task_class: Type) -> TaskSignature :
        assinatura = TaskSignature(name=nome)
        sig = inspect.signature(task_class.__init__)
        hints = get_type_hints(task_class.__init__)

        tem_kwargs = any(p.kind == inspect.Parameter.VAR_KEYWORD for p in sig.parameters.values())

        for param_name, param in sig.parameters.items() :
            if param_name == 'self' :
                continue
            if param.kind == inspect.Parameter.VAR_KEYWORD :
                continue

            tipo = hints.get(param_name, Any)

            if param.default == inspect.Parameter.empty :
                assinatura.required[param_name] = tipo
            else :
                assinatura.optional[param_name] = tipo

        # ← NOVO: guardar flag
        assinatura.aceita_extras = tem_kwargs
        return assinatura

    @classmethod
    def carregar_tasks(cls) :
        if cls._tasks_carregadas :
            return

        path = tasks.__path__
        prefix = tasks.__name__ + "."

        for loader, module_name, ispkg in pkgutil.walk_packages(path=path, prefix=prefix):
            try:
                importlib.import_module(module_name)
            except Exception as e:
                print(f"\n# # # # # #\nERRO AO CARREGAR MÓDULO!! '{module_name}'\n{e}\n# # # # # #\n")

        cls._tasks_carregadas = True

        print(f"Total de tasks registradas: {len(cls._tarefas.keys())}\n    → {list(cls._tarefas.keys())}\n")

    @classmethod
    def obter(cls, nome: str) -> Type :
        if nome not in cls._tarefas :
            disponíveis = ", ".join(cls._tarefas.keys())
            raise ValueError(f"Task '{nome}' não encontrada.\n"
                             f"Disponíveis: {disponíveis}")
        return cls._tarefas[nome]

    @classmethod
    def obter_assinatura(cls, nome: str) -> TaskSignature :
        return cls._assinaturas.get(nome)

    @classmethod
    def listar(cls) -> list[str] :
        return list(cls._tarefas.keys())

    @classmethod
    def validar_argumentos(cls, nome: str, kwargs: dict) -> tuple[bool, str] :
        assinatura = cls.obter_assinatura(nome)
        if not assinatura :
            return True, ""
        return assinatura.validar(kwargs)
