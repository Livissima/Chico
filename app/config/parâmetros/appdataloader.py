import os
from pathlib import Path
from app.config.parâmetros.parâmetros import Parâmetros, ANO_ATUAL
from app.config.settings.functions import ler_json
from app.config.parâmetros.getters.dias_letivos import DiasLetivos
from app.config.parâmetros.getters.modulação_servidor import ModulaçãoServidor
from app.config.parâmetros.getters.turmasséries import TurmasSéries


class AppDataLoader :
    @staticmethod
    def carregar_tudo(parâmetros: Parâmetros) :
        # 1. Resumo e Dados Básicos
        resumo = ler_json(parâmetros.diretório_base / 'fonte' / 'resumo.json')
        parâmetros.nome_ue = resumo.get('Nome UE', '')
        parâmetros.turmas_disponíveis = resumo.get('Turmas', [])
        parâmetros.turmas_selecionadas = parâmetros.turmas_disponíveis[:]
        parâmetros.estado_checkbox_turmas = {t : True for t in parâmetros.turmas_disponíveis}

        # 2. Estrutura de Turmas (Usando a lógica do Getter TurmasSéries)
        parâmetros.turma_por_série = TurmasSéries.gerar_dicionário_turmas_por_série(parâmetros.turmas_disponíveis)
        parâmetros.séries_disponíveis = TurmasSéries.gerar_lista_de_séries(parâmetros.turmas_disponíveis)

        # 3. Dias Letivos
        caminho_dias = parâmetros.diretório_base / 'fonte' / f'Dias Letivos {ANO_ATUAL}.json'
        dados_dias = ler_json(caminho_dias)
        lista, dicio = DiasLetivos.processar(dados_dias)
        parâmetros.lista_dias_letivos = lista
        parâmetros.dicionário_dias_letivos = dicio

        # 4. Modulações (Lê todos os arquivos da pasta e processa)
        pasta_modulacoes = parâmetros.diretório_base / 'fonte' / 'modulações'
        conteudos_modulacao = []
        if pasta_modulacoes.exists() :
            for arquivo in os.listdir(pasta_modulacoes) :
                if arquivo.endswith('.json') :
                    conteudos_modulacao.append(ler_json(pasta_modulacoes / arquivo))

        parâmetros.modulações = ModulaçãoServidor.processar(conteudos_modulacao)