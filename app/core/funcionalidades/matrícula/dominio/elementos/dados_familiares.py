from __future__ import annotations

from app.core.funcionalidades.matrícula.dominio.campos import Campo, Dependencia, Linha
from app.core.funcionalidades.matrícula.dominio.elementos.alternativas import NUCLEO_FAMILIAR, NAO_SIM
from app.core.funcionalidades.matrícula.dominio.regras import ComprimentoMaximo
from app.core.funcionalidades.matrícula.dominio.tipos import TipoCampo, TipoDado


# todo: Aqui neste módulo eu preciso criar uma lógica para obrigatoriedade de preenchimento dos campos de filiação e/ou responsável alternativo, mas de uma forma dinâmica. Seguem as condições abaixo:
#  Os dados de ao menos uma das três pessoas deve ser preenchido (filiação1, filiação2 e responsável alternativo).
#  Se o nome do responsável alternativo for preenchido, o nome e os dados da filiação 1 e filiação 2 são opcionais. Deve também ser possível escrever opcionalmente os nomes da filiação 1 e 2, sem precisar preencher os demais dados das respectivbas pessoas.
#  Se o nome do responsável alternativo for preenchido, os dados de DN, falecido e CPF são obrigatórios para o responsável alternativo.
#  Se não tem responsável alternativo preenchido, deve-se preencher ao menos uma das duas pessoas (filiação1 e filiação2) por completo (nome, dn, falecido e cpf)
#  Se eu preenchi por completo uma das pessoas filiação1 ou filiação2, eu posso inserir o nome da outra pessoa sem preencher os dados dela. (ex: filiação 1 com dados completos, filiação 2 só nome)
#  Se eu preencho os dados da filiação1 ou filiação2 e deixar o responsável alternativo em branco, ao menos uma das filiações preenchidas deve conter o valor 'Não' no campo de falecida
#  Para preencher os dados de DN, CPF, falecido e CPF para uma das 3 pessoas, eu preciso obrigatoriamente informar o nome dela.
#  Um mesmo número de CPF não pode ser inserido em mais de um campo de CPF
#  As datas de nascimento inseridas em filiação_1, filiação_2 ou responsável alternativo nunca podem ser iguais ou posteriores à data de nascimento informada para o estudante.
#  Como as condições envolve o preenchimento de campos que podem vir antes ou depois, incluindo de diferentes SEÇÕES, essa verificação pode ser feita após o preenchimento completo, quando ordenarmos a geração do relatório para impressão. Caso haja erros de acordo com as condições acima, a página acusa os campos incorretos ou pendentes, de acordo com a condição. Em casos que a verificação instantânea for possível/viável, ela deve ser aplicada. A condição de não preencher os dados sem informar o CPF da pessoa, por exemplo, provavelmente pode ser feita em tempo real, ao vincular os campos relacionados a cada pessoa e verificar se o nome foi preenchido antes de preencher CPF, DN ou falecimento.

#todo: Bolar um esqueminha para dar uma separada em elementos de uma mesma seção para facilitar visualização, facilitando distinguir os campos da filiação1, filiação2 e responsável sem misturar.

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
        tipo_dado=TipoDado.DATA
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
    tipo_dado=TipoDado.DATA
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

#todo: Será possível aumentar o tamanho da fonte das opções do núcleo?
linha_núcleo_1 = Linha(proporcoes=(1,), campos=(núcleo_familiar,))
linha_núcleo_2 = Linha(proporcoes=(1,), campos=(núcleo_outros,))


linhas_família = (
    *linhas_filiação_1,
    *linhas_filiação_2,

    linha_responsável_alt_1,
    linha_responsável_alt_2,

    linha_núcleo_1,
    linha_núcleo_2,
)
