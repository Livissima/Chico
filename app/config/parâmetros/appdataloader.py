from app.config.parâmetros.parâmetros import EstadoApp
from app.config.settings.functions import ler_json


class AppDataLoader:

    @staticmethod
    def carregar_tudo(estado: EstadoApp):
        resumo = ler_json(estado.diretório_base / 'fonte' / 'resumo.json')
        estado.nome_ue = resumo.get('Nome UE', '')
        estado.turmas_disponíveis = resumo.get('Turmas', [])

        AppDataLoader._processar_estruturas_turmas(estado)

    @staticmethod
    def _processar_estruturas_turmas(estado: EstadoApp):
        from collections import defaultdict
        turmas_dict = defaultdict(list)
        for turma in estado.turmas_disponíveis:
            série = ''.join(filter(str.isdigit, turma))
            if série: turmas_dict[série].append(turma)

        estado.turmas_por_serie = {s: sorted(ts) for s, ts in sorted(turmas_dict.items())}
        estado.series_disponiveis = sorted(set(t[0] for t in estado.turmas_disponíveis))
