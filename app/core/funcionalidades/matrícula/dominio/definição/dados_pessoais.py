from __future__ import annotations

from app.core.funcionalidades.matrícula.dominio.campos import Campo
from app.core.funcionalidades.matrícula.dominio.definição.alternativas import UFS, ETNIAS, RELIGIOES, GENEROS
from app.core.funcionalidades.matrícula.dominio.regras import ComprimentoMaximo, ApenasLetras, Obrigatorio, \
    ComprimentoMinimo
from app.core.funcionalidades.matrícula.dominio.tipos import TipoDado, TipoCampo

nome_social = Campo("nome_social", "Nome Social")
cpf_estudante =  Campo("cpf_estudante", "CPF (Estudante)", tipo_dado=TipoDado.CPF, regras=(ComprimentoMaximo(14),))
uf_naturalidade = Campo("uf_naturalidade", "UF de Nascimento", regras=(ComprimentoMaximo(2), ApenasLetras() ), opcoes=UFS)
município_naturalidade = Campo("municipio_naturalidade", "Município de Nascimento")
termo_cn = Campo("termo_cert_nasc", "Termo Cert. Nasc.")
livro_cn = Campo("livro", "Livro")
folha_cn = Campo("folha", "Folha")
data_emissão_cn = Campo("dt_emissao_cn", "Dt. Emissão (CN)", tipo_dado=TipoDado.DATA)
cartório_cn = Campo("cartorio_registro", "Cartório de Registro")
município_cn = Campo("municipio_registro", "Município de Registro")
etnia = Campo("cor_etnia", "Cor/Etnia", tipo=TipoCampo.SELECT, opcoes=ETNIAS, marcador="cor")
religião = Campo("religiao", "Religião", tipo=TipoCampo.SELECT, opcoes=RELIGIOES, marcador="rel")
t_bermuda = Campo("tam_bermuda", "Bermuda")
t_camiseta = Campo("tam_camiseta", "Camiseta")
t_calça = Campo("tam_calca", "Calça")
t_jaqueta = Campo("tam_jaqueta", "Jaqueta")
t_tênis = Campo("tam_tenis", "Tênis")
nome_estudante = Campo(
    "nome_estudante", "Nome do Estudante", regras=(Obrigatorio(), ComprimentoMinimo(3), ApenasLetras())
)
dn = Campo(
    "data_nascimento", "Data de Nascimento (dd/mm/aaaa)", tipo_dado=TipoDado.DATA, regras=(Obrigatorio(),)
)
gênero = Campo(
    "genero", "Gênero", tipo=TipoCampo.SELECT, opcoes=GENEROS, marcador="genero", sufixos_marcador={"Masculino": "m", "Feminino": "f"}
)
