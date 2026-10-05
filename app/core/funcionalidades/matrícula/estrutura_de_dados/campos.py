from .rótulos import *
from .estrutura import Campo

### LINHA 1
nome_estudante = Campo(chave="nome_estudante", rótulo=NOME_ESTUDANTE, obrigatório=True, cumprimento_mínimo=3)
dn = Campo(chave="data_nascimento", rótulo=DATA_NASCIMENTO, obrigatório=True, tipo_dado="date")
gênero = Campo(chave="genero", rótulo=GÊNERO, tipo="select", opções=["", "Masculino", "Feminino"])

### LINHA 2
nome_social = Campo(chave="nome_social", rótulo=NOME_SOCIAL)
cpf_estudante = Campo(chave="cpf_estudante", rótulo=CPF_ESTUDANTE, tipo_dado="cpf", cumprimento_máximo=14)
uf_naturalidade = Campo(chave="uf_naturalidade", rótulo=UF_NATURALIDADE, cumprimento_máximo=2)

### LINHA 3
município_naturalidade = Campo(chave="municipio_naturalidade", rótulo=MUNICÍPIO_NATURALIDADE)
termo_cn = Campo(chave="termo_cert_nasc", rótulo=TERMO_CN)
livro_cn = Campo(chave="livro", rótulo=LIVRO_CN)
folha_cn = Campo(chave="folha", rótulo=FOLHA)

### LINHA 4
data_emissão_cn = Campo(chave="dt_emissao_cn", rótulo=DATA_EMISSÃO_CN, tipo_dado="date")
cartório_registro = Campo(chave="cartorio_registro", rótulo=CARTÓRIO_REGISTRO)
município_registro = Campo(chave="municipio_registro", rótulo=MUNICÍPIO_REGISTRO)

### LINHA 5
etnia = Campo(chave="cor_etnia", rótulo=ETNIA, tipo="select", opções=ETNIAS)
religião = Campo(chave="religiao", rótulo=RELIGIÃO, tipo="select", opções=RELIGIÕES)

### LINHA 6
bermuda = Campo(chave="tam_bermuda", rótulo=BERMUDA)
camiseta = Campo(chave="tam_camiseta", rótulo=CAMISETA)
calça = Campo(chave="tam_calca", rótulo=CALÇA)
jaqueta = Campo(chave="tam_jaqueta", rótulo=JAQUETA)
tênis = Campo(chave="tam_tenis", rótulo=TÊNIS)

### LINHA 7
f1_nome = Campo(chave="filiacao1_nome", rótulo=FILIAÇÃO1_NOME)
f1_dn = Campo(chave="filiacao1_dn", rótulo=FILIAÇÃO1_DN)
f1_falecida = Campo(chave="filiacao1_falecida", rótulo=FILIAÇÃO1_FALECIDA, tipo="radio", opções=["Não", "Sim"], valor_padrão="Não")

### LINHA 8
f1_cpf = Campo(chave="filiacao1_cpf", rótulo=FILIAÇÃO1_CPF, tipo_dado="cpf")
f1_título = Campo(chave="filiacao1_título", rótulo=FILIAÇÃO1_TÍTULO)
f1_uf = Campo(chave="filiacao1_uf", rótulo=FILIAÇÃO1_UF_ELEITORAL, cumprimento_máximo=2)
f1_zona = Campo(chave="filiacao1_zona", rótulo=FILIAÇÃO1_ZONA)
f1_secao = Campo(chave="filiacao1_secao", rótulo=FILIAÇÃO1_SEÇÃO)

### LINHA 9
f1_prof = Campo(chave="filiacao1_profissao", rótulo=FILIAÇÃO1_PROFISSÃO)

### LINHA 10
f2_nome = Campo(chave="filiacao2_nome", rótulo=FILIAÇÃO2_NOME)
f2_dn = Campo(chave="filiacao2_dn", rótulo=FILIAÇÃO2_DN)
f2_falecido = Campo(chave="filiacao2_falecido", rótulo=FILIAÇÃO2_FALECIDA, tipo="radio", opções=["Não", "Sim"], valor_padrão="Não")

### LINHA 11
f2_cpf = Campo(chave="filiacao2_cpf", rótulo=FILIAÇÃO2_CPF, tipo_dado="cpf")
f2_título = Campo(chave="filiacao2_título", rótulo=FILIAÇÃO2_TÍTULO)
f2_uf = Campo(chave="filiacao2_uf", rótulo=FILIAÇÃO2_UF_ELEITORAL, cumprimento_máximo=2)
f2_zona = Campo(chave="filiacao2_zona", rótulo=FILIAÇÃO2_ZONA)
f2_secao = Campo(chave="filiacao2_secao", rótulo=FILIAÇÃO2_SEÇÃO)

### LINHA 12
f2_prof = Campo(chave="filiacao2_profissao", rótulo=FILIAÇÃO2_PROFISSÃO)

### LINHA 13
responsavel_nome = Campo(chave="responsavel_nome", rótulo=RESPONSÁVEL_NOME)
responsavel_dn = Campo(chave="responsavel_dn", rótulo=RESPONSÁVEL_DN)

### LINHA 14
responsavel_cpf = Campo(chave="responsavel_cpf", rótulo=RESPONSÁVEL_CPF, tipo_dado="cpf")
responsavel_título = Campo(chave="responsavel_título", rótulo=RESPONSÁVEL_TÍTULO)
responsavel_uf = Campo(chave="responsavel_uf", rótulo=RESPONSÁVEL_UF, cumprimento_máximo=2)
responsavel_zona = Campo(chave="responsavel_zona", rótulo=RESPONSÁVEL_ZONA)
responsavel_secao = Campo(chave="responsavel_secao", rótulo=RESPONSÁVEL_SEÇÃO)

### LINHA 15
responsavel_profissao = Campo(chave="responsavel_profissao", rótulo=RESPONSÁVEL_PROFISSÃO)
responsavel_relacao = Campo(chave="responsavel_relacao", rótulo=RESPONSÁVEL_VÍNCULO)

### LINHA 16
núcleo_familiar = Campo(chave="nucleo_opções", rótulo=NÚCLEO_FAMILIAR, tipo="multiselect", opções=NÚCLEO_FAMILIAR_OPÇÕES)

### LINHA 17
núcleo_outros = Campo(chave="nuc_outros_texto", rótulo=NÚCLEO_OUTROS_INPUT)

### LINHA 18
logradouro = Campo(chave="logradouro", rótulo=LOGRADOURO)
quadra = Campo(chave="quadra", rótulo=QUADRA)
lote = Campo(chave="lote", rótulo=LOTE)
núm_casa = Campo(chave="numero", rótulo=NÚMERO)
cep = Campo(chave="cep", rótulo=CEP)

### LINHA 19
complemento = Campo(chave="complemento", rótulo=COMPLEMENTO)
bairro = Campo(chave="bairro", rótulo=BAIRRO)
município = Campo(chave="municipio", rótulo=MUNICÍPIO)

### LINHA 20
tel_mãe = Campo(chave="celular_mae", rótulo=TELEFONE_MÃE)
tel_pai = Campo(chave="celular_pai", rótulo=TELEFONE_PAI)
tel_contato = Campo(chave="fone_contato", rótulo=TELEFONE_CONTATO)
tel_fixo = Campo(chave="telefone_fixo", rótulo=TELEFONE_FIXO)

### LINHA 21
email_contato = Campo(chave="email_contato", rótulo=EMAIL_CONTATO)
unidade_consumidora = Campo(chave="uc_equatorial", rótulo=UNIDADE_CONSUMIDORA)
cad_único = Campo(chave="cadunico", rótulo=CAD_ÚNICO)

### LINHA 22
irmãos = Campo(chave="irmaos_ue", rótulo=IRMÃOS)

### LINHA 23
possui_nee = Campo(chave="possui_nee", rótulo=QUESTÃO_NEE, tipo="radio", opções=["Não", "Sim"], valor_padrão="Não")

### LINHA 24
necessidades = Campo(chave="nee_opções", rótulo=SELECIONE_NEE, tipo="multiselect", opções=NECESSIDADES)

### LINHA 25
outra_necessidade = Campo(chave="nee_outro_texto", rótulo=NEE_OUTRA)

### LINHA 26
restrição_alimentar = Campo(chave="restricao_alimentar", rótulo=RESTRIÇÃO_ALIMENTAR)

### LINHA 27
ano_letivo = Campo(chave="ano_letivo", rótulo=ANO_LETIVO, valor_padrão="2026")
curso = Campo(chave="curso", rótulo=CURSO, valor_padrão="Ensino Fundamental")
ano_série = Campo(chave="ano_serie", rótulo=ANO_SÉRIE)
turma = Campo(chave="turma", rótulo=TURMA)

### LINHA 28
num_matrícula = Campo(chave="num_matricula", rótulo=NUM_MATRÍCULA)
data_matrícula = Campo(chave="data_matricula", rótulo=DATA_MATRÍCULA)
responsável_matrícula = Campo(chave="resp_mat_opcao", rótulo=RESPONSÁVEL_MATRÍCULA, tipo="select", opções=["Mãe", "Pai", "Outro"])

### LINHA 29
responsável_matrícula_outro = Campo(chave="resp_mat_outro_texto", rótulo=RESPONSÁVEL_MATRÍCULA_OUTRO)

### LINHA 30
preenchedora_matrícula = Campo(chave="preenchido_por", rótulo=PREENCHEDORA_MATRÍCULA, valor_padrão="Secretaria Escolar")
url_logo = Campo(chave="logo_src", rótulo="URL da Logo (opcional):", valor_padrão="")