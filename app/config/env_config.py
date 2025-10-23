from dotenv import load_dotenv
import os

from app.config.tipos.cpf import CPF

load_dotenv()
def obter(_constante: str):
    constante = os.getenv(_constante)
    # if constante == '' or constante is None:
    #     return
    return os.getenv(_constante)



ID_SIGE = obter('ID_SIGE')
SENHA_SIGE = obter('SENHA_SIGE')


__USUÁRIOS_SIAP : list[CPF] = [obter(f'USUARIO{i}') for i in range(0, 21) if obter(f'USUARIO{i}') != '' and obter(f'USUARIO{i}') is not None]
__IDS_SIAP                  = [CPF(obter(f'ID_SIAP{i}')) for i in range(0, 21) if obter(f'ID_SIAP{i}') != '' and obter(f'ID_SIAP{i}') is not None]
__SENHAS_SIAP               = [obter(f'SENHA_SIAP{i}') for i in range(0, 21) if obter(f'SENHA_SIAP{i}') != '' and obter(f'SENHA_SIAP{i}') is not None]
__TIPOS_SIAP                = [obter(f'TIPO{i}') for i in range(0, 21) if obter(f'TIPO{i}') != '' and obter(f'TIPO{i}') is not None]

CREDENCIAIS_SIAP = {
    usuário : {'id' : _id, 'senha': senha, 'tipo' : tipo}
    for usuário, _id, senha , tipo in zip(__USUÁRIOS_SIAP, __IDS_SIAP, __SENHAS_SIAP, __TIPOS_SIAP)
}

print(f'{CREDENCIAIS_SIAP = }')