from dotenv import load_dotenv
import os
from pathlib import Path

load_dotenv()

ID_SIAP = os.getenv('ID_SIAP')
ID_SIGE = os.getenv('ID_SIGE')
SENHA_SIAP = os.getenv('SENHA_SIAP')
SENHA_SIGE = os.getenv('SENHA_SIGE')


# Validação básica (opcional)
# def validar_credenciais() :
#     """Verifica se todas as credenciais foram configuradas"""
#     credenciais = {
#         'ID' : ID, 'SENHA_SIAP' : SENHA_SIAP, 'SENHA_SIGE' : SENHA_SIGE
#     }
#
#     faltantes = [nome for nome, valor in credenciais.items() if not valor]
#
#     if faltantes :
#         raise ValueError(f"Credenciais faltando no .env: {', '.join(faltantes)}")
#
#
# # Chama a validação ao importar o módulo
# try :
#     validar_credenciais()
# except ValueError as e :
#     print(f"⚠️  Aviso: {e}")
#     print("⚠️  Configure o arquivo .env com suas credenciais")

