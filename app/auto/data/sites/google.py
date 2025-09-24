class Google:

    url = 'https://accounts.google.com/v3/signin/identifier?dsh=S-719554540%3A1758746872244142&hl=pt-BR&ifkv=AfYwgwWqy-RvuM8GZs0ORmfb2WIShLGLLcCOg0um3ZyS9IziSl-uH-MEKU0Nu6Td1oiuw981XXUbiQ&service=mail&flowName=GlifWebSignIn&flowEntry=ServiceLogin'

    @property
    def xpaths(self):
        return {
            'input email' : '//*[@id="identifierId"]',
            'avançar email' : '//*[@id="identifierNext"]/div/button/span',
            'input senha': '//*[@id="password"]/div[1]/div/div[1]/input',
            'feedback': '//*[@id="c0"]',
            'avançar senha' : '//*[@id="passwordNext"]/div/button/div[3]'
        }

    @property
    def css_selectors(self) -> dict[str, str]:
        return {
            'input' : '#identifierId'
        }
