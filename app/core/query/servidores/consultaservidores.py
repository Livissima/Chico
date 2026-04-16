from pathlib import Path
from pandas import DataFrame, ExcelWriter

from app.config.parâmetros import parâmetros
from app.core.query.leitura import Leitura



class ConsultaServidores:

    COLUNAS = (
        ('Dados Pessoais', 'coluna_1'),
        ('coluna_2', 'coluna_3'),
        ('coluna_4', 'coluna_5'),
        ('coluna_6', 'coluna_7')
    )

    def __init__(self, diretório_fonte: str | Path):

        print(f'class ConsultaServidores instanciada: {diretório_fonte = }')

        self.consulta = self._consultar(diretório_fonte)
        self._exportar(self.consulta)
        print(self.consulta)


    def _consultar(self, path: Path):

        leitura = Leitura(path, 'servidores').leitura

        return DataFrame(self._gerar_pessoas(leitura))


    def _gerar_pessoas(self, leitura: list[dict]):

        pessoa_atual = {}

        for registro in leitura:

            if self._é_início_de_pessoa(registro):

                if pessoa_atual:
                    yield pessoa_atual

                pessoa_atual = {}
                continue

            for campo, valor in self._extrair_campos(registro):
                pessoa_atual[campo] = valor

        if pessoa_atual:
            yield pessoa_atual


    def _é_início_de_pessoa(self, registro: dict):

        return registro.get('Dados Pessoais') == 'Dados Pessoais'


    def _extrair_campos(self, registro: dict):

        for chave_campo, chave_valor in self.COLUNAS:

            campo = registro.get(chave_campo)
            valor = registro.get(chave_valor)

            if campo and valor:
                yield campo, valor
    @staticmethod
    def _exportar(df: DataFrame):
        #todo: método provisório. A consulta não deveria saber se exportar. Preciso elaborar melhor as classes de exportação
        nome_xlsx = 'Servidores.xlsx'
        with ExcelWriter(Path(parâmetros.diretório_base, nome_xlsx), engine='xlsxwriter') as writer:
            df.to_excel(writer, sheet_name='Servidores atuais')

    def __getitem__(self, item) :
        return self.consulta[item]

    def __getattr__(self, name) :
        return getattr(self.consulta, name)

    def __len__(self) :
        return len(self.consulta)

