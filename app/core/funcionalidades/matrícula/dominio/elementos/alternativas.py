from __future__ import annotations

ANO_LETIVO_PADRAO = "2027"
NAO_SIM = ("", "Não", "Sim")
GENEROS = ("", "Masculino", "Feminino")
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
    "",
    "AC", "AL", "AP", "AM", "BA", "CE", "DF", "ES", "GO",
    "MA", "MT", "MS", "MG", "PA", "PB", "PR", "PE", "PI",
    "RJ", "RN", "RS", "RO", "RR", "SC", "SP", "SE", "TO"
)
