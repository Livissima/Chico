from __future__ import annotations

from app.core.funcionalidades.matrícula.dominio.campos import Campo, Linha
from app.core.funcionalidades.matrícula.dominio.elementos.alternativas import UFS, ETNIAS, RELIGIOES, GENEROS
from app.core.funcionalidades.matrícula.dominio.elementos.regrinhas import obrigatório, obrigatório_letra, \
    obrigatório_max, letra, número
from app.core.funcionalidades.matrícula.dominio.regras import ApenasLetras, Obrigatorio, \
    ComprimentoMinimo
from app.core.funcionalidades.matrícula.dominio.regras_esquema import OrdemDeDatas
from app.core.funcionalidades.matrícula.dominio.tipos import TipoDado, TipoCampo

nome_estudante = Campo(
    chave="nome_estudante",
    rotulo="Nome do Estudante",
    regras=(Obrigatorio(), ComprimentoMinimo(3), ApenasLetras())
)
nome_social = Campo(
    chave="nome_social",
    rotulo="Nome Social (opcional)",
    regras=letra
)
dn = Campo(
    chave="data_nascimento",
    rotulo="Data de Nascimento",
    tipo_dado=TipoDado.NASCIMENTO,
    regras=obrigatório
)
cpf_estudante = Campo(
    chave="cpf_estudante",
    rotulo="CPF Estudante",
    tipo_dado=TipoDado.CPF,
    regras=obrigatório_max(14)
)
gênero = Campo(
    chave="genero",
    rotulo="Gênero",
    tipo=TipoCampo.SELECT,
    opcoes=GENEROS,
    marcador="genero",
    sufixos_marcador={"Masculino": "m", "Feminino": "f"},
    regras=obrigatório
)
etnia = Campo(
    chave="cor_etnia",
    rotulo="Cor/Etnia",
    tipo=TipoCampo.SELECT,
    opcoes=ETNIAS,
    marcador="cor",
    regras=obrigatório_letra
)
religião = Campo(
    chave="religiao",
    rotulo="Religião",
    tipo=TipoCampo.SELECT,
    opcoes=RELIGIOES,
    marcador="rel",
    regras=obrigatório_letra,
)
uf_naturalidade = Campo(
    chave="uf_naturalidade",
    rotulo="UF de Nascimento",
    tipo=TipoCampo.SELECT,
    opcoes=UFS,
    regras=obrigatório_letra
)
município_naturalidade = Campo(
    chave="municipio_naturalidade",
    rotulo="Município de Nascimento",
    regras=obrigatório
)
termo_cn = Campo(
    chave="termo_cert_nasc",
    rotulo="Termo Cert. Nasc. (opcional)",
    regras=número
)
livro_cn = Campo(
    chave="livro",
    rotulo="Livro",
    regras=número
)
folha_cn = Campo(
    chave="folha",
    rotulo="Folha",
    regras=número
)
data_emissão_cn = Campo(
    chave="dt_emissao_cn",
    rotulo="Dt. Emissão (CN)",
    tipo_dado=TipoDado.DATA
)
cartório_cn = Campo(
    chave="cartorio_registro",
    rotulo="Cartório de Registro"

)
município_cn = Campo(
    chave="municipio_registro",
    rotulo="Município de Registro"
)
t_bermuda = Campo(
    chave="tam_bermuda",
    rotulo="Bermuda",
    regras=número
)
t_camiseta = Campo(
    chave="tam_camiseta",
    rotulo="Camiseta"
)
t_calça = Campo(
    chave="tam_calca",
    rotulo="Calça"
)
t_jaqueta = Campo(
    chave="tam_jaqueta",
    rotulo="Jaqueta"
)
t_tênis = Campo(
    chave="tam_tenis",
    rotulo="Tênis"
)


linha1 = Linha(proporcoes=(4, 1), campos=(nome_estudante, nome_social, ))
linha2 = Linha(proporcoes=(1, 1, 1, 1, 1), campos=(dn, cpf_estudante, gênero, etnia, religião, ))
linha3 = Linha(proporcoes=(1, 1), campos=(uf_naturalidade, município_naturalidade, ))
linha4 = Linha(proporcoes=(1, 1, 1, 1, 1, 1), campos=(termo_cn, livro_cn, folha_cn, data_emissão_cn, cartório_cn, município_cn,))
linha5 = Linha(proporcoes=(1, 1, 1, 1, 1), campos=(t_bermuda, t_camiseta, t_calça, t_jaqueta, t_tênis,))

linhas_pessoal = (
    linha1,
    linha2,
    linha3,
    linha4,
    linha5,
)

# Regras que envolvem mais de um campo (verificadas ao gerar o relatório).
regras_pessoal = (
    OrdemDeDatas(
        anterior=dn.chave,
        posterior=data_emissão_cn.chave,
        alvo=data_emissão_cn.chave,
        mensagem="A data de emissão da certidão deve ser posterior à data de nascimento do estudante.",
    ),
)
