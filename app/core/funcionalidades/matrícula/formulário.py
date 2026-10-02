from estrutura_de_dados.linhas import *
from estrutura_de_dados.estrutura import SeçãoFormulário, LinhaFormulário, Campo
from estrutura_de_dados.rótulos import *

# ==========================================
# 1. DADOS PESSOAIS
SECAO_DADOS_PESSOAIS = SeçãoFormulário(título="1. Dados Pessoais",
                                       linhas=[linha1, linha2, linha3, linha4, linha5, linha6])

# ==========================================
# 2. DADOS FAMILIARES
# ==========================================
SECAO_DADOS_FAMILIARES = SeçãoFormulário(título="2. Dados Familiares", linhas=[])

# ==========================================
# 3. ENDEREÇO E CONTATO
# ==========================================
SECAO_ENDERECO_CONTATO = SeçãoFormulário(título="3. Endereço e Contato", linhas=[
    LinhaFormulário(proporções=[3, 1, 1, 1, 2],
                    campos=[Campo(chave="logradouro", rótulo=LOGRADOURO), Campo(chave="quadra", rótulo=QUADRA),
                            Campo(chave="lote", rótulo=LOTE), Campo(chave="numero", rótulo=NÚMERO),
                            Campo(chave="cep", rótulo=CEP), ]), LinhaFormulário(proporções=[2, 2, 2], campos=[
        Campo(chave="complemento", rótulo=COMPLEMENTO), Campo(chave="bairro", rótulo=BAIRRO),
        Campo(chave="municipio", rótulo=MUNICÍPIO), ]), LinhaFormulário(proporções=[1, 1, 1, 1], campos=[
        Campo(chave="celular_mae", rótulo=TELEFONE_MÃE), Campo(chave="celular_pai", rótulo=TELEFONE_PAI),
        Campo(chave="fone_contato", rótulo=TELEFONE_CONTATO), Campo(chave="telefone_fixo", rótulo=TELEFONE_FIXO), ]),
    LinhaFormulário(proporções=[2, 2, 1], campos=[Campo(chave="email_contato", rótulo=EMAIL_CONTATO),
                                                  Campo(chave="uc_equatorial", rótulo=UNIDADE_CONSUMIDORA),
                                                  Campo(chave="cadunico", rótulo=CAD_ÚNICO), ]),
    LinhaFormulário(proporções=[1], campos=[Campo(chave="irmaos_ue", rótulo=IRMÃOS)])])

# ==========================================
# 4. NECESSIDADE EDUCACIONAL ESPECIAL (NEE)
# ==========================================
SECAO_NEE = SeçãoFormulário(título="4. Necessidade Educacional Especial (NEE)", linhas=[LinhaFormulário(proporções=[1],
                                                                                                        campos=[Campo(
                                                                                                            chave="possui_nee",
                                                                                                            rótulo="Possui Necessidade Educacional Especial?",
                                                                                                            tipo="radio",
                                                                                                            opções=[
                                                                                                                "Não",
                                                                                                                "Sim"],
                                                                                                            valor_padrão="Não"), ]),
                                                                                        LinhaFormulário(proporções=[1],
                                                                                                        campos=[Campo(
                                                                                                            chave="nee_opções",
                                                                                                            rótulo="Selecione as opções de NEE:",
                                                                                                            tipo="multiselect",
                                                                                                            opções=[
                                                                                                                "Dislexia",
                                                                                                                "Baixa Visão",
                                                                                                                "Deficiência Auditiva",
                                                                                                                "Transtorno do Espectro Autista",
                                                                                                                "Surdo cegueira",
                                                                                                                "Dislalia",
                                                                                                                "Cegueira",
                                                                                                                "TDAH",
                                                                                                                "Altas Habilidades/Superdotação",
                                                                                                                "Deficiência Intelectual",
                                                                                                                "Disgrafia",
                                                                                                                "Síndrome de Rett",
                                                                                                                "Surdez",
                                                                                                                "Distúrbios de Aprendizagem",
                                                                                                                "Deficiência Física",
                                                                                                                "Discalculia",
                                                                                                                "Síndrome de Asperger",
                                                                                                                "Deficiência Múltipla",
                                                                                                                "Transtorno Desintegrativo da Infância",
                                                                                                                "Outro"])]),
                                                                                        LinhaFormulário(proporções=[1],
                                                                                                        campos=[Campo(
                                                                                                            chave="nee_outro_texto",
                                                                                                            rótulo="Especifique a NEE (Outro):")]),
                                                                                        LinhaFormulário(proporções=[1],
                                                                                                        campos=[Campo(
                                                                                                            chave="restricao_alimentar",
                                                                                                            rótulo="Restrição alimentar (se houver):")])])

# ==========================================
# 5. DADOS ESCOLARES E MATRÍCULA
# ==========================================
SECAO_DADOS_ESCOLARES = SeçãoFormulário(título="5. Dados Escolares e Matrícula", linhas=[
    LinhaFormulário(proporções=[1, 2, 1, 1], campos=[Campo(chave="ano_letivo", rótulo=ANO_LETIVO, valor_padrão="2026"),
                                                     Campo(chave="curso", rótulo=CURSO,
                                                           valor_padrão="Ensino Fundamental"),
                                                     Campo(chave="ano_serie", rótulo=ANO_SÉRIE),
                                                     Campo(chave="turma", rótulo=TURMA), ]),
    LinhaFormulário(proporções=[2, 1, 2], campos=[Campo(chave="num_matricula", rótulo=NUM_MATRÍCULA),
                                                  Campo(chave="data_matricula", rótulo=DATA_MATRÍCULA),
                                                  Campo(chave="resp_mat_opcao", rótulo=RESPONSÁVEL_MATRÍCULA,
                                                        tipo="select", opções=["Mãe", "Pai", "Outro"]), ]),
    LinhaFormulário(proporções=[1], campos=[Campo(chave="resp_mat_outro_texto", rótulo=RESPONSÁVEL_MATRÍCULA_OUTRO)]),
    LinhaFormulário(proporções=[1, 1], campos=[
        Campo(chave="preenchido_por", rótulo=PREENCHEDOR_MATRÍCULA, valor_padrão="Secretaria Escolar"),
        Campo(chave="logo_src", rótulo="URL da Logo (opcional):", valor_padrão=""), ])])

# ==========================================
# EXPORTAÇÃO FINAL
# ==========================================
TODAS_AS_SECOES = [SECAO_DADOS_PESSOAIS, SECAO_DADOS_FAMILIARES, SECAO_ENDERECO_CONTATO, SECAO_NEE,
                   SECAO_DADOS_ESCOLARES]
