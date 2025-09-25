class Google:

    url = 'https://accounts.google.com/'

    @property
    def xpaths(self):
        return {
            'input email' : '//*[@id="identifierId"]',
            'avançar email' : '//*[@id="identifierNext"]/div/button/span',
            'input senha': '//*[@id="password"]/div[1]/div/div[1]/input',
            'feedback': '//*[@id="c0"]',
            'avançar senha' : '//*[@id="passwordNext"]/div/button/div[3]',
            'alerta' : '//*[@id="c0"]'
        }

    @property
    def css_selectors(self) -> dict[str, str]:
        return {
            'input' : '#identifierId'
        }
