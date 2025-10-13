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

    def gerar_senha_email(self, linha):
        nomes = [
            self.normalizar_diacrítica(n) for n in linha['Estudante'].strip().split() if n.lower() not in ['das', 'dos', 'de', 'do', 'da']]



        prenome = nomes[0].lower()
        sobrenome = nomes[1].lower()
        terceirome = ''

        try:
            terceirome = nomes[2].lower()
        except IndexError:
            pass


        if len(prenome) >= 8 :
            return prenome

        elif len(prenome) + len(sobrenome) >= 8 :
            return f'{prenome}{sobrenome}'

        else:
            return f'{prenome}{sobrenome}{terceirome}'


