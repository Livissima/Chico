"""Modelo do formulário: Campo, Linha, Bloco, Seção e Esquema.

Tudo aqui é dado puro + comportamento do próprio dado. Não há Streamlit nem Jinja.
Identificadores e chaves são ASCII; acentos só aparecem em rótulos e opções.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Any, Callable, Iterator, Mapping

from .formatos import formato_de
from .regras import Erro, Obrigatorio, Regra, regra_para
from .regras_esquema import RegraDeEsquema
from .texto import é_coleção, normalizar_valor, slug
from .tipos import TipoCampo, TipoDado

_CHAVE_VALIDA = re.compile(r"[a-z][a-z0-9_]*")
_TAMANHO_FONTE_VALIDO = re.compile(r"\d+(\.\d+)?(px|pt|em|rem|%)")
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
    # Texto, ou função sem argumentos que devolve o texto (ex.: `hoje`, chamada a cada carregamento do formulário).
    valor_padrao: str | Callable[[], str] = ""
    regras: tuple[Regra, ...] = ()
    depende_de: Dependencia | None = None
    # Prefixo das flags "X" usadas na ficha impressa (ex.: "cor" -> cor_branca, cor_preta...).
    marcador: str | None = None
    # Sufixo da flag quando não dá para derivá-lo da opção (ex.: "Masculino" -> "m").
    sufixos_marcador: Mapping[str, str] = field(default_factory=dict, compare=False, hash=False)
    # Campo bloqueado: aparece com o `valor_padrao`, não pode ser editado, e esse valor é o usado
    # no relatório (o servidor ignora qualquer valor diferente que chegue do navegador).
    bloqueado: bool = False
    # Tamanho da fonte das opções (select e multiselect), ex.: "17px" ou "1.1rem".
    fonte_opcoes: str | None = None

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
        if self.bloqueado and self.tipo is TipoCampo.MULTISELECT:
            raise ValueError(f"Campo {self.chave!r}: multiselect não pode ser bloqueado.")
        if self.bloqueado and not self.valor_padrao:
            raise ValueError(f"Campo {self.chave!r} está bloqueado, então precisa de um valor_padrao.")
        if self.fonte_opcoes and not _TAMANHO_FONTE_VALIDO.fullmatch(self.fonte_opcoes):
            raise ValueError(f"Campo {self.chave!r}: fonte_opcoes inválida {self.fonte_opcoes!r} (use algo como '17px').")
        if self.tipo in (TipoCampo.SELECT, TipoCampo.RADIO) and isinstance(self.valor_padrao, str):
            if self.valor_padrao and self.valor_padrao not in self.opcoes:
                raise ValueError(f"Campo {self.chave!r}: valor_padrao {self.valor_padrao!r} não está nas opções.")

    # ---------------------------------------------------------------- valor
    @property
    def valor_inicial(self) -> str:
        """Valor padrão já resolvido (chama a função, se `valor_padrao` for uma função)."""
        return self.valor_padrao() if callable(self.valor_padrao) else self.valor_padrao

    @property
    def obrigatorio(self) -> bool:
        return any(isinstance(r, Obrigatorio) for r in self.regras)

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

    # ------------------------------------------------------------ formatação
    def formatar_formulario(self, valor: Any) -> Any:
        """Valor como fica no campo do formulário (ex.: telefone completo e com máscara)."""
        if é_coleção(valor):
            return [str(v) for v in valor]
        return formato_de(self.tipo_dado).formulario(normalizar_valor(valor))

    def para_ficha(self, valor: Any) -> Any:
        if é_coleção(valor):
            return [str(v) for v in valor]
        return formato_de(self.tipo_dado).ficha(normalizar_valor(valor))

    def para_json(self, valor: Any) -> Any:
        if self.tipo is TipoCampo.MULTISELECT:
            return [str(v) for v in valor] if é_coleção(valor) else []
        return formato_de(self.tipo_dado).json(normalizar_valor(valor))

    # ------------------------------------------------------------ apresentação
    def atributos_html(self) -> dict[str, str]:
        """Atributos do <input> de texto (máscaras, limites e placeholder lidos pelo JS)."""
        atributos = {"data-tipo": self.tipo_dado.tipo_js}
        if self.tipo_dado.placeholder:
            atributos["placeholder"] = self.tipo_dado.placeholder
        if self.tipo_dado.mostra_idade:
            atributos["data-idade"] = "true"
        for regra in self.regras:
            atributos.update(regra.atributos_html())
        return atributos

    def atributos_comuns(self) -> dict[str, str]:
        """Atributos de qualquer controle (input, select ou grupo de checkboxes)."""
        atributos = {}
        if self.obrigatorio:
            atributos["data-obrigatorio"] = "true"
        if self.bloqueado:
            atributos["data-bloqueado"] = "true"
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
class Bloco:
    """Grupo de linhas dentro de uma seção, desenhado como um "cartão" com título
    (ex.: Filiação 1, Filiação 2, Responsável alternativo)."""

    titulo: str
    linhas: tuple[Linha, ...]


@dataclass(frozen=True)
class Seção:
    titulo: str
    # Aceita Linhas soltas e Blocos misturados; as soltas ficam fora de qualquer cartão.
    linhas: tuple[Linha | Bloco, ...]

    def blocos(self) -> list[Bloco]:
        """Blocos da seção; linhas soltas consecutivas formam um bloco sem título."""
        resultado: list[Bloco] = []
        soltas: list[Linha] = []
        for item in self.linhas:
            if isinstance(item, Bloco):
                if soltas:
                    resultado.append(Bloco("", tuple(soltas)))
                    soltas = []
                resultado.append(item)
            else:
                soltas.append(item)
        if soltas:
            resultado.append(Bloco("", tuple(soltas)))
        return resultado

    def todas_as_linhas(self) -> Iterator[Linha]:
        for bloco in self.blocos():
            yield from bloco.linhas


@dataclass(frozen=True)
class Esquema:
    secoes: tuple[Seção, ...]
    regras: tuple[RegraDeEsquema, ...] = ()

    def __post_init__(self) -> None:
        posicao: dict[str, int] = {}
        for i, campo in enumerate(self.campos()):
            if campo.chave in posicao:
                raise ValueError(f"Chave de campo duplicada: {campo.chave!r}")
            posicao[campo.chave] = i
        for campo in self.campos():
            if campo.depende_de is None:
                continue
            pai = campo.depende_de.chave
            if pai not in posicao:
                raise ValueError(f"Campo {campo.chave!r} depende de {pai!r}, que não existe.")
            if posicao[pai] > posicao[campo.chave]:
                raise ValueError(f"Campo {campo.chave!r} depende de {pai!r}, que precisa vir antes dele no formulário.")
        for regra in self.regras:
            inexistentes = [k for k in regra.chaves() if k not in posicao]
            if inexistentes:
                raise ValueError(f"{type(regra).__name__} usa chaves que não existem no esquema: {inexistentes}")

    # ---------------------------------------------------------------- consulta
    def campos(self) -> Iterator[Campo]:
        for secao in self.secoes:
            for linha in secao.todas_as_linhas():
                yield from linha.campos

    def campo(self, chave: str) -> Campo:
        for campo in self.campos():
            if campo.chave == chave:
                return campo
        raise KeyError(chave)

    def campos_ativos(self, dados: Mapping[str, Any]) -> list[Campo]:
        """Campos visíveis para estes dados (o formulário não envia os campos ocultos)."""
        return [c for c in self.campos() if c.depende_de is None or c.depende_de.satisfeita(dados)]

    @property
    def regras_js(self) -> list[dict[str, Any]]:
        """Descrição das regras entre campos que o navegador também sabe aplicar."""
        descricoes = (regra.para_js(self) for regra in self.regras)
        return [d for d in descricoes if d is not None]

    # ------------------------------------------------------------- preparação
    def preparar(self, dados: Mapping[str, Any]) -> dict[str, Any]:
        """Dados do navegador -> dados confiáveis para validar, gerar a ficha e o JSON.

        - descarta chaves que não são campos (ex.: `_envio`) e campos ocultos por dependência;
        - campos bloqueados recebem sempre o valor padrão;
        - aplica a formatação do formulário (ex.: telefone completado com DDD e 9 extra).
        É idempotente: preparar dados já preparados não muda nada.
        """
        preparados: dict[str, Any] = {}
        for campo in self.campos():
            if campo.depende_de is not None and not campo.depende_de.satisfeita(preparados):
                continue
            if campo.bloqueado:
                preparados[campo.chave] = campo.valor_inicial
            elif campo.chave in dados:
                preparados[campo.chave] = campo.formatar_formulario(dados[campo.chave])
        return preparados

    # --------------------------------------------------------------- validação
    def validar(self, dados: Mapping[str, Any]) -> list[Erro]:
        preparados = self.preparar(dados)
        erros = [
            Erro(campo.chave, mensagem)
            for campo in self.campos_ativos(preparados)
            if (mensagem := campo.validar(preparados.get(campo.chave)))
        ]
        for regra in self.regras:
            erros.extend(regra.verificar(self, preparados))
        return erros
