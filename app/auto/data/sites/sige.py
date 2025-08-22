from app.utils.env_config import ID_SIGE, SENHA_SIGE


class Sige:

    url = 'https://sige.educacao.go.gov.br/sige/login.asp'

    #todo usar f-string nesse path para flexibilizar. Na verdade, não faz sentido que uma classe do SIGE tenha esse
    # tipo de informação ou méthodo, fazendo mais sentido elaborar uma classe própria para credenciais.

    @property
    def credenciais(self):
        return {
            'id' : ID_SIGE,
            'senha' :  SENHA_SIGE
        }

    @property
    def css_selectors(self) -> dict[str, str]:
        return {
            'voltar' : '#barraImpressao > img:nth-child(1)'
        }

    @property
    def ids(self) -> dict[str:str]:
        return {
            'gerar': 'gerarRel',
            'composição': 'cmbComposicao',
            'turno': 'cmbTurno',
            'turma': 'cmbTurma',
            'série': 'cmbSerie'
        }

    @property
    def xpaths(self):
        return {
            'misc' : {'input id': '/html/body/div[3]/div/form/input[1]',
                      'input senha': '/html/body/div[3]/div/form/input[2]',
                      'entrar': '/html/body/div[3]/div/form/input[3]',
                      'alerta': '/html/body/div[11]/div/a',
                      'marcar todos': '/html/body/div[8]/form/table/tbody/tr[9]/td/table/tbody/tr[1]/td[1]/input',
                      'composição': '/html/body/div[8]/form/table[1]/tbody/tr[1]/td[2]/select',
                      'série': '/html/body/div[8]/form/table[1]/tbody/tr[2]/td[2]/select',
                      'turma': '/html/body/div[8]/form/table[1]/tbody/tr[5]/td[2]/select',
                      'turno': '/html/body/div[8]/form/table[1]/tbody/tr[3]/td[2]/select',
                      'input data' : '/html/body/div[8]/form/table/tbody/tr[6]/td[2]/input'
            },
            'lápis': {'alunos': '/html/body/div[7]/ul/li[1]/h4/a',
                      'movimentação': '/html/body/div[7]/ul/li[2]/h4/a',
                      'período letivo': '/html/body/div[7]/ul/li[3]/h4/a',
                      'documentos': '/html/body/div[7]/ul/li[4]/h4/a'
            },
            'alunos': {'consultar': '/html/body/div[7]/ul/li[1]/ul/li[1]/a',
                       'ficha do aluno': '/html/body/div[7]/ul/li[1]/ul/li[2]/a'
            },
            'lápis docs': {'documentos': {'_xpath': '/html/body/div[7]/ul/li[4]/ul/li[1]/a',
                                          'acomp pedagógico': '/html/body/div[7]/ul/li[4]/ul/li[1]/ul/li[1]/a',
                                          'livro de matrícula': '/html/body/div[7]/ul/li[4]/ul/li[1]/ul/li[2]/a',
                                          'ata': '/html/body/div[7]/ul/li[4]/ul/li[1]/ul/li[3]/a'
            },
                           'relatórios': {'_xpath': '/html/body/div[7]/ul/li[4]/ul/li[2]/a',
                                          'dados cadastrais': {'_xpath': '/html/body/div[7]/ul/li[4]/ul/li[2]/ul/li[1]/a',
                                                               'dados pessoais': '/html/body/div[7]/ul/li[4]/ul/li[2]/ul/li[1]/ul/li[1]/a',
                                                               'ficha do aluno': '/html/body/div[7]/ul/li[4]/ul/li[2]/ul/li[1]/ul/li[2]/a',
                                                               'contatos dos alunos': '/html/body/div[7]/ul/li[4]/ul/li[2]/ul/li[1]/ul/li[6]/a'
                                          },
                                          'alunos': {'_xpath': '/html/body/div[7]/ul/li[4]/ul/li[2]/ul/li[2]/a',
                                                     'situação': '/html/body/div[7]/ul/li[4]/ul/li[2]/ul/li[2]/ul/li[2]/a'
                                          },
                                          'acomp. pedagógico': {'_xpath': '/html/body/div[7]/ul/li[4]/ul/li[2]/ul/li[3]/a',
                                                                'alunos por idade': '/html/body/div[7]/ul/li[4]/ul/li[2]/ul/li[3]/ul/li[6]/a'
                                          }
                           }
            }
        }
    @property
    def caminhos(self) -> dict[str, list[tuple]]:

        xpaths = self.xpaths

        caminhos = {
            'prefixos' : [(docs := ('lápis', 'documentos')),       (prefixo := ('lápis docs', 'relatórios'))],

            'fichas' : [docs, (*prefixo, '_xpath'),      (*prefixo, 'dados cadastrais', '_xpath'),
                        (*prefixo, 'dados cadastrais', 'ficha do aluno')
                        ],

            'contatos' : [docs, (*prefixo, '_xpath'), (*prefixo, 'dados cadastrais', '_xpath'),
                          (*prefixo, 'dados cadastrais', 'contatos dos alunos')
                          ],

            'situações' : [docs, (*prefixo, '_xpath'), (*prefixo, 'alunos', '_xpath'),
                           (*prefixo, 'alunos', 'situação')
                           ],
            'gêneros' : [docs, (*prefixo, '_xpath'), (*prefixo, 'acomp. pedagógico', '_xpath'),
                         (*prefixo, 'acomp. pedagógico', 'alunos por idade')
                         ]
        }

        return caminhos

