from .estrutura import Campo, LinhaFormulário, SeçãoFormulário
from .campos import *

linha1 = LinhaFormulário(proporções=[3, 1, 1], campos=[nome_estudante, dn, gênero])
linha2 = LinhaFormulário(proporções=[2, 2, 1], campos=[nome_social, cpf_estudante, uf_naturalidade])
linha3 = LinhaFormulário(proporções=[2, 1, 1, 1], campos=[município_naturalidade, termo_cn, livro_cn, folha_cn])
linha4 = LinhaFormulário(proporções=[1, 2, 2], campos=[data_emissão_cn, cartório_registro, município_registro])
linha5 = LinhaFormulário(proporções=[1, 1], campos=[etnia, religião])
linha6 = LinhaFormulário(proporções=[1, 1, 1, 1, 1], campos=[bermuda, camiseta, calça, jaqueta, tênis])

linha7 = LinhaFormulário(proporções=[3, 1, 1], campos=[f1_nome, f1_dn, f1_falecida])

linha8 = LinhaFormulário(proporções=[2, 2, 1, 1, 1], campos=[f1_cpf, f1_título, f1_uf, f1_zona, f1_secao])
linha9 = LinhaFormulário(proporções=[1], campos=[f1_prof]),

# --- Filiação 2 ---
linha10 = LinhaFormulário(proporções=[3, 1, 1], campos=[f2_nome, f2_dn, f2_falecido])
linha11 = LinhaFormulário(proporções=[2, 2, 1, 1, 1],campos=[f2_cpf, f2_título, f2_uf, f2_zona, f2_secao])
linha12 = LinhaFormulário(proporções=[1], campos=[f2_prof])

    # --- Responsável Legal ---
linha13 = LinhaFormulário(proporções=[3, 1], campos=[responsavel_nome, responsavel_dn])
linha14 = LinhaFormulário(proporções=[2, 2, 1, 1, 1], campos=[responsavel_cpf, responsavel_título, responsavel_uf, responsavel_zona, responsavel_secao])
linha15 = LinhaFormulário(proporções=[2, 2], campos=[responsavel_profissao, responsavel_relacao])

    # --- Núcleo Familiar ---
linha16 = LinhaFormulário(proporções=[1], campos=[
    Campo(chave="nucleo_opções", rótulo=NÚCLEO_OPÇÕES, tipo="multiselect",
                                                  opções=["Mãe", "Pai", "Irmãos", "Madrasta", "Tutor Legal", "Tios",
                                                          "Avós", "Primos", "Padrasto", "Outros"])]),
linha17 = LinhaFormulário(proporções=[1], campos=[
    Campo(chave="nuc_outros_texto", rótulo=NÚCLEO_OUTROS_INPUT)
])]


