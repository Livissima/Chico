from app.config.__metadata__ import PROJECT_NAME

class RegistradorDeTelas:
    REGISTRO_DE_TELAS = {}

    @classmethod
    def registrar(
            cls,
            nome_tela: str,
            título_da_janela: str,
            cabeçalho: str,
            descrição: str,
            mostrar_voltar: bool = True
    ):

        def wrapper(wrapped_class):
            cls.REGISTRO_DE_TELAS[nome_tela] = {
                'class' : wrapped_class,
                'metadata' : {
                    'título_janela' : f'{PROJECT_NAME} - {título_da_janela}',
                    'cabeçalho' : cabeçalho,
                    'descrição' : descrição,
                    'mostrar_voltar' : mostrar_voltar
                }
            }
            return wrapped_class
        return wrapper
