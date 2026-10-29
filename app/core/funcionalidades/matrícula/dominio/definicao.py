"""Definição do formulário de matrícula (substitui elements/campos.py, linhas.py,
esqueleto.py e rótulos.py).

Para adicionar um campo: acrescente um `Campo(...)` na `Linha` desejada.
Se ele tiver `marcador`, a ficha impressa precisa usar as variáveis `<marcador>_<sufixo>`.
"""
from __future__ import annotations

from .campos import Campo, Dependencia, Esquema, Linha, Seção
from .regras import ApenasLetras, ComprimentoMaximo, ComprimentoMinimo, Obrigatorio
from .tipos import TipoCampo, TipoDado

# ------------------------------------------------------------------ opções
ANO_LETIVO_PADRAO = "2026"

NAO_SIM = ("Não", "Sim")
GENEROS = ("Masculino", "Feminino")
ETNIAS = ("", "Branca", "Preta", "Parda", "Indígena", "Amarela", "Não declarada")
RELIGIOES = ("", "Budismo", "Catolicismo", "Evangelismo", "Congregação", "Espírita", "Sem religião")
NUCLEO_FAMILIAR = (
    "Mãe", "Pai", "Irmãos", "Madrasta", "Tutor Legal", "Tios", "Avós", "Primos", "Padrasto", "Outros",
)
RESPONSAVEL_MATRICULA = ("Mãe", "Pai", "Outro")
NECESSIDADES = (
    "Dislexia", "Baixa Visão", "Deficiência Auditiva", "Transtorno do Espectro Autista", "Surdo cegueira",
    "Dislalia", "Cegueira", "TDAH", "Altas Habilidades/Superdotação", "Deficiência Intelectual", "Disgrafia",
    "Síndrome de Rett", "Surdez", "Distúrbios de Aprendizagem", "Deficiência Física", "Discalculia",
    "Síndrome de Asperger", "Deficiência Múltipla", "Transtorno Desintegrativo da Infância", "Outro",
)
# Nomes usados por pagina_print.html que não saem do slug da opção.
SUFIXOS_NEE = {
    "Deficiência Auditiva": "def_auditiva",
    "Transtorno do Espectro Autista": "tea",
    "Altas Habilidades/Superdotação": "altas_habilidades",
    "Deficiência Intelectual": "def_intelectual",
    "Síndrome de Rett": "rett",
    "Distúrbios de Aprendizagem": "disturbios_aprendizagem",
    "Deficiência Física": "def_fisica",
    "Síndrome de Asperger": "asperger",
    "Deficiência Múltipla": "def_multipla",
    "Transtorno Desintegrativo da Infância": "desintegrativo",
}
UFS = (
    "AC", "AL", "AP", "AM", "BA", "CE", "DF", "ES", "GO",
    "MA", "MT", "MS", "MG", "PA", "PB", "PR", "PE", "PI",
    "RJ", "RN", "RS", "RO", "RR", "SC", "SP", "SE", "TO"
)

# ------------------------------------------------- blocos que se repetem
def _documentos(prefixo: str, pessoa: str, rotulo_cpf: str | None = None) -> Linha:
    """CPF + título de eleitor (usado em Filiação 1, Filiação 2 e Responsável)."""
    return Linha(
        proporcoes=(2, 2, 1, 1, 1),
        campos=(
            Campo(f"{prefixo}_cpf", rotulo_cpf or f"CPF ({pessoa})", tipo_dado=TipoDado.CPF),
            Campo(f"{prefixo}_titulo", f"Título eleitoral ({pessoa})"),
            Campo(f"{prefixo}_uf", f"UF de votação ({pessoa})", regras=(ComprimentoMaximo(2),)),
            Campo(f"{prefixo}_zona", f"Zona eleitoral ({pessoa})"),
            Campo(f"{prefixo}_secao", f"Seção eleitoral ({pessoa})"),
        ),
    )


def _filiacao(numero: int, rotulo_nome: str, chave_falecido: str, rotulo_falecido: str) -> tuple[Linha, ...]:
    prefixo, pessoa = f"filiacao{numero}", f"Filiação {numero}"
    return (
        Linha(
            proporcoes=(3, 1, 1),
            campos=(
                Campo(f"{prefixo}_nome", rotulo_nome),
                Campo(f"{prefixo}_dn", f"D.N. ({pessoa})"),
                Campo(
                    chave_falecido, rotulo_falecido,
                    tipo=TipoCampo.RADIO, opcoes=NAO_SIM, valor_padrao="Não", marcador=chave_falecido,
                ),
            ),
        ),
        _documentos(prefixo, pessoa),
        Linha(proporcoes=(1,), campos=(Campo(f"{prefixo}_profissao", f"Profissão ({pessoa})"),)),
    )


# ------------------------------------------------------------------ seções
SECAO_DADOS_PESSOAIS = Seção(
    titulo="1. Dados Pessoais",
    linhas=(
        Linha(proporcoes=(3, 1, 1), campos=(
            Campo("nome_estudante", "Nome do Estudante",
                  regras=(Obrigatorio(), ComprimentoMinimo(3), ApenasLetras())),
            Campo("data_nascimento", "Data de Nascimento (dd/mm/aaaa)",
                  tipo_dado=TipoDado.DATA, regras=(Obrigatorio(),)),
            Campo("genero", "Gênero", tipo=TipoCampo.SELECT, opcoes=GENEROS,
                  marcador="genero", sufixos_marcador={"Masculino": "m", "Feminino": "f"}),
        )),
        Linha(proporcoes=(2, 2, 1), campos=(
            Campo("nome_social", "Nome Social"),
            Campo("cpf_estudante", "CPF (Estudante)", tipo_dado=TipoDado.CPF, regras=(ComprimentoMaximo(14),)),
            Campo("uf_naturalidade", "UF de Nascimento",  regras=(ComprimentoMaximo(2), ApenasLetras() ), opcoes=UFS ),
        )),
        Linha(proporcoes=(2, 1, 1, 1), campos=(
            Campo("municipio_naturalidade", "Município de Nascimento"),
            Campo("termo_cert_nasc", "Termo Cert. Nasc."),
            Campo("livro", "Livro"),
            Campo("folha", "Folha"),
        )),
        Linha(proporcoes=(1, 2, 2), campos=(
            Campo("dt_emissao_cn", "Dt. Emissão (CN)", tipo_dado=TipoDado.DATA),
            Campo("cartorio_registro", "Cartório de Registro"),
            Campo("municipio_registro", "Município de Registro"),
        )),
        Linha(proporcoes=(1, 1), campos=(
            Campo("cor_etnia", "Cor/Etnia", tipo=TipoCampo.SELECT, opcoes=ETNIAS, marcador="cor"),
            Campo("religiao", "Religião", tipo=TipoCampo.SELECT, opcoes=RELIGIOES, marcador="rel"),
        )),
        Linha(proporcoes=(1, 1, 1, 1, 1), campos=(
            Campo("tam_bermuda", "Bermuda"),
            Campo("tam_camiseta", "Camiseta"),
            Campo("tam_calca", "Calça"),
            Campo("tam_jaqueta", "Jaqueta"),
            Campo("tam_tenis", "Tênis"),
        )),
    ),
)

SECAO_DADOS_FAMILIARES = Seção(
    titulo="2. Dados Familiares",
    linhas=(
        *_filiacao(1, "Nome Filiação 1 (de preferência a mãe)", "filiacao1_falecida", "Falecida?"),
        *_filiacao(2, "Nome Filiação 2 (de preferência o pai)", "filiacao2_falecido", "Falecido?"),
        # --- Responsável legal
        Linha(proporcoes=(3, 1), campos=(
            Campo("responsavel_nome", "Nome do responsável"),
            Campo("responsavel_dn", "Data de Nascimento (Responsável)"),
        )),
        _documentos("responsavel", "Responsável", rotulo_cpf="CPF do responsável"),
        Linha(proporcoes=(2, 2), campos=(
            Campo("responsavel_profissao", "Profissão (Responsável)"),
            Campo("responsavel_relacao", "Tipo de vínculo (mãe, pai, tutor legal etc)"),
        )),
        # --- Núcleo familiar
        Linha(proporcoes=(1,), campos=(
            Campo("nucleo_opcoes", "Quem mora com o(a) estudante", tipo=TipoCampo.MULTISELECT,
                  opcoes=NUCLEO_FAMILIAR, marcador="nuc"),
        )),
        Linha(proporcoes=(1,), campos=(
            Campo("nuc_outros_texto", 'Especifique "Outros" no núcleo familiar',
                  depende_de=Dependencia("nucleo_opcoes", "Outros")),
        )),
    ),
)

SECAO_ENDERECO_CONTATO = Seção(
    titulo="3. Endereço e Contato",
    linhas=(
        Linha(proporcoes=(3, 1, 1, 1, 2), campos=(
            Campo("logradouro", "Logradouro"),
            Campo("quadra", "Quadra"),
            Campo("lote", "Lote"),
            Campo("numero", "Número"),
            Campo("cep", "CEP"),
        )),
        Linha(proporcoes=(2, 2, 2), campos=(
            Campo("complemento", "Complemento"),
            Campo("bairro", "Bairro"),
            Campo("municipio", "Município"),
        )),
        Linha(proporcoes=(1, 1, 1, 1), campos=(
            Campo("celular_mae", "Celular da Mãe"),
            Campo("celular_pai", "Celular do Pai"),
            Campo("fone_contato", "Telefone p/ Contato"),
            Campo("telefone_fixo", "Telefone Fixo"),
        )),
        Linha(proporcoes=(2, 2, 1), campos=(
            Campo("email_contato", "Email p/ contato"),
            Campo("uc_equatorial", "UC (Equatorial)"),
            Campo("cadunico", "CadÚnico"),
        )),
        Linha(proporcoes=(1,), campos=(Campo("irmaos_ue", "Irmão(s) Nesta Escola"),)),
    ),
)

SECAO_NEE = Seção(
    titulo="4. Necessidade Educacional Especial (NEE)",
    linhas=(
        Linha(proporcoes=(1,), campos=(
            Campo("possui_nee", "Possui Necessidade Educacional Especial?", tipo=TipoCampo.RADIO,
                  opcoes=NAO_SIM, valor_padrao="Não", marcador="nee"),
        )),
        Linha(proporcoes=(1,), campos=(
            Campo("nee_opcoes", "Selecione as opções de NEE:", tipo=TipoCampo.MULTISELECT,
                  opcoes=NECESSIDADES, marcador="nee", sufixos_marcador=SUFIXOS_NEE,
                  depende_de=Dependencia("possui_nee", "Sim")),
        )),
        Linha(proporcoes=(1,), campos=(
            Campo("nee_outro_texto", "Especifique a NEE (Outro):",
                  depende_de=Dependencia("nee_opcoes", "Outro")),
        )),
        Linha(proporcoes=(1,), campos=(Campo("restricao_alimentar", "Restrição alimentar (se houver):"),)),
    ),
)

SECAO_DADOS_ESCOLARES = Seção(
    titulo="5. Dados Escolares e Matrícula",
    linhas=(
        Linha(proporcoes=(1, 2, 1, 1), campos=(
            Campo("ano_letivo", "Ano Letivo", valor_padrao=ANO_LETIVO_PADRAO),
            Campo("curso", "Curso", valor_padrao="Ensino Fundamental"),
            Campo("ano_serie", "Ano/Série"),
            Campo("turma", "Turma"),
        )),
        Linha(proporcoes=(2, 1, 2), campos=(
            Campo("num_matricula", "Nº Matrícula (aluno da rede)"),
            Campo("data_matricula", "Data Matrícula (dd/mm/aaaa)"),
            Campo("resp_mat_opcao", "Responsável pela matrícula", tipo=TipoCampo.SELECT,
                  opcoes=RESPONSAVEL_MATRICULA, marcador="resp_mat"),
        )),
        Linha(proporcoes=(1,), campos=(
            Campo("resp_mat_outro_texto", "Especifique o responsável pela matrícula:",
                  depende_de=Dependencia("resp_mat_opcao", "Outro")),
        )),
        Linha(proporcoes=(1, 1), campos=(
            Campo("preenchido_por", "Ficha preenchida por:", valor_padrao="Secretaria Escolar"),
            Campo("logo_src", "URL da Logo (opcional):"),
        )),
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
