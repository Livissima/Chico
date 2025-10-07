from app.config.env_config import USUÁRIOS_SIAP, IDS_SIAP, SENHAS_SIAP, TIPOS_SIAP


class Siap:
    url = 'https://siap.educacao.go.gov.br/'

    @property
    def credenciais(self):
        return {
            usuário : {'id' : _id, 'senha': senha, 'tipo' : tipo}
            for usuário, _id, senha , tipo in zip(USUÁRIOS_SIAP, IDS_SIAP, SENHAS_SIAP, TIPOS_SIAP)
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
            'diário' : {
                '_xpath' : '/html/body/form/div[4]/div[1]/span/div/div[2]/li[2]/a',
                'ano' : '/html/body/form/div[4]/div[2]/div/div[1]/div/div[1]/p[2]/input',
                'composição' : '/html/body/form/div[4]/div[2]/div/div[1]/div/div[2]/p[2]/select',
                'série' : '/html/body/form/div[4]/div[2]/div/div[1]/div/div[3]/p[2]/select',
                'bimestre' : '/html/body/form/div[4]/div[2]/div/div[1]/div/div[4]/p[2]/select',
                'turno' : '/html/body/form/div[4]/div[2]/div/div[1]/div/div[5]/p[2]/select',
                'disciplina' : '/html/body/form/div[4]/div[2]/div/div[1]/div/div[6]/p[2]/select',
                'botão listar' : '/html/body/form/div[4]/div[2]/div/p[2]/input[2]',
                'bloco resultados' : '/html/body/form/div[4]/div[2]/div/div[2]/div/div/div/div',
                'frequência' : '/html/body/form/div[4]/div[2]/div/p[3]/input[2]',
                'salvar' : '/html/body/form/div[4]/div[2]/div/p[2]/input[1]',
                'bt mês anterior' : '/html/body/form/div[4]/div[2]/div/div/div/div[4]/div[1]/div/div/div/div/div[1]',
                'mês' : '/html/body/form/div[4]/div[2]/div/div/div/div[4]/div[1]/div/div/div/div/select'

            },
            'salvar e próximo': '/html/body/form/div[4]/div[2]/div/p/input[1]',
            'data': '/html/body/form/div[4]/div[2]/div/div/div/div[4]/div[2]/div/div/div[1]/div'
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






