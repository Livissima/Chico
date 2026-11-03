"""Definição do formulário de matrícula (substitui elements/campos.py, linhas.py,
esqueleto.py e rótulos.py).

Para adicionar um campo: acrescente um `Campo(...)` na `Linha` desejada.
Se ele tiver `marcador`, a ficha impressa precisa usar as variáveis `<marcador>_<sufixo>`.
"""
from __future__ import annotations

from app.core.funcionalidades.matrícula.dominio.campos import Campo, Dependencia, Esquema, Linha, Seção
from app.core.funcionalidades.matrícula.dominio.definição.alternativas import ANO_LETIVO_PADRAO, NAO_SIM, \
    RESPONSAVEL_MATRICULA, NECESSIDADES, SUFIXOS_NEE
from app.core.funcionalidades.matrícula.dominio.definição.dados_familiares import nome_responsável, dn_responsável, \
    responsável_profissão, responsável_relação, núcleo_familiar, núcleo_outros
from app.core.funcionalidades.matrícula.dominio.definição.dados_pessoais import nome_social, cpf_estudante, \
    uf_naturalidade, município_naturalidade, termo_cn, livro_cn, folha_cn, data_emissão_cn, cartório_cn, município_cn, \
    etnia, religião, t_bermuda, t_camiseta, t_calça, t_jaqueta, t_tênis, nome_estudante, dn, gênero
from app.core.funcionalidades.matrícula.dominio.regras import ComprimentoMaximo
from app.core.funcionalidades.matrícula.dominio.tipos import TipoCampo, TipoDado

# ------------------------------------------------------------------ opções

# Nomes usados por pagina_print.html que não saem do slug da opção.


# ------------------------------------------------- blocos que se repetem
def _docs_responsáveis(prefixo: str, pessoa: str, rotulo_cpf: str | None = None) -> Linha:
    """CPF + título de eleitor (usado em Filiação 1, Filiação 2 e Responsável)."""
    cpf = Campo(f"{prefixo}_cpf", rotulo_cpf or f"CPF ({pessoa})", tipo_dado=TipoDado.CPF)
    título = Campo(f"{prefixo}_titulo", f"Título eleitoral ({pessoa})")
    uf_eleitoral = Campo(f"{prefixo}_uf", f"UF de votação ({pessoa})", regras=(ComprimentoMaximo(2),) )
    zona_eleitoral = Campo(f"{prefixo}_zona", f"Zona eleitoral ({pessoa})")
    seção_eleitoral = Campo(f"{prefixo}_secao", f"Seção eleitoral ({pessoa})")

    return Linha(proporcoes=(2, 2, 1, 1, 1), campos=(cpf, título, uf_eleitoral, zona_eleitoral, seção_eleitoral, ), )


def _filiação(numero: int, rotulo_nome: str, chave_falecido: str, rotulo_falecido: str) -> tuple[Linha, ...]:
    prefixo, pessoa = f"filiacao{numero}", f"Filiação {numero}"
    nome = Campo(f"{prefixo}_nome", rotulo_nome)
    dn_filiação = Campo(f"{prefixo}_dn", f"D.N. ({pessoa})")
    falecido = Campo(
        chave_falecido, rotulo_falecido, tipo=TipoCampo.RADIO, opcoes=NAO_SIM, valor_padrao="Não", marcador=chave_falecido,
    )
    profissão = Campo(f"{prefixo}_profissao", f"Profissão ({pessoa})")
    return (
        Linha(proporcoes=(3, 1, 1), campos=(nome, dn_filiação, falecido, ), ),
        _docs_responsáveis(prefixo, pessoa),
        Linha(proporcoes=(1,), campos=(profissão, ) ),
    )


# ------------------------------------------------------------------ seções

SECAO_DADOS_PESSOAIS = Seção(
    titulo="1. Dados Pessoais",
    linhas=(
        Linha(proporcoes=(3, 1, 1), campos=(nome_estudante, dn, gênero,)),
        Linha(proporcoes=(2, 2, 1), campos=(nome_social, cpf_estudante, uf_naturalidade,)),
        Linha(proporcoes=(2, 1, 1, 1), campos=(município_naturalidade, termo_cn, livro_cn, folha_cn,)),
        Linha(proporcoes=(1, 2, 2), campos=(data_emissão_cn, cartório_cn, município_cn,)),
        Linha(proporcoes=(1, 1), campos=(etnia, religião,)),
        Linha(proporcoes=(1, 1, 1, 1, 1), campos=(t_bermuda, t_camiseta, t_calça, t_jaqueta, t_tênis,)),
    ),
)

SECAO_DADOS_FAMILIARES = Seção(
    titulo="2. Dados Familiares",
    linhas=(
        *_filiação(1, "Nome Filiação 1 (de preferência a mãe)", "filiacao1_falecida", "Falecida?"),
        *_filiação(2, "Nome Filiação 2 (de preferência o pai)", "filiacao2_falecido", "Falecido?"),
        # --- Responsável legal
        Linha(proporcoes=(3, 1), campos=(nome_responsável, dn_responsável,)),
        _docs_responsáveis("responsavel", "Responsável", rotulo_cpf="CPF do responsável"),
        Linha(proporcoes=(2, 2), campos=(responsável_profissão, responsável_relação,)),
        # --- Núcleo familiar
        Linha(proporcoes=(1,), campos=(núcleo_familiar,)),
        Linha(proporcoes=(1,), campos=(núcleo_outros,)),
    ),
)
logradouro = Campo("logradouro", "Logradouro")
quadra = Campo("quadra", "Quadra")
lote = Campo("lote", "Lote")
número = Campo("numero", "Número")
cep = Campo("cep", "CEP")
complemento = Campo("complemento", "Complemento")
bairro = Campo("bairro", "Bairro")
município = Campo("municipio", "Município")
cel_mãe = Campo("celular_mae", "Celular da Mãe")
cel_pai = Campo("celular_pai", "Celular do Pai")
cel_ctt = Campo("fone_contato", "Telefone p/ Contato")
cel_fixo = Campo("telefone_fixo", "Telefone Fixo")
email = Campo("email_contato", "Email p/ contato")
uc_equatorial = Campo("uc_equatorial", "UC (Equatorial)")
cad_único = Campo("cadunico", "CadÚnico")
irmãos = Campo("irmaos_ue", "Irmão(s) Nesta Escola")

SECAO_ENDERECO_CONTATO = Seção(
    titulo="3. Endereço e Contato",
    linhas=(
        Linha(proporcoes=(3, 1, 1, 1, 2), campos=(logradouro, quadra, lote, número, cep, )),
        Linha(proporcoes=(2, 2, 2), campos=(complemento, bairro, município, )),
        Linha(proporcoes=(1, 1, 1, 1), campos=(cel_mãe, cel_pai, cel_ctt, cel_fixo, )),
        Linha(proporcoes=(2, 2, 1), campos=(email, uc_equatorial, cad_único, )),
        Linha(proporcoes=(1,), campos=(irmãos,)),
    ),
)
possui_nee = Campo(
    "possui_nee", "Possui Necessidade Educacional Especial?", tipo=TipoCampo.RADIO, opcoes=NAO_SIM, valor_padrao="Não", marcador="nee"
)
nee_opções = Campo(
    "nee_opcoes", "Selecione as opções de NEE:", tipo=TipoCampo.MULTISELECT, opcoes=NECESSIDADES, marcador="nee",
    sufixos_marcador=SUFIXOS_NEE, depende_de=Dependencia("possui_nee", "Sim")
)
nee_outros = Campo(
    "nee_outro_texto", "Especifique a NEE (Outro):", depende_de=Dependencia("nee_opcoes", "Outro")
)
restrição_alimentar = Campo("restricao_alimentar", "Restrição alimentar (se houver):")

SECAO_NEE = Seção(
    titulo="4. Necessidade Educacional Especial (NEE)",
    linhas=(
        Linha(proporcoes=(1,), campos=(possui_nee, ) ),
        Linha(proporcoes=(1,), campos=(nee_opções, ) ),
        Linha(proporcoes=(1,), campos=(nee_outros, ) ),
        Linha(proporcoes=(1,), campos=(restrição_alimentar, ) ),
    ),
)
ano_letivo = Campo("ano_letivo", "Ano Letivo", valor_padrao=ANO_LETIVO_PADRAO)
curso = Campo("curso", "Curso", valor_padrao="Ensino Fundamental")
série = Campo("ano_serie", "Ano/Série")
turma = Campo("turma", "Turma")
num_matrícula = Campo("num_matricula", "Nº Matrícula (aluno da rede)")
data_matrícula = Campo("data_matricula", "Data Matrícula (dd/mm/aaaa)")
responsável_matrícula = Campo(
    "resp_mat_opcao", "Responsável pela matrícula", tipo=TipoCampo.SELECT, opcoes=RESPONSAVEL_MATRICULA, marcador="resp_mat"
)
responsável_matrícula_outro = Campo(
    "resp_mat_outro_texto", "Especifique o responsável pela matrícula:", depende_de=Dependencia("resp_mat_opcao", "Outro")
)
preenchedora = Campo("preenchido_por", "Ficha preenchida por:", valor_padrao="Secretaria Escolar")
logo_url = Campo("logo_src", "URL da Logo (opcional):")

SECAO_DADOS_ESCOLARES = Seção(
    titulo="5. Dados Escolares e Matrícula",
    linhas=(
        Linha(proporcoes=(1, 2, 1, 1), campos=(ano_letivo, curso, série, turma, ) ),
        Linha(proporcoes=(2, 1, 2), campos=(num_matrícula, data_matrícula, responsável_matrícula, ) ),
        Linha(proporcoes=(1,), campos=(responsável_matrícula_outro, ) ),
        Linha(proporcoes=(1, 1), campos=(preenchedora, logo_url, ) ),
    ),
)

ESQUEMA = Esquema(
    secoes=(
        SECAO_DADOS_PESSOAIS,
        SECAO_DADOS_FAMILIARES,
        SECAO_ENDERECO_CONTATO,
        SECAO_NEE,
        SECAO_DADOS_ESCOLARES,
    )
)
