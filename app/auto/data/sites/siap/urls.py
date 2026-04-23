from dataclasses import dataclass


@dataclass(frozen=True)
class SiapUrls:
    tela_login: str = 'https://siap.educacao.go.gov.br/'

