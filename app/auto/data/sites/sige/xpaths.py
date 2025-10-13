class Xpaths:

    @property
    def xpaths(self):
        return {
            'misc' : self._misc,
            'ficha aluno' : self._ficha_aluno,
            'resumo' : self._resumo,
            'lápis' : self._lápis,
            'alunos' : self._alunos,
            'lápis docs' : self._lápis_docs
        }

    @property
    def _misc(self):
        return {
            'input id' : '/html/body/div[3]/div/form/input[1]',
            'input senha' : '/html/body/div[3]/div/form/input[2]',
            'entrar' : '/html/body/div[3]/div/form/input[3]',
            'alerta' : '/html/body/div[11]/div/a',
            'marcar todos' : '/html/body/div[8]/form/table/tbody/tr[9]/td/table/tbody/tr[1]/td[1]/input',
            'composição' : '/html/body/div[8]/form/table[1]/tbody/tr[1]/td[2]/select',
            'série' : '/html/body/div[8]/form/table[1]/tbody/tr[2]/td[2]/select',
            'turma' : '/html/body/div[8]/form/table[1]/tbody/tr[5]/td[2]/select',
            'turno' : '/html/body/div[8]/form/table[1]/tbody/tr[3]/td[2]/select',
            'input data' : '/html/body/div[8]/form/table/tbody/tr[6]/td[2]/input'
        }

    @property
    def _ficha_aluno(self):
        return {
            'matrícula' : '/html/body/div[8]/form/table[1]/tbody/tr[2]/td/table/tbody/tr[2]/td[2]/input[1]',
            'click fora' : '/html/body/div[8]/form/table[1]/tbody/tr[2]/td/table/tbody/tr[2]/td[2]',
            'foto' : '/html/body/div[8]/form/table[1]/tbody/tr[2]/td/table/tbody/tr[1]/td/table/tbody/tr[1]/td/div/img',
            'limpar' : '/html/body/div[8]/form/table[9]/tbody/tr/td/table/tbody/tr/td/input[4]'
        }

    @property
    def _resumo(self):
        quantitativo = {
            'total geral' : '/html/body/div[8]/form/table/tbody/tr[2]/td[2]/input[3]',
            'input data' : '/html/body/div[8]/form/table/tbody/tr[4]/td[2]/input',
            'total normal' : '/html/body/table[3]/tbody/tr[8]/td[6]/strong'
        }
        turmas = {
            'ativas' : '/html/body/div[8]/form/table/tbody/tr/td/table/tbody/tr[6]/td[2]/input[1]',
            'input data' : '/html/body/div[8]/form/table/tbody/tr[6]/td[2]/input'
        }

        return {
            'quantitativo' : quantitativo,
            'turmas' : turmas
        }

    @property
    def _lápis(self):
        return {
            'alunos' : '/html/body/div[7]/ul/li[1]/h4/a',
            'movimentação' : '/html/body/div[7]/ul/li[2]/h4/a',
            'período letivo' : '/html/body/div[7]/ul/li[3]/h4/a',
            'documentos' : '/html/body/div[7]/ul/li[4]/h4/a'
        }

    @property
    def _alunos(self):
        return {
            'consultar' : '/html/body/div[7]/ul/li[1]/ul/li[1]/a',
            'ficha do aluno' : '/html/body/div[7]/ul/li[1]/ul/li[2]/a'
        }

    @property
    def _lápis_docs(self):
        return {
            'documentos' : self.__documentos,
            'relatórios' : self.__relatórios
        }

    @property
    def __documentos(self):
        return {
            '_xpath' : '/html/body/div[7]/ul/li[4]/ul/li[1]/a',
            'acomp pedagógico' : '/html/body/div[7]/ul/li[4]/ul/li[1]/ul/li[1]/a',
            'livro de matrícula' : '/html/body/div[7]/ul/li[4]/ul/li[1]/ul/li[2]/a',
            'ata' : '/html/body/div[7]/ul/li[4]/ul/li[1]/ul/li[3]/a'
        }

    @property
    def __relatórios(self):
        xpath_relatórios = '/html/body/div[7]/ul/li[4]/ul/li[2]/a'

        dados_cadastrais = {
            '_xpath' : '/html/body/div[7]/ul/li[4]/ul/li[2]/ul/li[1]/a',
            'dados pessoais' : '/html/body/div[7]/ul/li[4]/ul/li[2]/ul/li[1]/ul/li[1]/a',
            'ficha do aluno' : '/html/body/div[7]/ul/li[4]/ul/li[2]/ul/li[1]/ul/li[2]/a',
            'contatos dos alunos' : '/html/body/div[7]/ul/li[4]/ul/li[2]/ul/li[1]/ul/li[6]/a',
            'turmas' : '/html/body/div[7]/ul/li[4]/ul/li[2]/ul/li[1]/ul/li[5]/a'
        }

        alunos = {
            '_xpath' : '/html/body/div[7]/ul/li[4]/ul/li[2]/ul/li[2]/a',
            'situação' : '/html/body/div[7]/ul/li[4]/ul/li[2]/ul/li[2]/ul/li[2]/a',
            'quantitativo' : '/html/body/div[7]/ul/li[4]/ul/li[2]/ul/li[2]/ul/li[1]/a'
        }

        acomp_pedagógico = {
            '_xpath' : '/html/body/div[7]/ul/li[4]/ul/li[2]/ul/li[3]/a',
            'alunos por idade' : '/html/body/div[7]/ul/li[4]/ul/li[2]/ul/li[3]/ul/li[6]/a'
        }

        dossiê_do_servidor = {
            '_xpath' : '/html/body/div[7]/ul/li[4]/ul/li[2]/ul/li[5]/a',
            'modulação' : '/html/body/div[7]/ul/li[4]/ul/li[2]/ul/li[5]/ul/li[2]/a',
            'geral' : '/html/body/div[7]/ul/li[4]/ul/li[2]/ul/li[5]/ul/li[2]/ul/li[2]/a',
            'cpf' : '//*[@id="txtCPF"]'
        }

        return {
            '_xpath' : xpath_relatórios,
            'dados cadastrais' : dados_cadastrais,
            'alunos' : alunos,
            'acomp. pedagógico' : acomp_pedagógico,
            'dossiê do servidor' : dossiê_do_servidor
        }

