class Urls:
    #todo: Apenas a propriedade de tela_login está em uso. O resto é rascunho.
    # Como o bot funcionava com caminhos (sequências de xpaths) e agora passa a ser com urls,
    # ainda preciso adequar as classes de data para suportarem as múltiplas urls,
    # dado que até então, elas só suportavam a url inicial.



    @property
    def tela_login(self) -> str:
        return 'https://sige.educacao.go.gov.br/sige/login.asp'

    ################################################################
    ################################################################
    ################################################################
    @property
    def tela_fichas(self) -> str:
        return r'https://sige.educacao.go.gov.br/sige/modulos/Academico/Relatorios/ave_fichadoaluno_con.asp'

    @property
    def contatos(self) -> str:
        return r'https://sige.educacao.go.gov.br/sige/modulos/Academico/Relatorios/Ave_telefones_con.asp'

    @property
    def situações(self) -> str:
        return r'https://sige.educacao.go.gov.br/sige/modulos/Academico/Relatorios/Ave_situacao_con.asp'

    @property
    def tela_gêneros(self) -> str:
        return r'https://sige.educacao.go.gov.br/sige/modulos/Academico/Relatorios/Ave_alunosPorIdade_con.asp'

    @property
    def tela_quantitativo(self) -> str:
        return r'https://sige.educacao.go.gov.br/sige/modulos/Academico/Relatorios/Ave_quantitativoAlunos_con.asp'

    @property
    def tela_sondagem(self) -> str:
        return r'https://sige.educacao.go.gov.br/sige/modulos/Academico/Relatorios/Ave_turmas_con.asp'

    @property
    def tela_ficha_do_aluno(self) -> str:
        return 'https://sige.educacao.go.gov.br/sige/modulos/academico/ave_aluno_cad.asp'

    @property
    def tela_modulações(self) -> str:
        return r'https://sige.educacao.go.gov.br/sige/modulos/Dossie/Relatorios/ddv_docencia_con.asp'

