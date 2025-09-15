import unicodedata

class Acessos:

    @staticmethod
    def normalizar_diacrítica(texto):
        return ''.join(
            c for c in unicodedata.normalize('NFKD', texto)
            if not unicodedata.combining(c)
        )

    def extrair_senha_padrão(self, linha):
        nomes = [self.normalizar_diacrítica(n) for n in linha['Estudante'].strip().split()]

        primeira_letra = nomes[0][0].upper()
        ultima_letra = nomes[-1][0].lower()
        dn = linha['Data de Nascimento'].strftime('%d%m%Y')
        return f'{primeira_letra}{ultima_letra}{dn}'

    def gerar_nova_senha(self, linha):
        nomes = [self.normalizar_diacrítica(n) for n in linha['Estudante'].strip().split()]

        primeiro = nomes[0]
        segundo = nomes[1] if len(nomes) > 1 else ""

        if len(primeiro) < 5:
            nome_final = primeiro + segundo
        else:
            nome_final = primeiro

        return nome_final.lower()+'00'

