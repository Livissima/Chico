from .estrutura import Campo, LinhaFormulário, SeçãoFormulário
from .campos import *

linha1 = LinhaFormulário(proporções=[3, 1, 1], campos=[nome_estudante, dn, gênero])
linha2 = LinhaFormulário(proporções=[2, 2, 1], campos=[nome_social, cpf_estudante, uf_naturalidade])
linha3 = LinhaFormulário(proporções=[2, 1, 1, 1], campos=[município_naturalidade, termo_cn, livro_cn, folha_cn])
linha4 = LinhaFormulário(proporções=[1, 2, 2], campos=[data_emissão_cn, cartório_registro, município_registro])
linha5 = LinhaFormulário(proporções=[1, 1], campos=[etnia, religião])
linha6 = LinhaFormulário(proporções=[1, 1, 1, 1, 1], campos=[bermuda, camiseta, calça, jaqueta, tênis])
# ==========================================
# 2. DADOS FAMILIARES
# ==========================================
linha7 = LinhaFormulário(proporções=[3, 1, 1], campos=[f1_nome, f1_dn, f1_falecida])
linha8 = LinhaFormulário(proporções=[2, 2, 1, 1, 1], campos=[f1_cpf, f1_título, f1_uf, f1_zona, f1_secao])
linha9 = LinhaFormulário(proporções=[1], campos=[f1_prof])
# --- Filiação 2 ---
linha10 = LinhaFormulário(proporções=[3, 1, 1], campos=[f2_nome, f2_dn, f2_falecido])
linha11 = LinhaFormulário(proporções=[2, 2, 1, 1, 1], campos=[f2_cpf, f2_título, f2_uf, f2_zona, f2_secao])
linha12 = LinhaFormulário(proporções=[1], campos=[f2_prof])
# --- Responsável Legal ---
linha13 = LinhaFormulário(proporções=[3, 1], campos=[responsavel_nome, responsavel_dn])
linha14 = LinhaFormulário(proporções=[2, 2, 1, 1, 1], campos=[responsavel_cpf, responsavel_título, responsavel_uf, responsavel_zona, responsavel_secao])
linha15 = LinhaFormulário(proporções=[2, 2], campos=[responsavel_profissao, responsavel_relacao])
# --- Núcleo Familiar ---
linha16 = LinhaFormulário(proporções=[1], campos=[núcleo_familiar])
linha17 = LinhaFormulário(proporções=[1], campos=[núcleo_outros])
# ==========================================
# 3. ENDEREÇO E CONTATO
# ==========================================
linha18 = LinhaFormulário(proporções=[3, 1, 1, 1, 2], campos=[logradouro, quadra, lote, núm_casa, cep])
linha19 = LinhaFormulário(proporções=[2, 2, 2], campos=[complemento, bairro, município])
linha20 = LinhaFormulário(proporções=[1, 1, 1, 1], campos=[tel_mãe, tel_pai, tel_contato, tel_fixo])
linha21 = LinhaFormulário(proporções=[2, 2, 1], campos=[email_contato, unidade_consumidora, cad_único])
linha22 = LinhaFormulário(proporções=[1], campos=[irmãos])
# ==========================================
# 4. NECESSIDADE EDUCACIONAL ESPECIAL (NEE)
# ==========================================
linha23 = LinhaFormulário(proporções=[1], campos=[possui_nee])
linha24 = LinhaFormulário(proporções=[1], campos=[necessidades])
linha25 = LinhaFormulário(proporções=[1], campos=[outra_necessidade])
linha26 = LinhaFormulário(proporções=[1], campos=[restrição_alimentar])
# ==========================================
# 5. DADOS ESCOLARES E MATRÍCULA
# ==========================================
linha27 = LinhaFormulário(proporções=[1, 2, 1, 1], campos=[ano_letivo, curso, ano_série, turma])
linha28 = LinhaFormulário(proporções=[2, 1, 2], campos=[num_matrícula, data_matrícula, responsável_matrícula])
linha29 = LinhaFormulário(proporções=[1], campos=[responsável_matrícula_outro])
linha30 = LinhaFormulário(proporções=[1, 1], campos=[preenchedora_matrícula, url_logo])