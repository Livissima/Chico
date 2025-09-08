import concurrent.futures
import threading

from app.ui.screens.janela import Janela


# with concurrent.futures.ThreadPoolExecutor() as executor:
#     thread_janela = executor.submit(Janela)


# thread_janela = threading.Thread(
#     target=Janela,
#     daemon=False
# )
# thread_janela.start()

Janela()
