import json
from pathlib import Path

from app.core import ConsultaEstudantes


class ExportaçãoJSON:
    def __init__(self, consulta: ConsultaEstudantes, _path: Path):
        self._exportar(consulta, _path)

    def _exportar(self, consulta, _path):
        self._exportar_completo(consulta, _path)
        self._exportar_resumido(consulta, _path)

    @staticmethod
    def _exportar_completo(consulta, _path):
        dicionário_completo = consulta.to_dict(orient='list')

        caminho_completo = Path(_path, 'fonte', 'Database.json')
        with open(caminho_completo, 'w', encoding='utf-8') as arquivo :
            json.dump(dicionário_completo, arquivo, ensure_ascii=False, indent=0)

    @staticmethod
    def _exportar_resumido(consulta, _path):
        resumo = consulta[['Turma', 'Estudante', 'Matrícula']].copy()
        resumo = resumo.to_dict(orient='list')

        caminho_completo = Path(_path, 'fonte', 'Database resumida.json')
        with open(caminho_completo, 'w', encoding='utf-8') as arquivo :
            json.dump(resumo, arquivo, ensure_ascii=False, indent=0)
