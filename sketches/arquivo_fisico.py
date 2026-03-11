
import pandas as pd
import unicodedata

path_df_caixas = r'C:\Users\meren\OneDrive - Secretaria de Estado da Educação\Controle do Arquivo Físico.xlsx'
path_df_pastas_a_serem_arquivadas = r'C:\Users\meren\OneDrive - Secretaria de Estado da Educação\Situação Históricos.xlsx'
import pandas as pd
import unicodedata


# Função para normalizar texto (remover acentos e converter para maiúsculas)
def normalizar_nome(texto) :
    if pd.isna(texto) :
        return None
    # Normaliza o texto para a forma NFD (decomposição de caracteres)
    texto = unicodedata.normalize('NFD', str(texto))
    # Remove os acentos (mantém apenas caracteres não diacríticos)
    texto = ''.join(c for c in texto if unicodedata.category(c) != 'Mn')
    # Converte para maiúsculas
    return texto.upper()


# Carregar os dados
caixas_df = pd.read_excel(path_df_caixas, sheet_name='Reorganização')
pastas_df = pd.read_excel(path_df_pastas_a_serem_arquivadas, sheet_name='Est')

# Normalizar os nomes
caixas_df['Nome_Inicial_Normalizado'] = caixas_df['Nome Inicial'].apply(normalizar_nome)
caixas_df['Nome_Final_Normalizado'] = caixas_df['Nome Final'].apply(normalizar_nome)
pastas_df['Nome_Normalizado'] = pastas_df['Estudante'].apply(normalizar_nome)

# Ordenar as caixas
caixas_df = caixas_df.sort_values('Nome_Inicial_Normalizado').reset_index(drop=True)


# Função para encontrar a caixa correta
def encontrar_caixa(nome_normalizado) :
    if nome_normalizado is None :
        return None, "Nome nulo"

    if not isinstance(nome_normalizado, str) :
        return None, f"Tipo inválido: {type(nome_normalizado)}"

    for _, caixa in caixas_df.iterrows() :
        nome_inicial = caixa['Nome_Inicial_Normalizado']
        nome_final = caixa['Nome_Final_Normalizado']

        if not isinstance(nome_inicial, str) or not isinstance(nome_final, str) :
            continue

        if nome_inicial <= nome_normalizado <= nome_final :
            return caixa['Caixa'], "Encontrado"

    return None, "Fora do intervalo"


# Aplicar a função e capturar razões
resultados = pastas_df['Nome_Normalizado'].apply(encontrar_caixa)
pastas_df['Caixa'] = [resultado[0] for resultado in resultados]
pastas_df['Status'] = [resultado[1] for resultado in resultados]

# Análise detalhada das pastas sem caixa
sem_caixa = pastas_df[pastas_df['Caixa'].isnull()]

print("=== DIAGNÓSTICO DETALHADO ===")
print(f"\nTotal de pastas sem caixa: {len(sem_caixa)}")

# Mostrar as primeiras pastas sem caixa com informações detalhadas
print("\n--- PRIMEIRAS 10 PASTAS SEM CAIXA ---")
for idx, pasta in sem_caixa.head(10).iterrows() :
    print(f"\nNome: {pasta['Estudante']}")
    print(f"Nome Normalizado: {pasta['Nome_Normalizado']}")
    print(f"Status: {pasta['Status']}")

# Verificar os limites das caixas
print("\n--- LIMITES DAS CAIXAS ---")
print(
    f"Primeira caixa: {caixas_df.iloc[0]['Nome_Inicial_Normalizado']} a {caixas_df.iloc[0]['Nome_Final_Normalizado']}")
print(
    f"Última caixa: {caixas_df.iloc[-1]['Nome_Inicial_Normalizado']} a {caixas_df.iloc[-1]['Nome_Final_Normalizado']}")

# Verificar onde estão as pastas sem caixa em relação aos limites
print("\n--- POSIÇÃO DAS PASTAS SEM CAIXA ---")
primeiro_nome = caixas_df.iloc[0]['Nome_Inicial_Normalizado']
ultimo_nome = caixas_df.iloc[-1]['Nome_Final_Normalizado']

antes_primeiro = sem_caixa[sem_caixa['Nome_Normalizado'] < primeiro_nome]
depois_ultimo = sem_caixa[sem_caixa['Nome_Normalizado'] > ultimo_nome]
entre_caixas = sem_caixa[
    (sem_caixa['Nome_Normalizado'] >= primeiro_nome) & (sem_caixa['Nome_Normalizado'] <= ultimo_nome)]

print(f"Pastas antes do primeiro nome: {len(antes_primeiro)}")
print(f"Pastas depois do último nome: {len(depois_ultimo)}")
print(f"Pastas entre os limites mas sem caixa: {len(entre_caixas)}")

# Se houver pastas entre os limites mas sem caixa, verificar possíveis lacunas
if len(entre_caixas) > 0 :
    print("\n--- VERIFICANDO LACUNAS NAS CAIXAS ---")

    # Verificar sobreposições e lacunas
    for i in range(len(caixas_df) - 1) :
        fim_atual = caixas_df.iloc[i]['Nome_Final_Normalizado']
        inicio_proximo = caixas_df.iloc[i + 1]['Nome_Inicial_Normalizado']

        # Verificar se há lacuna entre caixas
        if fim_atual < inicio_proximo :
            pastas_na_lacuna = entre_caixas[
                (entre_caixas['Nome_Normalizado'] > fim_atual) & (entre_caixas['Nome_Normalizado'] < inicio_proximo)]
            if len(pastas_na_lacuna) > 0 :
                print(f"Lacuna entre caixa {i + 1} ({fim_atual}) e caixa {i + 2} ({inicio_proximo}):")
                for _, pasta in pastas_na_lacuna.head(3).iterrows() :
                    print(f"  - {pasta['Nome_Normalizado']}")

# Verificar se há problemas com caracteres especiais
print("\n--- CARACTERES ESPECIAIS ---")
caracteres_especiais = []
for nome in sem_caixa['Nome_Normalizado'] :
    if nome and any(not c.isalnum() and c not in ' .' for c in nome) :
        caracteres_especiais.append(nome)

if caracteres_especiais :
    print(f"Nomes com caracteres especiais: {caracteres_especiais[:5]}")

# Salvar relatório detalhado
sem_caixa[['Estudante', 'Nome_Normalizado', 'Status']].to_excel('pastas_sem_caixa_detalhado.xlsx', index=False)
print(f"\nRelatório detalhado salvo em 'pastas_sem_caixa_detalhado.xlsx'")

# Salvar resultado final (sem a coluna Status)
pastas_df_sem_status = pastas_df.drop('Status', axis=1)
pastas_df_sem_status.to_excel('pastas_com_caixas.xlsx', index=False)