from dotenv import load_dotenv
import os

load_dotenv()
def obter(constante: str):
    return os.getenv(constante)



ID_SIGE = obter('ID_SIGE')
SENHA_SIGE = obter('SENHA_SIGE')


__USUÁRIOS_SIAP = [obter(f'USUARIO{i}') for i in range(0, 21) if obter(f'USUARIO{i}') != '' and obter(f'USUARIO{i}') is not None]
__IDS_SIAP      = [obter(f'ID_SIAP{i}') for i in range(0, 21) if obter(f'ID_SIAP{i}') != '' and obter(f'ID_SIAP{i}') is not None]
__SENHAS_SIAP   = [obter(f'SENHA_SIAP{i}') for i in range(0, 21) if obter(f'SENHA_SIAP{i}') != '' and obter(f'SENHA_SIAP{i}') is not None]
__TIPOS_SIAP    = [obter(f'TIPO{i}') for i in range(0, 21) if obter(f'TIPO{i}') != '' and obter(f'TIPO{i}') is not None]


CREDENCIAIS_SIAP = {
    usuário : {'id' : _id, 'senha': senha, 'tipo' : tipo}
    for usuário, _id, senha , tipo in zip(__USUÁRIOS_SIAP, __IDS_SIAP, __SENHAS_SIAP, __TIPOS_SIAP)
}

