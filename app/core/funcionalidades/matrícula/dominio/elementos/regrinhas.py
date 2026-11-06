from __future__ import annotations

from app.core.funcionalidades.matrícula.dominio.regras import Obrigatorio, ApenasLetras, ApenasNumeros, \
    ComprimentoMinimo, ComprimentoMaximo

obrigatório = (Obrigatorio(), )
obrigatório_letra = (Obrigatorio(), ApenasLetras())
obrigatório_número = (Obrigatorio(), ApenasNumeros())


número = (ApenasNumeros(), )
letra = (ApenasLetras(), )

def obrigatório_número_max(número_máximo_números):
    return Obrigatorio(), ApenasNumeros(), ComprimentoMaximo(número_máximo_números),

def obrigatório_letra_max(número_máximo_letras):
    return Obrigatorio(), ApenasLetras(), ComprimentoMaximo(número_máximo_letras),

def obrigatório_min(número_mínimo_de_caracteres: int):
    return Obrigatorio(), ComprimentoMinimo(número_mínimo_de_caracteres),

def obrigatório_max(número_máximo_de_caracteres: int):
    return Obrigatorio(), ComprimentoMaximo(número_máximo_de_caracteres),


def número_max(número_máximo_de_números: int):
    return ApenasNumeros(), ComprimentoMaximo(número_máximo_de_números), 