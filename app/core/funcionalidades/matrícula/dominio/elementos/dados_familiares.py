from __future__ import annotations

from app.core.funcionalidades.matrícula.dominio.campos import Bloco, Campo, Dependencia, Linha
from app.core.funcionalidades.matrícula.dominio.elementos.alternativas import NUCLEO_FAMILIAR, NAO_SIM
from app.core.funcionalidades.matrícula.dominio.elementos.dados_pessoais import dn as dn_estudante
from app.core.funcionalidades.matrícula.dominio.regras import ComprimentoMaximo
from app.core.funcionalidades.matrícula.dominio.regras_esquema import ComposicaoFamiliar, ExigeNome, OrdemDeDatas, Pessoa
from app.core.funcionalidades.matrícula.dominio.tipos import TipoCampo, TipoDado


# As regras de obrigatoriedade entre filiação 1, filiação 2 e responsável alternativo estão em `regras_família`,
# no final deste módulo. Os cartões que separam cada pessoa dentro da seção são os `Bloco(...)` de `linhas_família`.

def linha_docs_responsável(prefixo: str, pessoa: str, rotulo_cpf: str | None = None) -> Linha:
    """CPF + título de eleitor (usado em Filiação 1, Filiação 2 e Responsável)."""
    cpf = Campo(
        chave=f"{prefixo}_cpf",
        rotulo=rotulo_cpf or f"CPF ({pessoa})",
        tipo_dado=TipoDado.CPF
    )

    título = Campo(f"{prefixo}_titulo", f"Título eleitoral ({pessoa})")
    uf_eleitoral = Campo(f"{prefixo}_uf", f"UF de votação ({pessoa})", regras=(ComprimentoMaximo(2),) )
    zona_eleitoral = Campo(f"{prefixo}_zona", f"Zona eleitoral ({pessoa})")
    seção_eleitoral = Campo(f"{prefixo}_secao", f"Seção eleitoral ({pessoa})")

    _linha_docs_responsável = Linha(proporcoes=(2, 2, 1, 1, 1), campos=(cpf, título, uf_eleitoral, zona_eleitoral, seção_eleitoral, ), )

    return _linha_docs_responsável


def linhas_filiação(numero: int, rotulo_nome: str, chave_falecido: str, rotulo_falecido: str) -> tuple[Linha, ...]:
    prefixo, pessoa = f"filiacao{numero}", f"Filiação {numero}"
    nome = Campo(
        chave=f"{prefixo}_nome",
        rotulo=rotulo_nome
    )
    dn_filiação = Campo(
        chave=f"{prefixo}_dn",
        rotulo=f"D.N. ({pessoa})",
        tipo_dado=TipoDado.NASCIMENTO
    )

    falecido = Campo(
        chave=chave_falecido,
        rotulo=rotulo_falecido,
        tipo=TipoCampo.RADIO,
        opcoes=NAO_SIM,
        marcador=chave_falecido,
    )
    profissão = Campo(f"{prefixo}_profissao", f"Profissão ({pessoa})")  #Desativado. Por hora não pretendo perguntar a profissão
    return (
        Linha(proporcoes=(3, 1, 1), campos=(nome, dn_filiação, falecido, ), ),
        linha_docs_responsável(prefixo, pessoa),
        Linha(proporcoes=(1,), campos=(profissão, ) ),  #Desativado. Por hora não pretendo perguntar a profissão  #reativei porque o jina quebra se não fornecer os valores das chaves de profissões que ele já está esperando.
    )


nome_responsável_alternativo = Campo(
    chave="responsavel_nome",
    rotulo="Responsável alternativo (caso não seja nem a mãe nem o pai)"
)
dn_responsável = Campo(
    chave="responsavel_dn",
    rotulo="Data de Nascimento (Responsável)",
    tipo_dado=TipoDado.NASCIMENTO
)
responsável_profissão  = Campo(
    chave="responsavel_profissao",
    rotulo="Profissão (Responsável)"
)
responsável_relação = Campo(
    chave="responsavel_relacao",
    rotulo="Tipo de vínculo (Madrasta, Tia, Irmã, Vó etc)"
)

núcleo_familiar = Campo(
    chave="nucleo_opcoes",
    rotulo="Quem mora com o(a) estudante",
    tipo=TipoCampo.MULTISELECT,
    opcoes=NUCLEO_FAMILIAR,
    marcador="nuc"
)
núcleo_outros = Campo(
    chave="nuc_outros_texto",
    rotulo='Especifique "Outros" no núcleo familiar',
    depende_de=Dependencia("nucleo_opcoes", "Outros")
)

linhas_filiação_1 = linhas_filiação(1, "Nome Filiação 1 (de preferência a mãe)", "filiacao1_falecida", "Falecida?")
linhas_filiação_2 = linhas_filiação(2, "Nome Filiação 2 (de preferência o pai)", "filiacao2_falecido", "Falecido?")


linha_responsável_alt_1 = Linha(proporcoes=(3, 1, 1), campos=(nome_responsável_alternativo, dn_responsável, responsável_relação, ))
linha_responsável_alt_2 = linha_docs_responsável("responsavel", "Responsável", rotulo_cpf="CPF do responsável")

# Para aumentar a fonte das opções do núcleo, use o parâmetro `fonte_opcoes` (ex.: fonte_opcoes="17px") em `núcleo_familiar`.
linha_núcleo_1 = Linha(proporcoes=(1,), campos=(núcleo_familiar,))
linha_núcleo_2 = Linha(proporcoes=(1,), campos=(núcleo_outros,))


linhas_família = (
    Bloco("Filiação 1", linhas_filiação_1),
    Bloco("Filiação 2", linhas_filiação_2),
    Bloco("Responsável alternativo", (linha_responsável_alt_1, linha_responsável_alt_2, )),
    Bloco("Núcleo familiar", (linha_núcleo_1, linha_núcleo_2, )),
)


# ---------------------------------------------------------------- regras entre campos
# As chaves seguem a convenção `<prefixo>_nome`, `<prefixo>_dn`, `<prefixo>_cpf`... usada nas funções acima.
pessoa_filiação_1 = Pessoa.por_prefixo("filiacao1", "Filiação 1", falecido="filiacao1_falecida")
pessoa_filiação_2 = Pessoa.por_prefixo("filiacao2", "Filiação 2", falecido="filiacao2_falecido")
pessoa_responsável = Pessoa.por_prefixo(
    "responsavel",
    "Responsável alternativo",
    sufixos_outros=("titulo", "uf", "zona", "secao"),  # a profissão do responsável não está no formulário
    extras=(responsável_relação.chave, ),
)

regras_família = (
    # Nenhum dado de uma pessoa pode ser preenchido sem o nome dela (em tempo real, os campos ficam desabilitados).
    ExigeNome(pessoa_filiação_1),
    ExigeNome(pessoa_filiação_2),
    ExigeNome(pessoa_responsável),

    # Com responsável alternativo: ele precisa estar completo. Sem ele: ao menos uma filiação completa e viva.
    ComposicaoFamiliar(filiacoes=(pessoa_filiação_1, pessoa_filiação_2), responsavel=pessoa_responsável),

    # Filiação e responsável precisam ter nascido antes do estudante.
    *(
        OrdemDeDatas(
            anterior=pessoa.dn,
            posterior=dn_estudante.chave,
            alvo=pessoa.dn,
            mensagem=f"A data de nascimento de {pessoa.descricao} deve ser anterior à data de nascimento do estudante.",
        )
        for pessoa in (pessoa_filiação_1, pessoa_filiação_2, pessoa_responsável)
    ),
)
