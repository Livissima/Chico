"""Montagem do contexto que alimenta o template da ficha impressa (pagina_print.html)."""
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Mapping, Sequence

from .campos import Esquema
from .texto import é_coleção


class EtapaDeContexto(ABC):
    """Uma transformação do contexto. Para criar uma nova, herde desta classe e
    passe a instância ao ConstrutorDeContexto; nada existente precisa mudar."""

    @abstractmethod
    def aplicar(self, esquema: Esquema, contexto: dict[str, Any]) -> None: ...


class MarcadoresDeOpcao(EtapaDeContexto):
    """Para cada campo com `marcador`, cria uma flag por opção: '<marcador>_<sufixo>' = 'X' ou ''.

    Ex.: Campo(chave="cor_etnia", marcador="cor", opcoes=(..., "Parda", ...)) e valor "Parda"
    produzem cor_parda='X' e as demais cor_*=''.
    """

    def aplicar(self, esquema, contexto):
        chaves_de_campos = {c.chave for c in esquema.campos()}
        geradas: set[str] = set()

        for campo in esquema.campos():
            if not campo.marcador:
                continue
            escolhidas = self._como_conjunto(contexto.get(campo.chave))
            for opcao in filter(None, campo.opcoes):  # ignora a opção em branco
                nome = f"{campo.marcador}_{campo.sufixo_marcador(opcao)}"
                if nome in geradas or nome in chaves_de_campos:
                    raise ValueError(f"Flag de marcador duplicada ou em conflito com um campo: {nome!r}")
                geradas.add(nome)
                contexto[nome] = "X" if opcao in escolhidas else ""

    @staticmethod
    def _como_conjunto(valor: Any) -> set[str]:
        if é_coleção(valor):
            return {str(v) for v in valor}
        return {str(valor)} if valor else set()


class ConstrutorDeContexto:
    def __init__(self, etapas: Sequence[EtapaDeContexto] | None = None) -> None:
        self._etapas = tuple(etapas) if etapas is not None else (MarcadoresDeOpcao(),)

    def construir(self, esquema: Esquema, dados: Mapping[str, Any]) -> dict[str, Any]:
        # Começa pelos padrões de TODOS os campos: campos ocultos não vêm nos dados e o
        # template (StrictUndefined) exige que todas as variáveis existam.
        contexto: dict[str, Any] = {c.chave: c.valor_padrao for c in esquema.campos()}
        contexto.update(dados)
        for etapa in self._etapas:
            etapa.aplicar(esquema, contexto)
        return contexto
