import pandas as pd
import re


def valida_cpf(cpf):

    cpf = str(cpf)
    if len(cpf) != 11 or not cpf.isdigit():
        return False


    soma = sum(int(cpf[i]) * (10 - i) for i in range(9))
    digito_1 = (soma % 11)
    digito_1 = 0 if digito_1 < 2 else 11 - digito_1

    if digito_1 != int(cpf[9]):
        return False


    soma = sum(int(cpf[i]) * (11 - i) for i in range(10))
    digito_2 = (soma % 11)
    digito_2 = 0 if digito_2 < 2 else 11 - digito_2

    return digito_2 == int(cpf[10])


def extrai_numero_atualiza_endereco(endereco):

    if pd.isna(endereco) or endereco == '':
        return None, None


    match = re.search(r'\s+(\d+)$', endereco)
    if match:
        numero = match.group(1)
        endereco_atualizado = re.sub(r'\d+', '', endereco).strip()  # Remover todos os dígitos
        return endereco_atualizado, numero
    else:
        return endereco, None


df = pd.read_excel('Planilha_nao_filtrada', na_values=['', 'NA', 'nan'])


df = df.dropna(subset=['CPF'])


df['cpf_valido'] = df['CPF'].apply(valida_cpf)


df[['Endereco', 'numero']] = df['Endereco'].apply(extrai_numero_atualiza_endereco).apply(pd.Series)


df_filtrado = df[(df['cpf_valido']) & (df['numero'].notnull())]


df_filtrado.to_excel('test1_filtrado.xlsx', index=False, engine='openpyxl')

print("\nPlanilha filtrada salva em 'test3_filtrado.xlsx'.")
