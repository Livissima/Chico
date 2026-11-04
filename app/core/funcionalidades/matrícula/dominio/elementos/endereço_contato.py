from __future__ import annotations

from app.core.funcionalidades.matrícula.dominio.campos import Campo, Linha

logradouro = Campo(
    chave="logradouro",
    rotulo="Logradouro"
)
quadra = Campo(
    chave="quadra",
    rotulo="Quadra"
)
lote = Campo(
    chave="lote",
    rotulo="Lote"
)
número_casa = Campo(
    chave="numero",
    rotulo="Número"
)
cep = Campo(
    chave="cep",
    rotulo="CEP"
)
complemento = Campo(
    chave="complemento",
    rotulo="Complemento"
)
bairro = Campo(
    chave="bairro",
    rotulo="Bairro"
)
município = Campo(
    chave="municipio",
    rotulo="Município"
)
cel_mãe = Campo(
    chave="celular_mae",
    rotulo="Celular da Mãe"
)
cel_pai = Campo(
    chave="celular_pai",
    rotulo="Celular do Pai"
)
cel_ctt = Campo(
    chave="fone_contato",
    rotulo="Telefone p/ Contato"
)
cel_fixo = Campo(
    chave="telefone_fixo",
    rotulo="Telefone Fixo"
)
email = Campo(
    chave="email_contato",
    rotulo="Email p/ contato"
)
uc_equatorial = Campo(
    chave="uc_equatorial",
    rotulo="UC (Equatorial)"
)
cad_único = Campo(
    chave="cadunico",
    rotulo="CadÚnico"
)
irmãos = Campo(
    chave="irmaos_ue",
    rotulo="Irmão(s) Nesta Escola"
)


linha_endereço_1 = Linha(proporcoes=(3, 1, 1, 1, 2), campos=(logradouro, quadra, lote, número_casa, cep,))
linha_endereço_2 = Linha(proporcoes=(2, 2, 2), campos=(complemento, bairro, município,))
linha_endereço_3 = Linha(proporcoes=(1, 1, 1, 1), campos=(cel_mãe, cel_pai, cel_ctt, cel_fixo,))
linha_endereço_4 = Linha(proporcoes=(2, 2, 1), campos=(email, uc_equatorial, cad_único,))
linha_endereço_5 = Linha(proporcoes=(1,), campos=(irmãos,))

linhas_endereço = (linha_endereço_1, linha_endereço_2, linha_endereço_3, linha_endereço_4, linha_endereço_5, )
