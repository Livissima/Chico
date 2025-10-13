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
            'modulações' : self._modulações
        }

    @property
    def _ir_lápis_docs(self):
        return 'lápis', 'documentos'

    @property
    def _ir_relatórios(self):
        return 'lápis docs', 'relatórios'

    @property
    def _fichas(self):
        return [
            self._ir_lápis_docs,
            (*self._ir_relatórios, '_xpath'),
            (*self._ir_relatórios, 'dados cadastrais', '_xpath'),
            (*self._ir_relatórios, 'dados cadastrais', 'ficha do aluno')
        ]

    @property
    def _contatos(self):
        return [
            self._ir_lápis_docs,
            (*self._ir_relatórios, '_xpath'),
            (*self._ir_relatórios, 'dados cadastrais', '_xpath'),
            (*self._ir_relatórios, 'dados cadastrais', 'contatos dos alunos')
        ]

    @property
    def _situações(self):
        return [
            self._ir_lápis_docs,
            (*self._ir_relatórios, '_xpath'),
            (*self._ir_relatórios, 'alunos', '_xpath'),
            (*self._ir_relatórios, 'alunos', 'situação')
        ]

    @property
    def _gêneros(self):
        return [
            self._ir_lápis_docs,
            (*self._ir_relatórios, '_xpath'),
            (*self._ir_relatórios, 'acomp. pedagógico', '_xpath'),
            (*self._ir_relatórios, 'acomp. pedagógico', 'alunos por idade')
        ]

    @property
    def _quantitativo(self):
        return [
            self._ir_lápis_docs,
            (*self._ir_relatórios, '_xpath'),
            (*self._ir_relatórios, 'alunos', '_xpath'),
            (*self._ir_relatórios, 'alunos', 'quantitativo')
        ]

    @property
    def _sondagem(self):
        return [
            self._ir_lápis_docs,
            (*self._ir_relatórios, '_xpath'),
            (*self._ir_relatórios, 'dados cadastrais', '_xpath'),
            (*self._ir_relatórios, 'dados cadastrais', 'turmas')
        ]

    @property
    def _ficha_aluno(self):
        return [
            ('lápis', 'alunos'), ('alunos', 'ficha do aluno')
        ]

    @property
    def _modulações(self):
        return [
            self._ir_lápis_docs,
            (*self._ir_relatórios, '_xpath'),
            (*self._ir_relatórios, 'dossiê do servidor', '_xpath'),
            (*self._ir_relatórios, 'dossiê do servidor', 'modulação'),
            (*self._ir_relatórios, 'dossiê do servidor', 'geral')
        ]