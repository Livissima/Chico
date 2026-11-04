from __future__ import annotations

from app.core.funcionalidades.matrícula.dominio.campos import Campo, Dependencia, Linha
from app.core.funcionalidades.matrícula.dominio.elementos.alternativas import ANO_LETIVO_PADRAO, RESPONSAVEL_MATRICULA
from app.core.funcionalidades.matrícula.dominio.elementos.regrinhas import obrigatório_número_max, obrigatório
from app.core.funcionalidades.matrícula.dominio.regras import Obrigatorio, ComprimentoMaximo, ApenasNumeros
from app.core.funcionalidades.matrícula.dominio.tipos import TipoCampo, TipoDado

ano_letivo = Campo(
    chave="ano_letivo",
    rotulo="Ano Letivo",
    valor_padrao=ANO_LETIVO_PADRAO,
    regras=obrigatório
)
curso = Campo(
    chave="curso",
    rotulo="Curso",
    valor_padrao="199",
    regras=obrigatório_número_max(3)
)
série = Campo(
    chave="ano_serie",
    rotulo="Ano/Série",
    regras=obrigatório_número_max(1)
)
turma = Campo(
    chave="turma",
    rotulo="Turma",
    regras=obrigatório_número_max(1)
)
num_matrícula = Campo(
    chave="num_matricula",
    rotulo="Nº Matrícula (aluno da rede)",
    regras=obrigatório_número_max(11)
)
data_matrícula = Campo(
    chave="data_matricula",
    rotulo="Data Matrícula (dd/mm/aaaa)",
    tipo_dado=TipoDado.DATA
)
responsável_matrícula = Campo(
    chave="resp_mat_opcao",
    rotulo="Responsável pela matrícula",
    tipo=TipoCampo.SELECT,
    opcoes=RESPONSAVEL_MATRICULA,
    marcador="resp_mat"
)
responsável_matrícula_outro = Campo(
    chave="resp_mat_outro_texto",
    rotulo="Especifique o responsável pela matrícula:",
    depende_de=Dependencia(
        chave="resp_mat_opcao",
        valor="Outro"
    )
)
preenchedora = Campo(
    chave="preenchido_por",
    rotulo="Ficha preenchida por:",
    valor_padrao="Secretaria Escolar"
)
logo_url = Campo(
    chave="logo_src",
    rotulo="URL da Logo (opcional):"
)


linha_escolares_1 = Linha(proporcoes=(1, 2, 1, 1), campos=(ano_letivo, curso, série, turma,))
linha_escolares_2 = Linha(proporcoes=(2, 1, 2), campos=(num_matrícula, data_matrícula, responsável_matrícula,))
linha_escolares_3 = Linha(proporcoes=(1,), campos=(responsável_matrícula_outro,))
linha_escolares_4 = Linha(proporcoes=(1, 1), campos=(preenchedora, logo_url,))

linhas_escolares = (
    linha_escolares_1,
    linha_escolares_2,
    linha_escolares_3,
    linha_escolares_4,
)
