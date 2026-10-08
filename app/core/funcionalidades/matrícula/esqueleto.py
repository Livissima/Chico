from elements.linhas import *
from elements.templates import SeçãoFormulário, LinhaFormulário, Campo

# ==========================================
# 1. DADOS PESSOAIS
SECAO_DADOS_PESSOAIS = SeçãoFormulário(
    título="1. Dados Pessoais",
    linhas=[linha1, linha2, linha3, linha4, linha5, linha6]
)
# ==========================================
# 2. DADOS FAMILIARES
# ==========================================
SECAO_DADOS_FAMILIARES = SeçãoFormulário(
    título="2. Dados Familiares",
    linhas=[linha7, linha8, linha9, linha10, linha11, linha12, linha13, linha14, linha15, linha16, linha17]
)
# ==========================================
# 3. ENDEREÇO E CONTATO
# ==========================================
SECAO_ENDERECO_CONTATO = SeçãoFormulário(
    título="3. Endereço e Contato",
    linhas=[linha18, linha19, linha20, linha21, linha22]
)

# ==========================================
# 4. NECESSIDADE EDUCACIONAL ESPECIAL (NEE)
# ==========================================
SECAO_NEE = SeçãoFormulário(
    título="4. Necessidade Educacional Especial (NEE)",
    linhas=[linha23, linha24, linha25, linha26]
)
# ==========================================
# 5. DADOS ESCOLARES E MATRÍCULA
# ==========================================
SECAO_DADOS_ESCOLARES = SeçãoFormulário(
    título="5. Dados Escolares e Matrícula",
    linhas=[linha27, linha28, linha29, linha30]
)
# ==========================================
# EXPORTAÇÃO FINAL
# ==========================================
TODAS_AS_SECOES = [
    SECAO_DADOS_PESSOAIS, SECAO_DADOS_FAMILIARES, SECAO_ENDERECO_CONTATO, SECAO_NEE, SECAO_DADOS_ESCOLARES
]
