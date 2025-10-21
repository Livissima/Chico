import datetime


class Tempo:

    @property
    def hoje(self):
        return datetime.datetime.now().strftime('%d/%m/%Y')

    @property
    def hoje_dia(self):
        return datetime.datetime.now().strftime('%d')

    @property
    def agora(self):
        return datetime.datetime.now()

    @property
    def ano_atual(self) -> int:
        return datetime.datetime.now().year



tempo = Tempo()
