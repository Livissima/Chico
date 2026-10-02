from .rótulos import *
from .estrutura import Campo

nome_estudante = Campo(chave="nome_estudante", rótulo=NOME_ESTUDANTE, obrigatório=True, cumprimento_mínimo=3)
dn = Campo(chave="data_nascimento", rótulo=DATA_NASCIMENTO, obrigatório=True, tipo_dado="date")
gênero = Campo(chave="genero", rótulo=GÊNERO, tipo="select", opções=["", "Masculino", "Feminino"])

nome_social = Campo(chave="nome_social", rótulo=NOME_SOCIAL)
cpf_estudante = Campo(chave="cpf_estudante", rótulo=CPF_ESTUDANTE, tipo_dado="cpf", cumprimento_máximo=14)
uf_naturalidade = Campo(chave="uf_naturalidade", rótulo=UF_NATURALIDADE, cumprimento_máximo=2)

município_naturalidade = Campo(chave="municipio_naturalidade", rótulo=MUNICÍPIO_NATURALIDADE)
termo_cn = Campo(chave="termo_cert_nasc", rótulo=TERMO_CN)
livro_cn = Campo(chave="livro", rótulo=LIVRO_CN)
folha_cn = Campo(chave="folha", rótulo=FOLHA)

data_emissão_cn = Campo(chave="dt_emissao_cn", rótulo=DATA_EMISSÃO_CN, tipo_dado="date")
cartório_registro = Campo(chave="cartorio_registro", rótulo=CARTÓRIO_REGISTRO)
município_registro = Campo(chave="municipio_registro", rótulo=MUNICÍPIO_REGISTRO)

etnia = Campo(chave="cor_etnia", rótulo=ETNIA, tipo="select", opções=["", "Branca", "Preta", "Parda", "Indígena", "Amarela", "Não declarada"])
religião = Campo(chave="religiao", rótulo=RELIGIÃO, tipo="select", opções=["", "Budismo", "Catolicismo", "Evangelismo", "Congregação", "Espírita", "Sem religião"])

bermuda = Campo(chave="tam_bermuda", rótulo=BERMUDA)
camiseta = Campo(chave="tam_camiseta", rótulo=CAMISETA)
calça = Campo(chave="tam_calca", rótulo=CALÇA)
jaqueta = Campo(chave="tam_jaqueta", rótulo=JAQUETA)
tênis = Campo(chave="tam_tenis", rótulo=TÊNIS)

f1_nome = Campo(chave="filiacao1_nome", rótulo=FILIAÇÃO1_NOME)
f1_dn = Campo(chave="filiacao1_dn", rótulo=FILIAÇÃO1_DN)
f1_falecida = Campo(chave="filiacao1_falecida", rótulo=FILIAÇÃO1_FALECIDA, tipo="radio", opções=["Não", "Sim"], valor_padrão="Não")

f1_cpf = Campo(chave="filiacao1_cpf", rótulo=FILIAÇÃO1_CPF, tipo_dado="cpf")
f1_título = Campo(chave="filiacao1_título", rótulo=FILIAÇÃO1_TÍTULO)
f1_uf = Campo(chave="filiacao1_uf", rótulo=FILIAÇÃO1_UF_ELEITORAL, cumprimento_máximo=2)
f1_zona = Campo(chave="filiacao1_zona", rótulo=FILIAÇÃO1_ZONA)
f1_secao = Campo(chave="filiacao1_secao", rótulo=FILIAÇÃO1_SEÇÃO)

f1_prof =  Campo(chave="filiacao1_profissao", rótulo=FILIAÇÃO1_PROFISSÃO)

f2_nome = Campo(chave="filiacao2_nome", rótulo=FILIAÇÃO2_NOME)
f2_dn = Campo(chave="filiacao2_dn", rótulo=FILIAÇÃO2_DN)
f2_falecido = Campo(chave="filiacao2_falecido", rótulo=FILIAÇÃO2_FALECIDA, tipo="radio", opções=["Não", "Sim"], valor_padrão="Não")

f2_cpf = Campo(chave="filiacao2_cpf", rótulo=FILIAÇÃO2_CPF, tipo_dado="cpf")
f2_título = Campo(chave="filiacao2_título", rótulo=FILIAÇÃO2_TÍTULO)
f2_uf = Campo(chave="filiacao2_uf", rótulo=FILIAÇÃO2_UF_ELEITORAL, cumprimento_máximo=2)
f2_zona = Campo(chave="filiacao2_zona", rótulo=FILIAÇÃO2_ZONA)
f2_secao = Campo(chave="filiacao2_secao", rótulo=FILIAÇÃO2_SEÇÃO)

f2_prof = Campo(chave="filiacao2_profissao", rótulo=FILIAÇÃO2_PROFISSÃO)

responsavel_nome = Campo(chave="responsavel_nome", rótulo=RESPONSÁVEL_NOME)
responsavel_dn = Campo(chave="responsavel_dn", rótulo=RESPONSÁVEL_DN)

responsavel_cpf = Campo(chave="responsavel_cpf", rótulo=RESPONSÁVEL_CPF, tipo_dado="cpf")
responsavel_título = Campo(chave="responsavel_título", rótulo=RESPONSÁVEL_TÍTULO)
responsavel_uf = Campo(chave="responsavel_uf", rótulo=RESPONSÁVEL_UF, cumprimento_máximo=2)
responsavel_zona = Campo(chave="responsavel_zona", rótulo=RESPONSÁVEL_ZONA)
responsavel_secao = Campo(chave="responsavel_secao", rótulo=RESPONSÁVEL_SEÇÃO)

responsavel_profissao = Campo(chave="responsavel_profissao", rótulo=RESPONSÁVEL_PROFISSÃO)
responsavel_relacao = Campo(chave="responsavel_relacao", rótulo=RESPONSÁVEL_VÍNCULO)











