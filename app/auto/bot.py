from app.config.settings.functions import normalizar_unicode, normalizar_dicionário
from app.auto.tasks.registrotasks import RegistroTasks
from selenium import webdriver


class Bot:
    #todo: implementar multithreading / assynch
    def __init__(self, tarefa: str, **kwargs) :
        tarefa_normalizada = normalizar_unicode(tarefa)

        print(f"\n🤖 Bot iniciando: '{tarefa}'")
        print(f"   Argumentos: {list(kwargs.keys())}\n")

        # ← Criar navegador AQUI
        navegador = webdriver.Chrome()
        kwargs['navegador'] = navegador

        # ← DEPOIS validar
        valido, mensagem = RegistroTasks.validar_argumentos(tarefa_normalizada, kwargs)
        if not valido :
            navegador.quit()
            raise ValueError(f"❌ Erro de validação: {mensagem}")

        try :
            task_class = RegistroTasks.obter(tarefa_normalizada)
            print(f"🚀 Executando {task_class.__name__}...\n")
            task_class(**kwargs)

        except Exception as e :
            print(f"\n❌ Erro durante execução: {e}")
            raise

        finally :
            navegador.quit()

