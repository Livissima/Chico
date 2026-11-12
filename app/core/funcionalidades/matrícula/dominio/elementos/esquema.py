"""Definição do formulário de matrícula (substitui elements/campos.py, linhas.py,
esqueleto.py e rótulos.py).

Para adicionar um campo: acrescente um `Campo(...)` na `Linha` desejada.
Se ele tiver `marcador`, a ficha impressa precisa usar as variáveis `<marcador>_<sufixo>`.
"""
from __future__ import annotations

from app.core.funcionalidades.matrícula.dominio.campos import Esquema, Seção
from app.core.funcionalidades.matrícula.dominio.elementos.dados_escolares import linhas_escolares
from app.core.funcionalidades.matrícula.dominio.elementos.dados_familiares import linhas_família, regras_família, \
    pessoa_filiação_1, pessoa_filiação_2, pessoa_responsável
from app.core.funcionalidades.matrícula.dominio.elementos.dados_pessoais import linhas_pessoal, regras_pessoal, \
    cpf_estudante
from app.core.funcionalidades.matrícula.dominio.elementos.endereço_contato import linhas_endereço
from app.core.funcionalidades.matrícula.dominio.elementos.necessidades import linhas_nee
from app.core.funcionalidades.matrícula.dominio.regras_esquema import CpfsDistintos


# Variáveis que o pagina_print.html usa mas que não são campos do formulário (saem em branco na ficha).
# Se um dia criar o campo correspondente, apague a variável daqui.
VARIAVEIS_SEM_CAMPO = {
    "logo_src": "",
    "responsavel_profissao": "",
}

SECAO_DADOS_PESSOAIS = Seção(titulo="1. Dados Pessoais", linhas=linhas_pessoal, )

SECAO_DADOS_FAMILIARES = Seção(titulo="2. Dados Familiares", linhas=linhas_família, )

SECAO_ENDERECO_CONTATO = Seção(titulo="3. Endereço e Contato", linhas=linhas_endereço, )

SECAO_NEE = Seção(titulo="4. Necessidade Educacional Especial (NEE)", linhas=linhas_nee, )

SECAO_DADOS_ESCOLARES = Seção(titulo="5. Dados Escolares e Matrícula", linhas=linhas_escolares, )

# Regras entre campos de seções diferentes ficam aqui; as de uma seção só ficam no módulo dela.
regras_esquema = (
    *regras_pessoal,
    *regras_família,
    CpfsDistintos(campos=(cpf_estudante.chave, pessoa_filiação_1.cpf, pessoa_filiação_2.cpf, pessoa_responsável.cpf, )),
)

ESQUEMA = Esquema(
    secoes=(
        SECAO_DADOS_PESSOAIS,
        SECAO_DADOS_FAMILIARES,
        SECAO_ENDERECO_CONTATO,
        SECAO_NEE,
        SECAO_DADOS_ESCOLARES,
    ),
    regras=regras_esquema,
)

