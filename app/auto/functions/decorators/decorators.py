#apenas alguns testes


import time
from functools import wraps

def cronometrar(função) :
    @wraps(função)
    def wrapper(*args, **kwargs):



        início = time.time()
        função(*args, **kwargs)
        fim = time.time()
        print(f'Duração da sessão: {fim - início:.3f} segundos.')

    return wrapper


def dbg(função) :
    #modelo de decorator cru
    wraps(função)

    def wrapper(*args, **kwargs) :
        nome_função = função.__qualname__
        função(*args, **kwargs)

    return wrapper
