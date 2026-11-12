"""Regras que envolvem mais de um campo (e podem cruzar seções).

São verificadas ao gerar o relatório, sobre os dados já preparados (`Esquema.preparar`).
Algumas também têm versão instantânea no navegador: `para_js` descreve a regra para o
scripts.js, que só aplica os tipos que conhece. Quem devolve None em `para_js` só roda no servidor.

Para criar uma regra nova, herde de `RegraDeEsquema`; nada existente precisa mudar.
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import TYPE_CHECKING, Any, Mapping

from .regras import Erro
from .texto import analisar_data, normalizar_valor, só_dígitos

if TYPE_CHECKING:
    from .campos import Esquema


class RegraDeEsquema(ABC):
    @abstractmethod
    def chaves(self) -> tuple[str, ...]:
        """Chaves de campos que a regra usa (o Esquema confere se todas existem)."""

    @abstractmethod
    def verificar(self, esquema: "Esquema", dados: Mapping[str, Any]) -> list[Erro]: ...

    def para_js(self, esquema: "Esquema") -> dict[str, Any] | None:
        return None


def _valor(dados: Mapping[str, Any], chave: str) -> str:
    return normalizar_valor(dados.get(chave))


# ---------------------------------------------------------------------- pessoas
@dataclass(frozen=True)
class Pessoa:
    """Agrupa as chaves dos campos de uma pessoa (filiação ou responsável)."""

    descricao: str  # "Filiação 1", "Responsável alternativo"...
    nome: str
    dn: str
    cpf: str
    falecido: str | None = None
    outros: tuple[str, ...] = ()  # demais campos da pessoa (título, UF, zona, profissão...)

    @classmethod
    def por_prefixo(
        cls,
        prefixo: str,
        descricao: str,
        *,
        falecido: str | None = None,
        sufixos_outros: tuple[str, ...] = ("titulo", "uf", "zona", "secao", "profissao"),
        extras: tuple[str, ...] = (),
    ) -> "Pessoa":
        """Monta a pessoa pela convenção de chaves `<prefixo>_nome`, `<prefixo>_dn`, `<prefixo>_cpf`..."""
        return cls(
            descricao=descricao,
            nome=f"{prefixo}_nome",
            dn=f"{prefixo}_dn",
            cpf=f"{prefixo}_cpf",
            falecido=falecido,
            outros=tuple(f"{prefixo}_{s}" for s in sufixos_outros) + tuple(extras),
        )

    @property
    def exigidas_para_estar_completa(self) -> tuple[str, ...]:
        return (self.nome, self.dn, self.cpf) + ((self.falecido,) if self.falecido else ())

    @property
    def dependentes_do_nome(self) -> tuple[str, ...]:
        return (self.dn, self.cpf) + ((self.falecido,) if self.falecido else ()) + self.outros

    @property
    def todas_as_chaves(self) -> tuple[str, ...]:
        return (self.nome,) + self.dependentes_do_nome


# ----------------------------------------------------------------------- regras
@dataclass(frozen=True)
class ExigeNome(RegraDeEsquema):
    """Nenhum dado de uma pessoa pode ser preenchido sem o nome dela.
    No navegador, os demais campos ficam desabilitados enquanto o nome está vazio."""

    pessoa: Pessoa

    def chaves(self):
        return self.pessoa.todas_as_chaves

    def verificar(self, esquema, dados):
        if _valor(dados, self.pessoa.nome):
            return []
        if not any(_valor(dados, k) for k in self.pessoa.dependentes_do_nome):
            return []
        return [Erro(self.pessoa.nome, f"Informe o nome de {self.pessoa.descricao} antes de preencher os demais dados dela.")]

    def para_js(self, esquema):
        return {"tipo": "exige_nome", "nome": self.pessoa.nome, "dependentes": list(self.pessoa.dependentes_do_nome)}


@dataclass(frozen=True)
class ComposicaoFamiliar(RegraDeEsquema):
    """Quem responde pelo estudante:

    - com responsável alternativo (nome preenchido): ele precisa estar completo; as filiações são opcionais;
    - sem responsável alternativo: ao menos uma filiação precisa estar completa e ao menos uma das
      filiações completas precisa estar viva (`valor_vivo` no campo falecido).
    Uma pessoa está "completa" quando todos os campos de `exigidas_para_estar_completa` estão preenchidos.
    """

    filiacoes: tuple[Pessoa, ...]
    responsavel: Pessoa
    valor_vivo: str = "Não"

    def chaves(self):
        return tuple(k for p in (*self.filiacoes, self.responsavel) for k in p.todas_as_chaves)

    def verificar(self, esquema, dados):
        responsavel = self.responsavel

        if _valor(dados, responsavel.nome):
            faltando = [k for k in responsavel.exigidas_para_estar_completa if not _valor(dados, k)]
            return [
                Erro(k, f"O campo {esquema.campo(k).rotulo} é obrigatório quando há responsável alternativo.")
                for k in faltando
            ]

        completas = [
            f for f in self.filiacoes if all(_valor(dados, k) for k in f.exigidas_para_estar_completa)
        ]
        if not completas:
            nomes = [f.nome for f in self.filiacoes] + [responsavel.nome]
            return [Erro(
                nomes[0],
                "Preencha por completo (nome, data de nascimento, falecido e CPF) ao menos uma das filiações, "
                "ou informe o responsável alternativo.",
                relacionadas=tuple(nomes[1:]),
            )]

        if not any(_valor(dados, f.falecido) == self.valor_vivo for f in completas):
            chaves = [f.falecido for f in completas]
            return [Erro(
                chaves[0],
                f"Sem responsável alternativo, ao menos uma das filiações completas precisa estar viva "
                f"(marque \"{self.valor_vivo}\" em falecido) — ou informe o responsável alternativo.",
                relacionadas=tuple(chaves[1:]),
            )]
        return []


@dataclass(frozen=True)
class CpfsDistintos(RegraDeEsquema):
    """O mesmo CPF não pode aparecer em dois campos."""

    campos: tuple[str, ...]

    def chaves(self):
        return self.campos

    def verificar(self, esquema, dados):
        por_cpf: dict[str, list[str]] = {}
        for chave in self.campos:
            digitos = só_dígitos(_valor(dados, chave))
            if len(digitos) == 11:
                por_cpf.setdefault(digitos, []).append(chave)

        erros = []
        for chaves in por_cpf.values():
            if len(chaves) > 1:
                rotulos = ", ".join(esquema.campo(k).rotulo for k in chaves)
                erros.append(Erro(chaves[0], f"O mesmo CPF foi informado em mais de um campo: {rotulos}.", tuple(chaves[1:])))
        return erros

    def para_js(self, esquema):
        return {
            "tipo": "cpfs_distintos",
            "chaves": list(self.campos),
            "rotulos": {k: esquema.campo(k).rotulo for k in self.campos},
        }


@dataclass(frozen=True)
class OrdemDeDatas(RegraDeEsquema):
    """A data `anterior` precisa ser estritamente anterior à data `posterior` (se ambas forem datas válidas).
    O erro é mostrado no campo `alvo`."""

    anterior: str
    posterior: str
    alvo: str
    mensagem: str

    def chaves(self):
        return (self.anterior, self.posterior, self.alvo)

    def verificar(self, esquema, dados):
        antes = analisar_data(_valor(dados, self.anterior))
        depois = analisar_data(_valor(dados, self.posterior))
        if antes and depois and not antes < depois:
            return [Erro(self.alvo, self.mensagem)]
        return []

    def para_js(self, esquema):
        return {
            "tipo": "ordem_datas",
            "anterior": self.anterior,
            "posterior": self.posterior,
            "alvo": self.alvo,
            "mensagem": self.mensagem,
        }
