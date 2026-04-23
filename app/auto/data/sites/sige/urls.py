from dataclasses import dataclass


@dataclass(frozen=True)
class SigeUrls:
    tela_login: str = 'https://sige.educacao.go.gov.br/sige/login.asp'
    #     #todo: Apenas a propriedade de tela_login está em uso. O resto é rascunho.
    #     # Como o bot funcionava com caminhos (sequências de xpaths) e agora passa a ser com urls,
    #     # ainda preciso adequar as classes de data para suportarem as múltiplas urls,
    #     # dado que até então, elas só suportavam a url inicial.

    tela_fichas: str =  r'https://sige.educacao.go.gov.br/sige/modulos/Academico/Relatorios/ave_fichadoaluno_con.asp'
    contatos: str =  r'https://sige.educacao.go.gov.br/sige/modulos/Academico/Relatorios/Ave_telefones_con.asp'
    situações: str =  r'https://sige.educacao.go.gov.br/sige/modulos/Academico/Relatorios/Ave_situacao_con.asp'
    tela_gêneros: str =  r'https://sige.educacao.go.gov.br/sige/modulos/Academico/Relatorios/Ave_alunosPorIdade_con.asp'
    tela_quantitativo: str =  r'https://sige.educacao.go.gov.br/sige/modulos/Academico/Relatorios/Ave_quantitativoAlunos_con.asp'
    tela_sondagem: str =  r'https://sige.educacao.go.gov.br/sige/modulos/Academico/Relatorios/Ave_turmas_con.asp'
    tela_ficha_do_aluno: str =  'https://sige.educacao.go.gov.br/sige/modulos/academico/ave_aluno_cad.asp'
    tela_modulações: str =  r'https://sige.educacao.go.gov.br/sige/modulos/Dossie/Relatorios/ddv_docencia_con.asp'
