from __future__ import annotations

from app.core.funcionalidades.matrícula.dominio.campos import Campo, Linha
from app.core.funcionalidades.matrícula.dominio.elementos.regrinhas import obrigatório, obrigatório_número_max, \
    número_max, número

logradouro = Campo(
    chave="logradouro",
    rotulo="Logradouro",
    regras=obrigatório
)
quadra = Campo(
    chave="quadra",
    rotulo="Quadra"
)
lote = Campo(
    chave="lote",
    rotulo="Lote",
    regras=número
)
número_casa = Campo(
    chave="numero",
    rotulo="Número"
)
cep = Campo(
    chave="cep",
    rotulo="CEP",
    regras=obrigatório_número_max(8)
    #todo: Bolar um esqueminha de placeholder para cep e de formatação como cep (00000-000)
)
complemento = Campo(
    chave="complemento",
    rotulo="Complemento"
)
bairro = Campo(
    chave="bairro",
    rotulo="Bairro",
    regras=obrigatório
)
município = Campo(
    chave="municipio",
    rotulo="Município",
    regras=obrigatório
)
telefone_um = Campo(
    #todo: bolar um esqueminha de validação de telefones e também de formatação de acordo com quantidade de dígitos: (xx) xxxxx xxxx / (xx) xxxx xxxx / xxxxx xxxx / xxxx xxxx
    chave="celular_mae",
    rotulo="Celular da Mãe",
    regras=obrigatório_número_max(11)
)
telefone_dois = Campo(
    chave="celular_pai",
    rotulo="Celular do Pai",
    regras=número_max(11)
)
telefone_três = Campo(
    chave="fone_contato",
    rotulo="Telefone p/ Contato",
    regras=número_max(11)
)
cel_fixo = Campo(
    chave="telefone_fixo",
    rotulo="Telefone Fixo",
    regras=número_max(11)
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
linha_endereço_3 = Linha(proporcoes=(1, 1, 1, 1), campos=(telefone_um, telefone_dois, telefone_três, cel_fixo,))
linha_endereço_4 = Linha(proporcoes=(2, 2, 1), campos=(email, uc_equatorial, cad_único,))
linha_endereço_5 = Linha(proporcoes=(1,), campos=(irmãos,))

linhas_endereço = (linha_endereço_1, linha_endereço_2, linha_endereço_3, linha_endereço_4, linha_endereço_5, )
