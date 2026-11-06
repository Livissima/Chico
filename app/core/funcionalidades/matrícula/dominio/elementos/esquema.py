"""Definição do formulário de matrícula (substitui elements/campos.py, linhas.py,
esqueleto.py e rótulos.py).

Para adicionar um campo: acrescente um `Campo(...)` na `Linha` desejada.
Se ele tiver `marcador`, a ficha impressa precisa usar as variáveis `<marcador>_<sufixo>`.
"""
from __future__ import annotations

from app.core.funcionalidades.matrícula.dominio.campos import Esquema, Seção
from app.core.funcionalidades.matrícula.dominio.elementos.dados_escolares import linhas_escolares
from app.core.funcionalidades.matrícula.dominio.elementos.dados_familiares import linhas_família
from app.core.funcionalidades.matrícula.dominio.elementos.dados_pessoais import linhas_pessoal
from app.core.funcionalidades.matrícula.dominio.elementos.endereço_contato import linhas_endereço
from app.core.funcionalidades.matrícula.dominio.elementos.necessidades import linhas_nee


#todo: Identificar o que faz com que o background do campo fique branco caso cliquemos em uma string que ficou salva de outro preenchimento
#todo: Talvez fosse uma boa criar uma lógica que deixasse o background dos campos verdes quando eles fossem preenchidos com um valor válido, mantendo o padrão caso estejam vazios



SECAO_DADOS_PESSOAIS = Seção(titulo="1. Dados Pessoais", linhas=linhas_pessoal, )

SECAO_DADOS_FAMILIARES = Seção(titulo="2. Dados Familiares", linhas=linhas_família, )

SECAO_ENDERECO_CONTATO = Seção(titulo="3. Endereço e Contato", linhas=linhas_endereço, )

SECAO_NEE = Seção(titulo="4. Necessidade Educacional Especial (NEE)", linhas=linhas_nee, )

SECAO_DADOS_ESCOLARES = Seção(titulo="5. Dados Escolares e Matrícula", linhas=linhas_escolares, )

ESQUEMA = Esquema(
    secoes=(
        SECAO_DADOS_PESSOAIS,
        SECAO_DADOS_FAMILIARES,
        SECAO_ENDERECO_CONTATO,
        SECAO_NEE,
        SECAO_DADOS_ESCOLARES,
    )
)
