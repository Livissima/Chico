from app.config.settings.functions import normalizar_diacrítica

class Acessos:

    @staticmethod
    def _obter_senha_email_padrão_seduc(linha):
        nomes = [normalizar_diacrítica(n) for n in linha['Estudante'].strip().split()]

        primeira_letra = nomes[0][0].upper()
        ultima_letra = nomes[-1][0].lower()
        data_nascimento = linha['Data de Nascimento'].strftime('%d%m%Y')
        return f'{primeira_letra}{ultima_letra}{data_nascimento}'

    @staticmethod
    def _gerar_senha_netescola_padrão_chico(linha):
        nome_splitado = [normalizar_diacrítica(n) for n in linha['Estudante'].strip().split()]

        primeiro_nome = nome_splitado[0]
        segundo_nome = nome_splitado[1] if len(nome_splitado) > 1 else ""

        if len(primeiro_nome) < 5:
            nome_final = primeiro_nome + segundo_nome
        else:
            nome_final = primeiro_nome

        return nome_final.lower()+'00'

    @staticmethod
    def _gerar_senha_email_padrão_chico(linha):
        preposições = ['das', 'dos', 'de', 'do', 'da']

        nome_splitado = [
            normalizar_diacrítica(n) for n in linha['Estudante'].strip().split() if n.lower() not in preposições
        ]

        primeiro_nome = nome_splitado[0].lower()
        segundo_nome = nome_splitado[1].lower()
        terceiro_nome = ''

        try:
            terceiro_nome = nome_splitado[2].lower()

        except IndexError:
            pass

        if len(primeiro_nome) >= 8 :
            return primeiro_nome

        elif len(primeiro_nome) + len(segundo_nome) >= 8 :
            return f'{primeiro_nome}{segundo_nome}'

        else:
            return f'{primeiro_nome}{segundo_nome}{terceiro_nome}'


