import os
import pandas as pd

path_pasta_geral = r'C:\Users\meren\OneDrive - Secretaria de Estado da Educação\Secretaria\Estudantes'
path_database = r'C:\Users\meren\OneDrive - Secretaria de Estado da Educação\SIGE\Database.xlsx'
path_cancelados = r'C:\Users\meren\OneDrive - Secretaria de Estado da Educação\Secretaria\Matrículas canceladas 2026.xlsx'

df_cancelados = pd.read_excel(path_cancelados)
df_cancelados['Matrícula'] = df_cancelados['Matrícula'].replace(['\xa0', '-'], ['', ''], regex=True)

matrícula = df_cancelados['Matrícula']
estudante = df_cancelados['Nome']
série = df_cancelados['Série']

dicio = dict(zip(matrícula, estudante, série))
for i in dicio:
    print(f'{i = }')