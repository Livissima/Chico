from dataclasses import dataclass
from app.config.classes.cpf import CPF

@dataclass(slots=True)
class CredencialSIAP:
    id: CPF
    senha: str
    tipo: str
