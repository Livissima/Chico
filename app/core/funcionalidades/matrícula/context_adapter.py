class ContextAdapter:

    @staticmethod
    def conextualizar_jinja(dados: dict) -> dict:
        contexto = dados.copy()

        gênero = dados.get('gênero', '')
        contexto['gênero_m'] = 'X' if gênero == 'Masculino' else ''
        contexto['gênero_f'] = 'X' if gênero == 'Feminino' else ''

        cor_etnia = dados.get('cor_etnia', '')
        for opção in ['Branca', 'Preta', 'Parda', 'Indígena', 'Amarela', 'Não declarado']:
            chave_cor = f'cor_{opção.lower().replace(' ', '_').replace('í', 'i')}'
            contexto[chave_cor] = 'X' if cor_etnia == opção else ''

        return contexto
