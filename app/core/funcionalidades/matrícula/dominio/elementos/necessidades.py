from __future__ import annotations

from app.core.funcionalidades.matrícula.dominio.campos import Campo, Dependencia, Linha
from app.core.funcionalidades.matrícula.dominio.elementos.alternativas import NAO_SIM, NECESSIDADES, SUFIXOS_NEE
from app.core.funcionalidades.matrícula.dominio.tipos import TipoCampo

possui_nee = Campo(
    "possui_nee", "Possui Necessidade Educacional Especial?", tipo=TipoCampo.RADIO, opcoes=NAO_SIM, valor_padrao="Não", marcador="nee"
)
nee_opções = Campo(
    "nee_opcoes", "Selecione as opções de NEE:", tipo=TipoCampo.MULTISELECT, opcoes=NECESSIDADES, marcador="nee",
    sufixos_marcador=SUFIXOS_NEE, depende_de=Dependencia("possui_nee", "Sim")
)
nee_outros = Campo(
    "nee_outro_texto", "Especifique a NEE (Outro):", depende_de=Dependencia("nee_opcoes", "Outro")
)
restrição_alimentar = Campo("restricao_alimentar", "Restrição alimentar (se houver):")


linha_nee_1 = Linha(proporcoes=(1,), campos=(possui_nee,))
linha_nee_2 = Linha(proporcoes=(1,), campos=(nee_opções,))
linha_nee_3 = Linha(proporcoes=(1,), campos=(nee_outros,))
linha_nee_4 = Linha(proporcoes=(1,), campos=(restrição_alimentar,))

linhas_nee = (linha_nee_1, linha_nee_2, linha_nee_3, linha_nee_4, )
