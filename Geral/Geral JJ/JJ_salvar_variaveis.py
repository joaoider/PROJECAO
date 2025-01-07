import pandas as pd
import os
import subprocess

from configuracoes_modelos.imports import *
from JJ_configuracoes import marca, freq, horizon, variaveis_futuras, variaveis_historicas, data_inicio_base


# Função para salvar as variáveis em um CSV
def salvar_variaveis_csv(marca, freq, horizon, variaveis_futuras, variaveis_historicas, pasta_saida='outputs'):
    if not os.path.exists(pasta_saida):
        os.makedirs(pasta_saida)

    # Criar um DataFrame com as variáveis
    df_variaveis = pd.DataFrame({
        'Marca': [marca],
        'Freq': [freq],
        'Horizon': [horizon],
        'Variáveis Futuras': [', '.join(variaveis_futuras)],  # Concatenar as variáveis futuras
        'Variáveis Históricas': [', '.join(variaveis_historicas)],  # Concatenar as variáveis históricas
        'Data de Início Base': [data_inicio_base]
    })

    # Caminho para o arquivo CSV
    arquivo_csv = os.path.join(pasta_saida, f'variaveis_configuracoes_{marca}.csv')
    
    # Salvar o DataFrame como CSV
    df_variaveis.to_csv(arquivo_csv, index=False)
    print(f"Variáveis salvas com sucesso em {arquivo_csv}")


# Salvar as variáveis em CSV
salvar_variaveis_csv(marca, freq, horizon, variaveis_futuras, variaveis_historicas)