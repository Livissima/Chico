# app/auto/registry.py
from typing import Dict, Type, Callable


class TaskRegistry :
    _tarefas: Dict[str, Type] = {}

    @classmethod
    def registrar(cls, nome: str) :
        def wrapper(task_class: Type) -> Type :
            cls._tarefas[nome] = task_class
            print(f"✅ Task '{nome}' registrada: {task_class.__name__}")
            return task_class
        return wrapper

    @classmethod
    def obter(cls, nome: str) -> Type :
        if nome not in cls._tarefas :
            raise ValueError(f"❌ Task '{nome}' não encontrada. "
                             f"Disponíveis: {list(cls._tarefas.keys())}")
        return cls._tarefas[nome]

    @classmethod
    def listar(cls) -> list[str] :
        return list(cls._tarefas.keys())
