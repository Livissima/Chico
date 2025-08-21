class NetEscola:

    url = 'https://netescola.educacao.go.gov.br/#PrimeiroAcesso'

    @property
    def xpaths(self):
        return {
            'matrícula' : '/html/body/div[1]/div[2]/div/form/div/div/div/div[2]/input',
            'nascimento' : '/html/body/div[1]/div[2]/div/form/div/div/div/div[3]/input',
            'pesquisar' : '/html/body/div[1]/div[2]/div/form/div/div/span/button',
            'email' : '/html/body/div[1]/div[2]/div/div[2]/div[2]/div[1]/div/div[2]/div[2]/div[1]/div/input',
            'email2' : '/html/body/div[1]/div[2]/div/div[2]/div[2]/div[1]/div/div[2]/div[2]/div[2]/div/input',
            'senha' : '/html/body/div[1]/div[2]/div/div[2]/div[2]/div[3]/div[2]/div/div[1]/div/input',
            'senha2' : '/html/body/div[1]/div[2]/div/div[2]/div[2]/div[3]/div[2]/div/div[2]/div/input',
            'concordo' : '/html/body/div[1]/div[2]/div/div[2]/div[2]/div[4]/div[1]/div[1]/label/input',
            'salvar'   : '/html/body/div[1]/div[2]/div/div[2]/div[2]/div[4]/div[1]/div[3]/button'
        }

    @property
    def caminhos(self) -> dict[str, list[tuple]]:
        xpaths = self.xpaths

        caminhos = {
            '' : [()]
        }
        return caminhos
