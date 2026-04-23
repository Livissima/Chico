from dataclasses import dataclass


@dataclass(frozen=True)
class Credenciais:
    id: str
    senha: str
    tipo: str | None = None
