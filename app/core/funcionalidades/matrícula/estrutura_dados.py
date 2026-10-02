from schemas import SeçãoFormulário, LinhaFormulário, CampoSchema
from rótulos import *

# ==========================================
# 1. DADOS PESSOAIS
# ==========================================
SECAO_DADOS_PESSOAIS = SeçãoFormulário(
    título="1. Dados Pessoais",
    linhas=[LinhaFormulário(
        proporções=[3, 1, 1],
    campos=[CampoSchema(chave="nome_estudante", rótulo=NOME_ESTUDANTE, obrigatório=True, cumprimento_mínimo=3),
        CampoSchema(chave="data_nascimento", rótulo=DATA_NASCIMENTO, obrigatório=True, tipo_dado="date"),
        CampoSchema(chave="genero", rótulo=GÊNERO, tipo="select", opções=["", "Masculino", "Feminino"]), ]),
    LinhaFormulário(proporções=[2, 2, 1], campos=[CampoSchema(chave="nome_social", rótulo=NOME_SOCIAL),
        CampoSchema(chave="cpf_estudante", rótulo=CPF_ESTUDANTE, tipo_dado="cpf", cumprimento_máximo=14),
        CampoSchema(chave="uf_naturalidade", rótulo=UF_NATURALIDADE, cumprimento_máximo=2), ]),
    LinhaFormulário(proporções=[2, 1, 1, 1],
        campos=[CampoSchema(chave="municipio_naturalidade", rótulo=MUNICÍPIO_NATURALIDADE),
            CampoSchema(chave="termo_cert_nasc", rótulo=TERMO_CN), CampoSchema(chave="livro", rótulo=LIVRO_CN),
            CampoSchema(chave="folha", rótulo=FOLHA), ]), LinhaFormulário(proporções=[1, 2, 2],
        campos=[CampoSchema(chave="dt_emissao_cn", rótulo=DATA_EMISSÃO_CN, tipo_dado="date"),
            CampoSchema(chave="cartorio_registro", rótulo=CARTÓRIO_REGISTRO),
            CampoSchema(chave="municipio_registro", rótulo=MUNICÍPIO_REGISTRO), ]), LinhaFormulário(proporções=[1, 1],
        campos=[CampoSchema(chave="cor_etnia", rótulo=ETNIA, tipo="select",
                            opções=["", "Branca", "Preta", "Parda", "Indígena", "Amarela", "Não declarada"]),
            CampoSchema(chave="religiao", rótulo=RELIGIÃO, tipo="select",
                        opções=["", "Budismo", "Catolicismo", "Evangelismo", "Congregação", "Espírita",
                                "Sem religião"]), ]), # Tamanhos de Uniforme
    LinhaFormulário(proporções=[1, 1, 1, 1, 1],
        campos=[CampoSchema(chave="tam_bermuda", rótulo=BERMUDA), CampoSchema(chave="tam_camiseta", rótulo=CAMISETA),
            CampoSchema(chave="tam_calca", rótulo=CALÇA), CampoSchema(chave="tam_jaqueta", rótulo=JAQUETA),
            CampoSchema(chave="tam_tenis", rótulo=TÊNIS), ])])

# ==========================================
# 2. DADOS FAMILIARES
# ==========================================
SECAO_DADOS_FAMILIARES = SeçãoFormulário(título="2. Dados Familiares", linhas=[# --- Filiação 1 ---
    LinhaFormulário(proporções=[3, 1, 1], campos=[CampoSchema(chave="filiacao1_nome", rótulo=FILIAÇÃO1_NOME),
        CampoSchema(chave="filiacao1_dn", rótulo=FILIAÇÃO1_DN),
        CampoSchema(chave="filiacao1_falecida", rótulo=FILIAÇÃO1_FALECIDA, tipo="radio", opções=["Não", "Sim"],
                    valor_padrão="Não"), ]), LinhaFormulário(proporções=[2, 2, 1, 1, 1],
        campos=[CampoSchema(chave="filiacao1_cpf", rótulo=FILIAÇÃO1_CPF, tipo_dado="cpf"),
            CampoSchema(chave="filiacao1_título", rótulo=FILIAÇÃO1_TÍTULO),
            CampoSchema(chave="filiacao1_uf", rótulo=FILIAÇÃO1_UF_ELEITORAL, cumprimento_máximo=2),
            CampoSchema(chave="filiacao1_zona", rótulo=FILIAÇÃO1_ZONA),
            CampoSchema(chave="filiacao1_secao", rótulo=FILIAÇÃO1_SEÇÃO), ]),
    LinhaFormulário(proporções=[1], campos=[CampoSchema(chave="filiacao1_profissao", rótulo=FILIAÇÃO1_PROFISSÃO)]),

    # --- Filiação 2 ---
    LinhaFormulário(proporções=[3, 1, 1], campos=[CampoSchema(chave="filiacao2_nome", rótulo=FILIAÇÃO2_NOME),
        CampoSchema(chave="filiacao2_dn", rótulo=FILIAÇÃO2_DN),
        CampoSchema(chave="filiacao2_falecido", rótulo=FILIAÇÃO2_FALECIDA, tipo="radio", opções=["Não", "Sim"],
                    valor_padrão="Não"), ]), LinhaFormulário(proporções=[2, 2, 1, 1, 1],
        campos=[CampoSchema(chave="filiacao2_cpf", rótulo=FILIAÇÃO2_CPF, tipo_dado="cpf"),
            CampoSchema(chave="filiacao2_título", rótulo=FILIAÇÃO2_TÍTULO),
            CampoSchema(chave="filiacao2_uf", rótulo=FILIAÇÃO2_UF_ELEITORAL, cumprimento_máximo=2),
            CampoSchema(chave="filiacao2_zona", rótulo=FILIAÇÃO2_ZONA),
            CampoSchema(chave="filiacao2_secao", rótulo=FILIAÇÃO2_SEÇÃO), ]),
    LinhaFormulário(proporções=[1], campos=[CampoSchema(chave="filiacao2_profissao", rótulo=FILIAÇÃO2_PROFISSÃO)]),

    # --- Responsável Legal ---
    LinhaFormulário(proporções=[3, 1], campos=[CampoSchema(chave="responsavel_nome", rótulo=RESPONSÁVEL_NOME),
        CampoSchema(chave="responsavel_dn", rótulo=RESPONSÁVEL_DN), ]), LinhaFormulário(proporções=[2, 2, 1, 1, 1],
        campos=[CampoSchema(chave="responsavel_cpf", rótulo=RESPONSÁVEL_CPF, tipo_dado="cpf"),
            CampoSchema(chave="responsavel_título", rótulo=RESPONSÁVEL_TÍTULO),
            CampoSchema(chave="responsavel_uf", rótulo=RESPONSÁVEL_UF, cumprimento_máximo=2),
            CampoSchema(chave="responsavel_zona", rótulo=RESPONSÁVEL_ZONA),
            CampoSchema(chave="responsavel_secao", rótulo=RESPONSÁVEL_SEÇÃO), ]), LinhaFormulário(proporções=[2, 2],
        campos=[CampoSchema(chave="responsavel_profissao", rótulo=RESPONSÁVEL_PROFISSÃO),
            CampoSchema(chave="responsavel_relacao", rótulo=RESPONSÁVEL_VÍNCULO), ]),

    # --- Núcleo Familiar ---
    LinhaFormulário(proporções=[1], campos=[CampoSchema(chave="nucleo_opções", rótulo=NÚCLEO_OPÇÕES, tipo="multiselect",
        opções=["Mãe", "Pai", "Irmãos", "Madrasta", "Tutor Legal", "Tios", "Avós", "Primos", "Padrasto", "Outros"])]),
    LinhaFormulário(proporções=[1], campos=[CampoSchema(chave="nuc_outros_texto", rótulo=NÚCLEO_OUTROS_INPUT)])])

# ==========================================
# 3. ENDEREÇO E CONTATO
# ==========================================
SECAO_ENDERECO_CONTATO = SeçãoFormulário(título="3. Endereço e Contato", linhas=[
    LinhaFormulário(proporções=[3, 1, 1, 1, 2],
        campos=[CampoSchema(chave="logradouro", rótulo=LOGRADOURO), CampoSchema(chave="quadra", rótulo=QUADRA),
            CampoSchema(chave="lote", rótulo=LOTE), CampoSchema(chave="numero", rótulo=NÚMERO),
            CampoSchema(chave="cep", rótulo=CEP), ]), LinhaFormulário(proporções=[2, 2, 2],
        campos=[CampoSchema(chave="complemento", rótulo=COMPLEMENTO), CampoSchema(chave="bairro", rótulo=BAIRRO),
            CampoSchema(chave="municipio", rótulo=MUNICÍPIO), ]), LinhaFormulário(proporções=[1, 1, 1, 1],
        campos=[CampoSchema(chave="celular_mae", rótulo=TELEFONE_MÃE),
            CampoSchema(chave="celular_pai", rótulo=TELEFONE_PAI),
            CampoSchema(chave="fone_contato", rótulo=TELEFONE_CONTATO),
            CampoSchema(chave="telefone_fixo", rótulo=TELEFONE_FIXO), ]), LinhaFormulário(proporções=[2, 2, 1],
        campos=[CampoSchema(chave="email_contato", rótulo=EMAIL_CONTATO),
            CampoSchema(chave="uc_equatorial", rótulo=UNIDADE_CONSUMIDORA),
            CampoSchema(chave="cadunico", rótulo=CAD_ÚNICO), ]),
    LinhaFormulário(proporções=[1], campos=[CampoSchema(chave="irmaos_ue", rótulo=IRMÃOS)])])

# ==========================================
# 4. NECESSIDADE EDUCACIONAL ESPECIAL (NEE)
# ==========================================
SECAO_NEE = SeçãoFormulário(título="4. Necessidade Educacional Especial (NEE)", linhas=[LinhaFormulário(proporções=[1],
    campos=[CampoSchema(chave="possui_nee", rótulo="Possui Necessidade Educacional Especial?", tipo="radio",
                        opções=["Não", "Sim"], valor_padrão="Não"), ]), LinhaFormulário(proporções=[1], campos=[
    CampoSchema(chave="nee_opções", rótulo="Selecione as opções de NEE:", tipo="multiselect",
        opções=["Dislexia", "Baixa Visão", "Deficiência Auditiva", "Transtorno do Espectro Autista", "Surdo cegueira",
            "Dislalia", "Cegueira", "TDAH", "Altas Habilidades/Superdotação", "Deficiência Intelectual", "Disgrafia",
            "Síndrome de Rett", "Surdez", "Distúrbios de Aprendizagem", "Deficiência Física", "Discalculia",
            "Síndrome de Asperger", "Deficiência Múltipla", "Transtorno Desintegrativo da Infância", "Outro"])]),
    LinhaFormulário(proporções=[1], campos=[CampoSchema(chave="nee_outro_texto", rótulo="Especifique a NEE (Outro):")]),
    LinhaFormulário(proporções=[1],
        campos=[CampoSchema(chave="restricao_alimentar", rótulo="Restrição alimentar (se houver):")])])

# ==========================================
# 5. DADOS ESCOLARES E MATRÍCULA
# ==========================================
SECAO_DADOS_ESCOLARES = SeçãoFormulário(título="5. Dados Escolares e Matrícula", linhas=[
    LinhaFormulário(proporções=[1, 2, 1, 1],
        campos=[CampoSchema(chave="ano_letivo", rótulo=ANO_LETIVO, valor_padrão="2026"),
            CampoSchema(chave="curso", rótulo=CURSO, valor_padrão="Ensino Fundamental"),
            CampoSchema(chave="ano_serie", rótulo=ANO_SÉRIE), CampoSchema(chave="turma", rótulo=TURMA), ]),
    LinhaFormulário(proporções=[2, 1, 2], campos=[CampoSchema(chave="num_matricula", rótulo=NUM_MATRÍCULA),
        CampoSchema(chave="data_matricula", rótulo=DATA_MATRÍCULA),
        CampoSchema(chave="resp_mat_opcao", rótulo=RESPONSÁVEL_MATRÍCULA, tipo="select",
                    opções=["Mãe", "Pai", "Outro"]), ]), LinhaFormulário(proporções=[1],
        campos=[CampoSchema(chave="resp_mat_outro_texto", rótulo=RESPONSÁVEL_MATRÍCULA_OUTRO)]),
    LinhaFormulário(proporções=[1, 1],
        campos=[CampoSchema(chave="preenchido_por", rótulo=PREENCHEDOR_MATRÍCULA, valor_padrão="Secretaria Escolar"),
            CampoSchema(chave="logo_src", rótulo="URL da Logo (opcional):", valor_padrão=""), ])])

# ==========================================
# EXPORTAÇÃO FINAL
# ==========================================
TODAS_AS_SECOES = [SECAO_DADOS_PESSOAIS, SECAO_DADOS_FAMILIARES, SECAO_ENDERECO_CONTATO, SECAO_NEE, SECAO_DADOS_ESCOLARES]