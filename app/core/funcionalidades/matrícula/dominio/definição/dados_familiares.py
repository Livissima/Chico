from __future__ import annotations

from app.core.funcionalidades.matrícula.dominio.campos import Campo, Dependencia
from app.core.funcionalidades.matrícula.dominio.definição.alternativas import NUCLEO_FAMILIAR
from app.core.funcionalidades.matrícula.dominio.tipos import TipoCampo

nome_responsável = Campo("responsavel_nome", "Nome do responsável")
dn_responsável = Campo("responsavel_dn", "Data de Nascimento (Responsável)")
responsável_profissão  = Campo("responsavel_profissao", "Profissão (Responsável)")
responsável_relação = Campo("responsavel_relacao", "Tipo de vínculo (mãe, pai, tutor legal etc)")
núcleo_familiar = Campo(
    "nucleo_opcoes", "Quem mora com o(a) estudante", tipo=TipoCampo.MULTISELECT, opcoes=NUCLEO_FAMILIAR, marcador="nuc"
)
núcleo_outros = Campo(
    "nuc_outros_texto", 'Especifique "Outros" no núcleo familiar', depende_de=Dependencia("nucleo_opcoes", "Outros")
)
