import concurrent.futures
from app.ui.screens.janela import Janela


with concurrent.futures.ThreadPoolExecutor() as executor:
    thread_janela = executor.submit(Janela)



