import pandas as pd
import os
from config.settings import MARCA, FREQ, HORIZON, MODEL_CONFIGS, DATA_INICIO_BASE

# Função para salvar as variáveis em um CSV
# variaveis_futuras e variaveis_historicas devem ser passadas como listas

def salvar_variaveis_csv(marca, freq, horizon, variaveis_futuras, variaveis_historicas, data_inicio_base, pasta_saida='outputs'):
    if not os.path.exists(pasta_saida):
        os.makedirs(pasta_saida)

    # Criar um DataFrame com as variáveis
    df_variaveis = pd.DataFrame({
        'Marca': [marca],
        'Freq': [freq],
        'Horizon': [horizon],
        'Variáveis Futuras': [', '.join(variaveis_futuras) if variaveis_futuras else ''],
        'Variáveis Históricas': [', '.join(variaveis_historicas) if variaveis_historicas else ''],
        'Data de Início Base': [data_inicio_base]
    })

    # Caminho para o arquivo CSV
    arquivo_csv = os.path.join(pasta_saida, f'variaveis_configuracoes_{marca}.csv')
    
    # Salvar o DataFrame como CSV
    df_variaveis.to_csv(arquivo_csv, index=False)
    print(f"Variáveis salvas com sucesso em {arquivo_csv}") 