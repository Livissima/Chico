class Caminhos:

    @property
    def caminhos(self):
        return {
            'fichas' : self._fichas,
            'contatos' : self._contatos,
            'situações' : self._situações,
            'gêneros' : self._gêneros,
            'quantitativo' : self._quantitativo,
            'sondagem' : self._sondagem,
            'ficha aluno' : self._ficha_aluno,
            'modulações' : self._modulações,
            'avaliação' : self._avaliação,
        }

    @property
    def _fichas(self):
        return r'https://sige.educacao.go.gov.br/sige/modulos/Academico/Relatorios/ave_fichadoaluno_con.asp'

    @property
    def _contatos(self):
        return r'https://sige.educacao.go.gov.br/sige/modulos/Academico/Relatorios/Ave_telefones_con.asp'

    @property
    def _situações(self):
        return r'https://sige.educacao.go.gov.br/sige/modulos/Academico/Relatorios/Ave_situacao_con.asp'

    @property
    def _gêneros(self):
        return r'https://sige.educacao.go.gov.br/sige/modulos/Academico/Relatorios/Ave_alunosPorIdade_con.asp'

    @property
    def _quantitativo(self):
        return r'https://sige.educacao.go.gov.br/sige/modulos/Academico/Relatorios/Ave_quantitativoAlunos_con.asp'

    @property
    def _sondagem(self):
        return r'https://sige.educacao.go.gov.br/sige/modulos/Academico/Relatorios/Ave_turmas_con.asp'

    @property
    def _ficha_aluno(self):
        return 'https://sige.educacao.go.gov.br/sige/modulos/academico/ave_aluno_cad.asp'

    @property
    def _modulações(self):
        return r'https://sige.educacao.go.gov.br/sige/modulos/Dossie/Relatorios/ddv_docencia_con.asp'

    @property
    def _avaliação(self):
        return 'https://sige.educacao.go.gov.br/sige/modulos/Academico/Ave_NotasFaltas_cad.asp'
