from app.config.env_config import ID_SIAP, SENHA_SIAP

class Siap:
    url = 'https://siap.educacao.go.gov.br/'

    @property
    def credenciais(self):
        return {
            'id':    ID_SIAP,
            'senha': SENHA_SIAP
        }

    @property
    def xpaths(self) -> dict:
        return {
            'input login' : '/html/body/form/div[3]/div/div/div/div[2]/div[2]/div[1]/div[1]/div[1]/input',
            'input senha' : '/html/body/form/div[3]/div/div/div/div[2]/div[2]/div[1]/div[1]/div[2]/div[1]/input',
            'captcha' : '/html/body/form/div[3]/div/div/div/div[2]/div[2]/span[2]',
            'input captcha' : '/html/body/form/div[3]/div/div/div/div[2]/div[2]/div[1]/div[1]/div[2]/div[2]/input',
            'fail captcha'  : '/html/body/form/div[3]/div/div/div/div[2]/div[2]/span[1]',
            'botão login' : '/html/body/form/div[3]/div/div/div/div[2]/div[2]/div[1]/div[2]/input',
            'menu sistema' : '/html/body/form/div[3]/div/div[2]',
            'menu frequência' : '/html/body/form/div[4]/div[1]/span/div/div[2]/li[7]/a',
            'salvar e próximo': '/html/body/form/div[4]/div[2]/div/p/input[1]',
            'data': '/html/body/form/div[4]/div[2]/div/div/div/div[4]/div[2]/div/div/div[1]/div',
            # 'turmas' : { ## Estas referências hardcoded não são mais necessárias
            #     '6A': '/html/body/form/div[4]/div[2]/div/div/div/div[1]/div[1]/span',
            #     '6B': '/html/body/form/div[4]/div[2]/div/div/div/div[1]/div[2]/span',
            #     '7A': '/html/body/form/div[4]/div[2]/div/div/div/div[1]/div[3]/span',
            #     '7B': '/html/body/form/div[4]/div[2]/div/div/div/div[1]/div[4]/span',
            #     '8A': '/html/body/form/div[4]/div[2]/div/div/div/div[1]/div[5]/span',
            #     '8B': '/html/body/form/div[4]/div[2]/div/div/div/div[1]/div[6]/span',
            #     '9A': '/html/body/form/div[4]/div[2]/div/div/div/div[1]/div[7]/span',
            #     '6C': '/html/body/form/div[4]/div[2]/div/div/div/div[1]/div[8]/span'
            #     }
            }

    @property
    def ids(self) -> dict[str, str]:
        return {
            '' : ''
        }

    @property
    def caminhos(self) -> dict[str, list[tuple]]:
        xpaths = self.xpaths
        caminhos = {
            '' : [()]
        }
        return caminhos

    @property
    def css_selectors(self) -> dict[str, str]:
        return {
            '' : ''
        }





