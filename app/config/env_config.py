from dotenv import load_dotenv
import os

load_dotenv()
def obter(constante: str):
    return os.getenv(constante)



ID_SIGE = obter('ID_SIGE')
SENHA_SIGE = obter('SENHA_SIGE')


USUÁRIOS_SIAP = [obter(f'USUARIO{i}') for i in range(0, 21) if obter(f'USUARIO{i}') != '' and obter(f'USUARIO{i}') is not None]
IDS_SIAP      = [obter(f'ID_SIAP{i}') for i in range(0, 21) if obter(f'ID_SIAP{i}') != '' and obter(f'ID_SIAP{i}') is not None]
SENHAS_SIAP   = [obter(f'SENHA_SIAP{i}') for i in range(0, 21) if obter(f'SENHA_SIAP{i}') != '' and obter(f'SENHA_SIAP{i}') is not None]
TIPOS_SIAP    = [obter(f'TIPO{i}') for i in range(0, 21) if obter(f'TIPO{i}') != '' and obter(f'TIPO{i}') is not None]

# print({
#             usuário : {'id' : _id, 'senha': senha, 'tipo' : tipo}
#             for usuário, _id, senha, tipo in zip(USUÁRIOS_SIAP, IDS_SIAP, SENHAS_SIAP, TIPOS_SIAP)
#         })



# print(USUÁRIOS_SIAP)
# print(IDS_SIAP)
# print(SENHAS_SIAP)
