import datetime


class Tempo:

    @property
    def hoje(self):
        return datetime.datetime.now().strftime('%d/%m/%Y')

    @property
    def agora(self):
        return datetime.datetime.now()

