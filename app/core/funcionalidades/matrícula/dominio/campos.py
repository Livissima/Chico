"""Modelo do formulário: Campo, Linha, Secao e Esquema.

Tudo aqui é dado puro + comportamento do próprio dado. Não há Streamlit nem Jinja.
Identificadores e chaves são ASCII; acentos só aparecem em rótulos e opções.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Any, Iterator, Mapping

from .regras import Regra, regra_para
from .texto import é_coleção, normalizar_valor, slug
from .tipos import TipoCampo, TipoDado

_CHAVE_VALIDA = re.compile(r"[a-z][a-z0-9_]*")
_TIPOS_COM_OPCOES = (TipoCampo.SELECT, TipoCampo.RADIO, TipoCampo.MULTISELECT)


@dataclass(frozen=True)
class Dependencia:
    """Campo só aparece quando o campo `chave` tem `valor` (ou contém `valor`, se multiselect)."""

    chave: str
    valor: str

    def satisfeita(self, dados: Mapping[str, Any]) -> bool:
        atual = dados.get(self.chave)
        if é_coleção(atual):
            return self.valor in atual
        return atual == self.valor


@dataclass(frozen=True)
class Campo:
    chave: str
    rotulo: str
    tipo: TipoCampo = TipoCampo.TEXTO
    tipo_dado: TipoDado = TipoDado.TEXTO
    opcoes: tuple[str, ...] = ()
    valor_padrao: str = ""
    regras: tuple[Regra, ...] = ()
    depende_de: Dependencia | None = None
    # Prefixo das flags "X" usadas na ficha impressa (ex.: "cor" -> cor_branca, cor_preta...).
    marcador: str | None = None
    # Sufixo da flag quando não dá para derivá-lo da opção (ex.: "Masculino" -> "m").
    sufixos_marcador: Mapping[str, str] = field(default_factory=dict, compare=False, hash=False)

    def __post_init__(self) -> None:
        if not _CHAVE_VALIDA.fullmatch(self.chave):
            raise ValueError(f"Chave inválida {self.chave!r}: use só a-z, 0-9 e _ (sem acento).")
        if self.tipo in _TIPOS_COM_OPCOES and not self.opcoes:
            raise ValueError(f"Campo {self.chave!r} do tipo {self.tipo.value} precisa de opções.")
        if self.marcador and not self.opcoes:
            raise ValueError(f"Campo {self.chave!r} tem marcador mas não tem opções.")
        desconhecidas = set(self.sufixos_marcador) - set(self.opcoes)
        if desconhecidas:
            raise ValueError(f"Campo {self.chave!r}: sufixos para opções inexistentes: {sorted(desconhecidas)}")

    # ------------------------------------------------------------- validação
    @property
    def todas_regras(self) -> tuple[Regra, ...]:
        regra_do_tipo = regra_para(self.tipo_dado)
        return self.regras + ((regra_do_tipo,) if regra_do_tipo else ())

    def validar(self, valor: Any) -> str | None:
        texto = normalizar_valor(valor)
        for regra in self.todas_regras:
            if erro := regra.verificar(self, texto):
                return erro
        return None

    # ------------------------------------------------------------ apresentação
    def atributos_html(self) -> dict[str, str]:
        """Atributos do <input> de texto (máscaras, limites e placeholder lidos pelo JS)."""
        atributos = {"data-tipo": self.tipo_dado.value}
        if self.tipo_dado.placeholder:
            atributos["placeholder"] = self.tipo_dado.placeholder
        for regra in self.regras:
            atributos.update(regra.atributos_html())
        return atributos

    # ------------------------------------------------------------ marcadores
    def sufixo_marcador(self, opcao: str) -> str:
        return self.sufixos_marcador.get(opcao) or slug(opcao)


@dataclass(frozen=True)
class Linha:
    campos: tuple[Campo, ...]
    proporcoes: tuple[float, ...] = ()

    def com_larguras(self) -> list[tuple[Campo, float]]:
        """Pares (campo, largura em % da linha). Sem proporções válidas, divide por igual."""
        pesos = self.proporcoes if len(self.proporcoes) == len(self.campos) else (1,) * len(self.campos)
        total = sum(pesos) or 1
        return [(campo, round(peso / total * 100, 4)) for campo, peso in zip(self.campos, pesos)]


@dataclass(frozen=True)
class Seção:
    titulo: str
    linhas: tuple[Linha, ...]


@dataclass(frozen=True)
class Esquema:
    secoes: tuple[Seção, ...]

    def __post_init__(self) -> None:
        vistas: set[str] = set()
        for campo in self.campos():
            if campo.chave in vistas:
                raise ValueError(f"Chave de campo duplicada: {campo.chave!r}")
            vistas.add(campo.chave)
        for campo in self.campos():
            if campo.depende_de and campo.depende_de.chave not in vistas:
                raise ValueError(f"Campo {campo.chave!r} depende de {campo.depende_de.chave!r}, que não existe.")

    def campos(self) -> Iterator[Campo]:
        for secao in self.secoes:
            for linha in secao.linhas:
                yield from linha.campos

    def campos_ativos(self, dados: Mapping[str, Any]) -> list[Campo]:
        """Campos visíveis para estes dados (o formulário não envia os campos ocultos)."""
        return [c for c in self.campos() if c.depende_de is None or c.depende_de.satisfeita(dados)]

    def validar(self, dados: Mapping[str, Any]) -> list[str]:
        return [
            erro for campo in self.campos_ativos(dados) if (erro := campo.validar(dados.get(campo.chave)))
        ]
