from os import PathLike

from app.config.parâmetros.gerenciadordeestado import ConfiguraçãoBase
from app.config.parâmetros.getters.dias_letivos import DiasLetivos
from app.config.parâmetros.getters.modulação_servidor import ModulaçãoServidor
from app.config.parâmetros.getters.prévias import Prévias
from app.config.parâmetros.getters.tempo import tempo
from app.config.parâmetros.getters.turmasséries import TurmasSéries



class IniciadorConfiguraçãoBase:

    @staticmethod
    def configuração(path: PathLike) -> ConfiguraçãoBase :
        ano_atual = tempo.ano_atual
        prévias = Prévias(path)
        dias_letivos_obj = DiasLetivos(path, ano_atual)
        modulacoes_obj = ModulaçãoServidor(path)

        return ConfiguraçãoBase(
            diretorio_base=path,
            ano_letivo=ano_atual,
            nome_ue=prévias.nome_ue,
            turmas_disponiveis=tuple(prévias.turmas),
            series_disponiveis=tuple(TurmasSéries(prévias).lista_séries),
            lista_dias_letivos=tuple(dias_letivos_obj.lista_dias_letivos),
            dicionario_dias_letivos=dias_letivos_obj.dicionário_dias_letivos,
            modulacoes=modulacoes_obj.modulações,
            resumo=prévias.resumo
        )
