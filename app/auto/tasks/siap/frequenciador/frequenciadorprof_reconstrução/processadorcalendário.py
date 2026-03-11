from selenium.webdriver import Chrome

from app.auto.tasks.siap.frequenciador import Calendário

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from app.auto.tasks.siap.frequenciador import ProcessadorDisciplina
    from app.auto.tasks.siap.frequenciador import LinhasDisciplinas


class ProcessadorCalendário:

    def __init__(
            self,
            master: Chrome,
            navegação,
            propriedades,
            # elemento_disciplinas,
            índice_linha,
            linhas_disciplinas: "LinhasDisciplinas"

    ) :

        self.elemento = self.processar(master, propriedades, navegação, índice_linha, linhas_disciplinas)

    @staticmethod
    def processar(master, pp, nv, índice, linhas_disciplinas):
        tentativas = 0

        while tentativas < 4 :
            try :
                return Calendário(nv).elemento

            except Exception as e :

                print(f'Erro na obtenção de calendário. Tentando novamente... {e}')
                tentativas += 1

                if tentativas >= 4 :
                    raise Exception('Não deu para obter o calendário.') from e

                linhas = linhas_disciplinas.elemento

                ProcessadorDisciplina(master, pp, nv, índice, linhas)

        return None


