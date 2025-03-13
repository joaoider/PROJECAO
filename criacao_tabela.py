# Databricks notebook source
import pandas as pd
from pyspark.sql import SparkSession
import os

# COMMAND ----------

# Criar DataFrame vazio com as colunas especificadas
df = pd.DataFrame(columns=['período', 'marca', 'modelo', 'categoria', 'venda'])

print(df)

# COMMAND ----------

# MAGIC %md
# MAGIC # GERAL

# COMMAND ----------

# MAGIC %md
# MAGIC ## DD

# COMMAND ----------

# DD

# Lista de caminhos possíveis
paths_DD = [
    'Geral/Geral DD/outputs/melhor_modelo_forecast_LSTM_mensal_DD.csv',
    'Geral/Geral DD/outputs/melhor_modelo_forecast_GRU_mensal_DD.csv',
    'Geral/Geral DD/outputs/melhor_modelo_forecast_NHITS_mensal_DD.csv',
    'Geral/Geral DD/outputs/melhor_modelo_forecast_NBEATSx_mensal_DD.csv'
]

# Variável para armazenar o caminho completo do arquivo encontrado
found_path_DD = None

# Verificar se os arquivos existem
for path in paths_DD:
    if os.path.exists(path):
        found_path_DD = path  # Salva o caminho completo do arquivo
        print(f"Arquivo encontrado: {found_path_DD}")
        break

if not found_path_DD:
    print("Nenhum arquivo correspondente foi encontrado.")

print(f"Caminho completo do arquivo encontrado: {found_path_DD}")

###############
#geral
data_DD = pd.read_csv(found_path_DD)

####################
# Renomear as colunas
data_DD = data_DD.rename(columns={data_DD.columns[0]: 'mes_ano', data_DD.columns[1]: 'DD'})

# COMMAND ----------

# Criar o novo DataFrame com os valores ajustados
df_DD = pd.DataFrame({
    'mes_ano': data_DD['mes_ano'],
    'marca': 'DD',
    'modelo': 'geral',
    'categoria': 'total',
    'venda': data_DD['DD']
})

df_DD

# COMMAND ----------

# MAGIC %md
# MAGIC ## LL

# COMMAND ----------

# LL

# Lista de caminhos possíveis
paths_LL = [
    'Geral/Geral LL/outputs/melhor_modelo_forecast_LSTM_mensal_LL.csv',
    'Geral/Geral LL/outputs/melhor_modelo_forecast_GRU_mensal_LL.csv',
    'Geral/Geral LL/outputs/melhor_modelo_forecast_NHITS_mensal_LL.csv',
    'Geral/Geral LL/outputs/melhor_modelo_forecast_NBEATSx_mensal_LL.csv'
]

# Variável para armazenar o caminho completo do arquivo encontrado
found_path_LL = None

# Verificar se os arquivos existem
for path in paths_LL:
    if os.path.exists(path):
        found_path_LL = path  # Salva o caminho completo do arquivo
        print(f"Arquivo encontrado: {found_path_LL}")
        break

if not found_path_LL:
    print("Nenhum arquivo correspondente foi encontrado.")

print(f"Caminho completo do arquivo encontrado: {found_path_LL}")

###############
#geral
data_LL = pd.read_csv(found_path_LL)

####################
# Renomear as colunas
data_LL = data_LL.rename(columns={data_LL.columns[0]: 'mes_ano', data_LL.columns[1]: 'LL'})

# COMMAND ----------

# Criar o novo DataFrame com os valores ajustados
df_LL = pd.DataFrame({
    'mes_ano': data_LL['mes_ano'],
    'marca': 'LL',
    'modelo': 'geral',
    'categoria': 'total',
    'venda': data_LL['LL']
})

df_LL

# COMMAND ----------

# MAGIC %md
# MAGIC ## JJ

# COMMAND ----------

# JJ

# Lista de caminhos possíveis
paths_JJ = [
    'Geral/Geral JJ/outputs/melhor_modelo_forecast_LSTM_mensal_JJ.csv',
    'Geral/Geral JJ/outputs/melhor_modelo_forecast_GRU_mensal_JJ.csv',
    'Geral/Geral JJ/outputs/melhor_modelo_forecast_NHITS_mensal_JJ.csv',
    'Geral/Geral JJ/outputs/melhor_modelo_forecast_NBEATSx_mensal_JJ.csv'
]

# Variável para armazenar o caminho completo do arquivo encontrado
found_path_JJ = None

# Verificar se os arquivos existem
for path in paths_JJ:
    if os.path.exists(path):
        found_path_JJ = path  # Salva o caminho completo do arquivo
        print(f"Arquivo encontrado: {found_path_JJ}")
        break

if not found_path_JJ:
    print("Nenhum arquivo correspondente foi encontrado.")

print(f"Caminho completo do arquivo encontrado: {found_path_JJ}")

###############
#geral
data_JJ = pd.read_csv(found_path_JJ)

####################
# Renomear as colunas
data_JJ = data_JJ.rename(columns={data_JJ.columns[0]: 'mes_ano', data_JJ.columns[1]: 'JJ'})

# COMMAND ----------

# Criar o novo DataFrame com os valores ajustados
df_JJ = pd.DataFrame({
    'mes_ano': data_JJ['mes_ano'],
    'marca': 'JJ',
    'modelo': 'geral',
    'categoria': 'total',
    'venda': data_JJ['JJ']
})

df_JJ

# COMMAND ----------

# Concatenar os DataFrames
df_final = pd.concat([df_DD, df_LL, df_JJ], ignore_index=True)

df_final

# COMMAND ----------

# MAGIC %md
# MAGIC # CATEGORIA_N1

# COMMAND ----------

# MAGIC %md
# MAGIC ## DD

# COMMAND ----------

# DD

# Lista de caminhos possíveis
paths_DD_categorian1 = [
    'Categoria/CATEGORIA_N1/DD/outputs/forecast_transposed_GRU_DD_categoria_final.csv',
    'Categoria/CATEGORIA_N1/DD/outputs/forecast_transposed_LSTM_DD_categoria_final.csv',
    'Categoria/CATEGORIA_N1/DD/outputs/forecast_transposed_NHITS_DD_categoria_final.csv',
    'Categoria/CATEGORIA_N1/DD/outputs/forecast_transposed_NBEATSx_DD_categoria_final.csv'
]

# Variável para armazenar o caminho completo do arquivo encontrado
found_path_DD_categoria = None

# Verificar se os arquivos existem
for path in paths_DD_categorian1:
    if os.path.exists(path):
        found_path_DD_categoria = path  # Salva o caminho completo do arquivo
        print(f"Arquivo encontrado: {found_path_DD_categoria}")
        break

if not found_path_DD_categoria:
    print("Nenhum arquivo correspondente foi encontrado.")

print(f"Caminho completo do arquivo encontrado: {found_path_DD_categoria}")

#################
#geral
data_DD_categoria = pd.read_csv(found_path_DD_categoria)

# Adicionar "LL_" às colunas, exceto 'mes_ano'
#data_DD_categoria.columns = ['mes_ano' if col == 'mes_ano' else f'DD_{col}' for col in data_DD_categoria.columns]

####################
# Renomear as colunas
data_DD_categoria = data_DD_categoria.rename(columns={data_DD_categoria.columns[0]: 'mes_ano'})


# Transformar o DataFrame
df_DD_categoria = data_DD_categoria.melt(
    id_vars=['mes_ano'],        # Coluna que será mantida fixa
    var_name='categoria',     # Nova coluna que conterá os nomes das colunas originais
    value_name='venda'     # Nova coluna que conterá os valores das colunas originais
)

df_DD_categoria['modelo'] = 'categoria geral'
df_DD_categoria['marca'] = 'DD'

# COMMAND ----------

# MAGIC %md
# MAGIC ## JJ

# COMMAND ----------

# JJ

# Lista de caminhos possíveis
paths_JJ_categorian1 = [
    'Categoria/CATEGORIA_N1/JJ/outputs/forecast_transposed_GRU_JJ_categoria_final.csv',
    'Categoria/CATEGORIA_N1/JJ/outputs/forecast_transposed_LSTM_JJ_categoria_final.csv',
    'Categoria/CATEGORIA_N1/JJ/outputs/forecast_transposed_NHITS_JJ_categoria_final.csv',
    'Categoria/CATEGORIA_N1/JJ/outputs/forecast_transposed_NBEATSx_JJ_categoria_final.csv'
]

# Variável para armazenar o caminho completo do arquivo encontrado
found_path_JJ_categoria = None

# Verificar se os arquivos existem
for path in paths_JJ_categorian1:
    if os.path.exists(path):
        found_path_JJ_categoria = path  # Salva o caminho completo do arquivo
        print(f"Arquivo encontrado: {found_path_JJ_categoria}")
        break

if not found_path_JJ_categoria:
    print("Nenhum arquivo correspondente foi encontrado.")

print(f"Caminho completo do arquivo encontrado: {found_path_JJ_categoria}")

#################
#geral
data_JJ_categoria = pd.read_csv(found_path_JJ_categoria)

# Adicionar "LL_" às colunas, exceto 'mes_ano'
#data_DD_categoria.columns = ['mes_ano' if col == 'mes_ano' else f'DD_{col}' for col in data_DD_categoria.columns]

####################
# Renomear as colunas
data_JJ_categoria = data_JJ_categoria.rename(columns={data_JJ_categoria.columns[0]: 'mes_ano'})


# Transformar o DataFrame
df_JJ_categoria = data_JJ_categoria.melt(
    id_vars=['mes_ano'],        # Coluna que será mantida fixa
    var_name='categoria',     # Nova coluna que conterá os nomes das colunas originais
    value_name='venda'     # Nova coluna que conterá os valores das colunas originais
)

df_JJ_categoria['modelo'] = 'categoria geral'
df_JJ_categoria['marca'] = 'JJ'

# COMMAND ----------

# MAGIC %md
# MAGIC ## LL

# COMMAND ----------

# LL

# Lista de caminhos possíveis
paths_LL_categorian1 = [
    'Categoria/CATEGORIA_N1/LL/outputs/forecast_transposed_GRU_LL_categoria_final.csv',
    'Categoria/CATEGORIA_N1/LL/outputs/forecast_transposed_LSTM_LL_categoria_final.csv',
    'Categoria/CATEGORIA_N1/LL/outputs/forecast_transposed_NHITS_LL_categoria_final.csv',
    'Categoria/CATEGORIA_N1/LL/outputs/forecast_transposed_NBEATSx_LL_categoria_final.csv'
]

# Variável para armazenar o caminho completo do arquivo encontrado
found_path_LL_categoria = None

# Verificar se os arquivos existem
for path in paths_LL_categorian1:
    if os.path.exists(path):
        found_path_LL_categoria = path  # Salva o caminho completo do arquivo
        print(f"Arquivo encontrado: {found_path_LL_categoria}")
        break

if not found_path_LL_categoria:
    print("Nenhum arquivo correspondente foi encontrado.")

print(f"Caminho completo do arquivo encontrado: {found_path_LL_categoria}")

#################
#geral
data_LL_categoria = pd.read_csv(found_path_LL_categoria)

# Adicionar "LL_" às colunas, exceto 'mes_ano'
#data_DD_categoria.columns = ['mes_ano' if col == 'mes_ano' else f'DD_{col}' for col in data_DD_categoria.columns]

####################
# Renomear as colunas
data_LL_categoria = data_LL_categoria.rename(columns={data_LL_categoria.columns[0]: 'mes_ano'})


# Transformar o DataFrame
df_LL_categoria = data_LL_categoria.melt(
    id_vars=['mes_ano'],        # Coluna que será mantida fixa
    var_name='categoria',     # Nova coluna que conterá os nomes das colunas originais
    value_name='venda'     # Nova coluna que conterá os valores das colunas originais
)

df_LL_categoria['modelo'] = 'categoria geral'
df_LL_categoria['marca'] = 'LL'

# COMMAND ----------

# Concatenar os DataFrames
df_final_categoria = pd.concat([df_DD_categoria, df_LL_categoria, df_JJ_categoria], ignore_index=True)

df_final_categoria

# COMMAND ----------

# MAGIC %md
# MAGIC # CATEGORIA_N1 ÚNICOS

# COMMAND ----------

# MAGIC %md
# MAGIC ## DD

# COMMAND ----------

# MAGIC %md
# MAGIC ### alfataiataria

# COMMAND ----------

# DD

# Lista de caminhos possíveis
paths_DD_categorian1 = [
    'CATEGORIA_N1 - único/DD - Alfaiataria/outputs/forecast_transposed_GRU_DD_categoria_alfaiataria_final.csv'#,
    #'Categoria/CATEGORIA_N1/DD/outputs/forecast_transposed_LSTM_DD_alfaiataria_final.csv',
    #'Categoria/CATEGORIA_N1/DD/outputs/forecast_transposed_NHITS_DD_alfaiataria_final.csv',
    #'Categoria/CATEGORIA_N1/DD/outputs/forecast_transposed_NBEATSx_DD_alfaiatariaa_final.csv'
]

# Variável para armazenar o caminho completo do arquivo encontrado
found_path_DD_categoria = None

# Verificar se os arquivos existem
for path in paths_DD_categorian1:
    if os.path.exists(path):
        found_path_DD_categoria = path  # Salva o caminho completo do arquivo
        print(f"Arquivo encontrado: {found_path_DD_categoria}")
        break

if not found_path_DD_categoria:
    print("Nenhum arquivo correspondente foi encontrado.")

print(f"Caminho completo do arquivo encontrado: {found_path_DD_categoria}")

#################
#geral
data_DD_categoria = pd.read_csv(found_path_DD_categoria)

# Adicionar "LL_" às colunas, exceto 'mes_ano'
#data_DD_categoria.columns = ['mes_ano' if col == 'mes_ano' else f'DD_{col}' for col in data_DD_categoria.columns]

####################
# Renomear as colunas
data_DD_categoria = data_DD_categoria.rename(columns={data_DD_categoria.columns[0]: 'mes_ano'})


# Transformar o DataFrame
df_DD_categoria_alfaiataria = data_DD_categoria.melt(
    id_vars=['mes_ano'],        # Coluna que será mantida fixa
    var_name='categoria',     # Nova coluna que conterá os nomes das colunas originais
    value_name='venda'     # Nova coluna que conterá os valores das colunas originais
)

df_DD_categoria_alfaiataria['modelo'] = 'categoria único'
df_DD_categoria_alfaiataria['marca'] = 'DD'

# COMMAND ----------

# MAGIC %md
# MAGIC ### jeans sarja

# COMMAND ----------

# DD

# Lista de caminhos possíveis
paths_DD_categorian1 = [
    'CATEGORIA_N1 - único/DD - Jeans Sarja/outputs/forecast_transposed_GRU_DD_categoria_jeans_sarja_final.csv'#,
    #'Categoria/CATEGORIA_N1/DD/outputs/forecast_transposed_LSTM_DD_alfaiataria_final.csv',
    #'Categoria/CATEGORIA_N1/DD/outputs/forecast_transposed_NHITS_DD_alfaiataria_final.csv',
    #'Categoria/CATEGORIA_N1/DD/outputs/forecast_transposed_NBEATSx_DD_alfaiatariaa_final.csv'
]

# Variável para armazenar o caminho completo do arquivo encontrado
found_path_DD_categoria = None

# Verificar se os arquivos existem
for path in paths_DD_categorian1:
    if os.path.exists(path):
        found_path_DD_categoria = path  # Salva o caminho completo do arquivo
        print(f"Arquivo encontrado: {found_path_DD_categoria}")
        break

if not found_path_DD_categoria:
    print("Nenhum arquivo correspondente foi encontrado.")

print(f"Caminho completo do arquivo encontrado: {found_path_DD_categoria}")

#################
#geral
data_DD_categoria = pd.read_csv(found_path_DD_categoria)

# Adicionar "LL_" às colunas, exceto 'mes_ano'
#data_DD_categoria.columns = ['mes_ano' if col == 'mes_ano' else f'DD_{col}' for col in data_DD_categoria.columns]

####################
# Renomear as colunas
data_DD_categoria = data_DD_categoria.rename(columns={data_DD_categoria.columns[0]: 'mes_ano'})


# Transformar o DataFrame
df_DD_categoria_jeans_sarja = data_DD_categoria.melt(
    id_vars=['mes_ano'],        # Coluna que será mantida fixa
    var_name='categoria',     # Nova coluna que conterá os nomes das colunas originais
    value_name='venda'     # Nova coluna que conterá os valores das colunas originais
)

df_DD_categoria_jeans_sarja['modelo'] = 'categoria único'
df_DD_categoria_jeans_sarja['marca'] = 'DD'

# COMMAND ----------

# MAGIC %md
# MAGIC ### malha

# COMMAND ----------

# DD

# Lista de caminhos possíveis
paths_DD_categorian1 = [
    'CATEGORIA_N1 - único/DD - Malha/outputs/forecast_transposed_GRU_DD_categoria_malha_final.csv'#,
    #'Categoria/CATEGORIA_N1/DD/outputs/forecast_transposed_LSTM_DD_alfaiataria_final.csv',
    #'Categoria/CATEGORIA_N1/DD/outputs/forecast_transposed_NHITS_DD_alfaiataria_final.csv',
    #'Categoria/CATEGORIA_N1/DD/outputs/forecast_transposed_NBEATSx_DD_alfaiatariaa_final.csv'
]

# Variável para armazenar o caminho completo do arquivo encontrado
found_path_DD_categoria = None

# Verificar se os arquivos existem
for path in paths_DD_categorian1:
    if os.path.exists(path):
        found_path_DD_categoria = path  # Salva o caminho completo do arquivo
        print(f"Arquivo encontrado: {found_path_DD_categoria}")
        break

if not found_path_DD_categoria:
    print("Nenhum arquivo correspondente foi encontrado.")

print(f"Caminho completo do arquivo encontrado: {found_path_DD_categoria}")

#################
#geral
data_DD_categoria = pd.read_csv(found_path_DD_categoria)

# Adicionar "LL_" às colunas, exceto 'mes_ano'
#data_DD_categoria.columns = ['mes_ano' if col == 'mes_ano' else f'DD_{col}' for col in data_DD_categoria.columns]

####################
# Renomear as colunas
data_DD_categoria = data_DD_categoria.rename(columns={data_DD_categoria.columns[0]: 'mes_ano'})


# Transformar o DataFrame
df_DD_categoria_malha = data_DD_categoria.melt(
    id_vars=['mes_ano'],        # Coluna que será mantida fixa
    var_name='categoria',     # Nova coluna que conterá os nomes das colunas originais
    value_name='venda'     # Nova coluna que conterá os valores das colunas originais
)

df_DD_categoria_malha['modelo'] = 'categoria único'
df_DD_categoria_malha['marca'] = 'DD'

# COMMAND ----------

# MAGIC %md
# MAGIC ### tecido plano

# COMMAND ----------

# DD

# Lista de caminhos possíveis
paths_DD_categorian1 = [
    'CATEGORIA_N1 - único/DD - Tecido Plano/outputs/forecast_transposed_GRU_DD_categoria_tecido_plano_final.csv'#,
    #'Categoria/CATEGORIA_N1/DD/outputs/forecast_transposed_LSTM_DD_alfaiataria_final.csv',
    #'Categoria/CATEGORIA_N1/DD/outputs/forecast_transposed_NHITS_DD_alfaiataria_final.csv',
    #'Categoria/CATEGORIA_N1/DD/outputs/forecast_transposed_NBEATSx_DD_alfaiatariaa_final.csv'
]

# Variável para armazenar o caminho completo do arquivo encontrado
found_path_DD_categoria = None

# Verificar se os arquivos existem
for path in paths_DD_categorian1:
    if os.path.exists(path):
        found_path_DD_categoria = path  # Salva o caminho completo do arquivo
        print(f"Arquivo encontrado: {found_path_DD_categoria}")
        break

if not found_path_DD_categoria:
    print("Nenhum arquivo correspondente foi encontrado.")

print(f"Caminho completo do arquivo encontrado: {found_path_DD_categoria}")

#################
#geral
data_DD_categoria = pd.read_csv(found_path_DD_categoria)

# Adicionar "LL_" às colunas, exceto 'mes_ano'
#data_DD_categoria.columns = ['mes_ano' if col == 'mes_ano' else f'DD_{col}' for col in data_DD_categoria.columns]

####################
# Renomear as colunas
data_DD_categoria = data_DD_categoria.rename(columns={data_DD_categoria.columns[0]: 'mes_ano'})


# Transformar o DataFrame
df_DD_categoria_tecido_plano = data_DD_categoria.melt(
    id_vars=['mes_ano'],        # Coluna que será mantida fixa
    var_name='categoria',     # Nova coluna que conterá os nomes das colunas originais
    value_name='venda'     # Nova coluna que conterá os valores das colunas originais
)

df_DD_categoria_tecido_plano['modelo'] = 'categoria único'
df_DD_categoria_tecido_plano['marca'] = 'DD'

# COMMAND ----------

# MAGIC %md
# MAGIC ### outros

# COMMAND ----------

# DD

# Lista de caminhos possíveis
paths_DD_categorian1 = [
    'CATEGORIA_N1 - único/DD - Outros/outputs/forecast_transposed_GRU_DD_categoria_outros_final.csv'#,
    #'Categoria/CATEGORIA_N1/DD/outputs/forecast_transposed_LSTM_DD_alfaiataria_final.csv',
    #'Categoria/CATEGORIA_N1/DD/outputs/forecast_transposed_NHITS_DD_alfaiataria_final.csv',
    #'Categoria/CATEGORIA_N1/DD/outputs/forecast_transposed_NBEATSx_DD_alfaiatariaa_final.csv'
]

# Variável para armazenar o caminho completo do arquivo encontrado
found_path_DD_categoria = None

# Verificar se os arquivos existem
for path in paths_DD_categorian1:
    if os.path.exists(path):
        found_path_DD_categoria = path  # Salva o caminho completo do arquivo
        print(f"Arquivo encontrado: {found_path_DD_categoria}")
        break

if not found_path_DD_categoria:
    print("Nenhum arquivo correspondente foi encontrado.")

print(f"Caminho completo do arquivo encontrado: {found_path_DD_categoria}")

#################
#geral
data_DD_categoria = pd.read_csv(found_path_DD_categoria)

# Adicionar "LL_" às colunas, exceto 'mes_ano'
#data_DD_categoria.columns = ['mes_ano' if col == 'mes_ano' else f'DD_{col}' for col in data_DD_categoria.columns]

####################
# Renomear as colunas
data_DD_categoria = data_DD_categoria.rename(columns={data_DD_categoria.columns[0]: 'mes_ano'})


# Transformar o DataFrame
df_DD_categoria_outros = data_DD_categoria.melt(
    id_vars=['mes_ano'],        # Coluna que será mantida fixa
    var_name='categoria',     # Nova coluna que conterá os nomes das colunas originais
    value_name='venda'     # Nova coluna que conterá os valores das colunas originais
)

df_DD_categoria_outros['modelo'] = 'categoria único'
df_DD_categoria_outros['marca'] = 'DD'

# COMMAND ----------

# Concatenar os DataFrames
df_final_categoria_DD_unico = pd.concat([df_DD_categoria_alfaiataria, df_DD_categoria_jeans_sarja, df_DD_categoria_malha, df_DD_categoria_tecido_plano, df_DD_categoria_outros], ignore_index=True)

df_final_categoria_DD_unico

# COMMAND ----------

# MAGIC %md
# MAGIC ## JJ

# COMMAND ----------

# MAGIC %md
# MAGIC ### jeans sarja

# COMMAND ----------

# JJ

# Lista de caminhos possíveis
paths_JJ_categorian1 = [
    'CATEGORIA_N1 - único/JJ - Jeans e Sarja/outputs/forecast_transposed_GRU_JJ_categoria_jeans_sarja_final.csv'#,
    #'Categoria/CATEGORIA_N1/JJ/outputs/forecast_transposed_LSTM_JJ_categoria_final.csv',
    #'Categoria/CATEGORIA_N1/JJ/outputs/forecast_transposed_NHITS_JJ_categoria_final.csv',
    #'Categoria/CATEGORIA_N1/JJ/outputs/forecast_transposed_NBEATSx_JJ_categoria_final.csv'
]

# Variável para armazenar o caminho completo do arquivo encontrado
found_path_JJ_categoria = None

# Verificar se os arquivos existem
for path in paths_JJ_categorian1:
    if os.path.exists(path):
        found_path_JJ_categoria = path  # Salva o caminho completo do arquivo
        print(f"Arquivo encontrado: {found_path_JJ_categoria}")
        break

if not found_path_JJ_categoria:
    print("Nenhum arquivo correspondente foi encontrado.")

print(f"Caminho completo do arquivo encontrado: {found_path_JJ_categoria}")

#################
#geral
data_JJ_categoria = pd.read_csv(found_path_JJ_categoria)

# Adicionar "LL_" às colunas, exceto 'mes_ano'
#data_DD_categoria.columns = ['mes_ano' if col == 'mes_ano' else f'DD_{col}' for col in data_DD_categoria.columns]

####################
# Renomear as colunas
data_JJ_categoria = data_JJ_categoria.rename(columns={data_JJ_categoria.columns[0]: 'mes_ano'})


# Transformar o DataFrame
df_JJ_categoria_jeans_sarja = data_JJ_categoria.melt(
    id_vars=['mes_ano'],        # Coluna que será mantida fixa
    var_name='categoria',     # Nova coluna que conterá os nomes das colunas originais
    value_name='venda'     # Nova coluna que conterá os valores das colunas originais
)

df_JJ_categoria_jeans_sarja['modelo'] = 'categoria único'
df_JJ_categoria_jeans_sarja['marca'] = 'JJ'

# COMMAND ----------

# MAGIC %md
# MAGIC ### malha e moletom

# COMMAND ----------

# JJ

# Lista de caminhos possíveis
paths_JJ_categorian1 = [
    'CATEGORIA_N1 - único/JJ - Malha e Moletom/outputs/forecast_transposed_GRU_JJ_categoria_malha_moletom_final.csv'#,
    #'Categoria/CATEGORIA_N1/JJ/outputs/forecast_transposed_LSTM_JJ_categoria_final.csv',
    #'Categoria/CATEGORIA_N1/JJ/outputs/forecast_transposed_NHITS_JJ_categoria_final.csv',
    #'Categoria/CATEGORIA_N1/JJ/outputs/forecast_transposed_NBEATSx_JJ_categoria_final.csv'
]

# Variável para armazenar o caminho completo do arquivo encontrado
found_path_JJ_categoria = None

# Verificar se os arquivos existem
for path in paths_JJ_categorian1:
    if os.path.exists(path):
        found_path_JJ_categoria = path  # Salva o caminho completo do arquivo
        print(f"Arquivo encontrado: {found_path_JJ_categoria}")
        break

if not found_path_JJ_categoria:
    print("Nenhum arquivo correspondente foi encontrado.")

print(f"Caminho completo do arquivo encontrado: {found_path_JJ_categoria}")

#################
#geral
data_JJ_categoria = pd.read_csv(found_path_JJ_categoria)

# Adicionar "LL_" às colunas, exceto 'mes_ano'
#data_DD_categoria.columns = ['mes_ano' if col == 'mes_ano' else f'DD_{col}' for col in data_DD_categoria.columns]

####################
# Renomear as colunas
data_JJ_categoria = data_JJ_categoria.rename(columns={data_JJ_categoria.columns[0]: 'mes_ano'})


# Transformar o DataFrame
df_JJ_categoria_malha_moletom = data_JJ_categoria.melt(
    id_vars=['mes_ano'],        # Coluna que será mantida fixa
    var_name='categoria',     # Nova coluna que conterá os nomes das colunas originais
    value_name='venda'     # Nova coluna que conterá os valores das colunas originais
)

df_JJ_categoria_malha_moletom['modelo'] = 'categoria único'
df_JJ_categoria_malha_moletom['marca'] = 'JJ'

# COMMAND ----------

# MAGIC %md
# MAGIC ### moda

# COMMAND ----------

# JJ

# Lista de caminhos possíveis
paths_JJ_categorian1 = [
    'CATEGORIA_N1 - único/JJ - Moda/outputs/forecast_transposed_GRU_JJ_categoria_moda_final.csv'#,
    #'Categoria/CATEGORIA_N1/JJ/outputs/forecast_transposed_LSTM_JJ_categoria_final.csv',
    #'Categoria/CATEGORIA_N1/JJ/outputs/forecast_transposed_NHITS_JJ_categoria_final.csv',
    #'Categoria/CATEGORIA_N1/JJ/outputs/forecast_transposed_NBEATSx_JJ_categoria_final.csv'
]

# Variável para armazenar o caminho completo do arquivo encontrado
found_path_JJ_categoria = None

# Verificar se os arquivos existem
for path in paths_JJ_categorian1:
    if os.path.exists(path):
        found_path_JJ_categoria = path  # Salva o caminho completo do arquivo
        print(f"Arquivo encontrado: {found_path_JJ_categoria}")
        break

if not found_path_JJ_categoria:
    print("Nenhum arquivo correspondente foi encontrado.")

print(f"Caminho completo do arquivo encontrado: {found_path_JJ_categoria}")

#################
#geral
data_JJ_categoria = pd.read_csv(found_path_JJ_categoria)

# Adicionar "LL_" às colunas, exceto 'mes_ano'
#data_DD_categoria.columns = ['mes_ano' if col == 'mes_ano' else f'DD_{col}' for col in data_DD_categoria.columns]

####################
# Renomear as colunas
data_JJ_categoria = data_JJ_categoria.rename(columns={data_JJ_categoria.columns[0]: 'mes_ano'})


# Transformar o DataFrame
df_JJ_categoria_moda = data_JJ_categoria.melt(
    id_vars=['mes_ano'],        # Coluna que será mantida fixa
    var_name='categoria',     # Nova coluna que conterá os nomes das colunas originais
    value_name='venda'     # Nova coluna que conterá os valores das colunas originais
)

df_JJ_categoria_moda['modelo'] = 'categoria único'
df_JJ_categoria_moda['marca'] = 'JJ'

# COMMAND ----------

# MAGIC %md
# MAGIC ### outros

# COMMAND ----------

# JJ

# Lista de caminhos possíveis
paths_JJ_categorian1 = [
    'CATEGORIA_N1 - único/JJ - Outros/outputs/forecast_transposed_GRU_JJ_categoria_outros_final.csv'#,
    #'Categoria/CATEGORIA_N1/JJ/outputs/forecast_transposed_LSTM_JJ_categoria_final.csv',
    #'Categoria/CATEGORIA_N1/JJ/outputs/forecast_transposed_NHITS_JJ_categoria_final.csv',
    #'Categoria/CATEGORIA_N1/JJ/outputs/forecast_transposed_NBEATSx_JJ_categoria_final.csv'
]

# Variável para armazenar o caminho completo do arquivo encontrado
found_path_JJ_categoria = None

# Verificar se os arquivos existem
for path in paths_JJ_categorian1:
    if os.path.exists(path):
        found_path_JJ_categoria = path  # Salva o caminho completo do arquivo
        print(f"Arquivo encontrado: {found_path_JJ_categoria}")
        break

if not found_path_JJ_categoria:
    print("Nenhum arquivo correspondente foi encontrado.")

print(f"Caminho completo do arquivo encontrado: {found_path_JJ_categoria}")

#################
#geral
data_JJ_categoria = pd.read_csv(found_path_JJ_categoria)

# Adicionar "LL_" às colunas, exceto 'mes_ano'
#data_DD_categoria.columns = ['mes_ano' if col == 'mes_ano' else f'DD_{col}' for col in data_DD_categoria.columns]

####################
# Renomear as colunas
data_JJ_categoria = data_JJ_categoria.rename(columns={data_JJ_categoria.columns[0]: 'mes_ano'})


# Transformar o DataFrame
df_JJ_categoria_outros = data_JJ_categoria.melt(
    id_vars=['mes_ano'],        # Coluna que será mantida fixa
    var_name='categoria',     # Nova coluna que conterá os nomes das colunas originais
    value_name='venda'     # Nova coluna que conterá os valores das colunas originais
)

df_JJ_categoria_outros['modelo'] = 'categoria único'
df_JJ_categoria_outros['marca'] = 'JJ'

# COMMAND ----------

# Concatenar os DataFrames
df_final_categoria_JJ_unico = pd.concat([df_JJ_categoria_jeans_sarja, df_JJ_categoria_malha_moletom, df_JJ_categoria_moda, df_JJ_categoria_outros], ignore_index=True)

df_final_categoria_JJ_unico

# COMMAND ----------

# MAGIC %md
# MAGIC ## LL

# COMMAND ----------

# MAGIC %md
# MAGIC ### acessorio

# COMMAND ----------

# LL

# Lista de caminhos possíveis
paths_LL_categorian1 = [
    'CATEGORIA_N1 - único/LL - Acessorio/outputs/forecast_transposed_GRU_LL_categoria_final.csv'#,
    #'Categoria/CATEGORIA_N1/LL/outputs/forecast_transposed_LSTM_LL_categoria_final.csv',
    #'Categoria/CATEGORIA_N1/LL/outputs/forecast_transposed_NHITS_LL_categoria_final.csv',
    #'Categoria/CATEGORIA_N1/LL/outputs/forecast_transposed_NBEATSx_LL_categoria_final.csv'
]

# Variável para armazenar o caminho completo do arquivo encontrado
found_path_LL_categoria = None

# Verificar se os arquivos existem
for path in paths_LL_categorian1:
    if os.path.exists(path):
        found_path_LL_categoria = path  # Salva o caminho completo do arquivo
        print(f"Arquivo encontrado: {found_path_LL_categoria}")
        break

if not found_path_LL_categoria:
    print("Nenhum arquivo correspondente foi encontrado.")

print(f"Caminho completo do arquivo encontrado: {found_path_LL_categoria}")

#################
#geral
data_LL_categoria = pd.read_csv(found_path_LL_categoria)

# Adicionar "LL_" às colunas, exceto 'mes_ano'
#data_DD_categoria.columns = ['mes_ano' if col == 'mes_ano' else f'DD_{col}' for col in data_DD_categoria.columns]

####################
# Renomear as colunas
data_LL_categoria = data_LL_categoria.rename(columns={data_LL_categoria.columns[0]: 'mes_ano'})


# Transformar o DataFrame
df_LL_categoria_acessorio = data_LL_categoria.melt(
    id_vars=['mes_ano'],        # Coluna que será mantida fixa
    var_name='categoria',     # Nova coluna que conterá os nomes das colunas originais
    value_name='venda'     # Nova coluna que conterá os valores das colunas originais
)

df_LL_categoria_acessorio['modelo'] = 'categoria único'
df_LL_categoria_acessorio['marca'] = 'LL'

# COMMAND ----------

# MAGIC %md
# MAGIC ### alfaiataria

# COMMAND ----------

# LL

# Lista de caminhos possíveis
paths_LL_categorian1 = [
    'CATEGORIA_N1 - único/LL - Alfaiataria/outputs/forecast_transposed_GRU_LL_categoria_alfaiataria_final.csv'#,
    #'Categoria/CATEGORIA_N1/LL/outputs/forecast_transposed_LSTM_LL_categoria_final.csv',
    #'Categoria/CATEGORIA_N1/LL/outputs/forecast_transposed_NHITS_LL_categoria_final.csv',
    #'Categoria/CATEGORIA_N1/LL/outputs/forecast_transposed_NBEATSx_LL_categoria_final.csv'
]

# Variável para armazenar o caminho completo do arquivo encontrado
found_path_LL_categoria = None

# Verificar se os arquivos existem
for path in paths_LL_categorian1:
    if os.path.exists(path):
        found_path_LL_categoria = path  # Salva o caminho completo do arquivo
        print(f"Arquivo encontrado: {found_path_LL_categoria}")
        break

if not found_path_LL_categoria:
    print("Nenhum arquivo correspondente foi encontrado.")

print(f"Caminho completo do arquivo encontrado: {found_path_LL_categoria}")

#################
#geral
data_LL_categoria = pd.read_csv(found_path_LL_categoria)

# Adicionar "LL_" às colunas, exceto 'mes_ano'
#data_DD_categoria.columns = ['mes_ano' if col == 'mes_ano' else f'DD_{col}' for col in data_DD_categoria.columns]

####################
# Renomear as colunas
data_LL_categoria = data_LL_categoria.rename(columns={data_LL_categoria.columns[0]: 'mes_ano'})


# Transformar o DataFrame
df_LL_categoria_alfaiataria = data_LL_categoria.melt(
    id_vars=['mes_ano'],        # Coluna que será mantida fixa
    var_name='categoria',     # Nova coluna que conterá os nomes das colunas originais
    value_name='venda'     # Nova coluna que conterá os valores das colunas originais
)

df_LL_categoria_alfaiataria['modelo'] = 'categoria único'
df_LL_categoria_alfaiataria['marca'] = 'LL'

# COMMAND ----------

# MAGIC %md
# MAGIC ### casual ville tricot moda

# COMMAND ----------

# LL

# Lista de caminhos possíveis
paths_LL_categorian1 = [
    'CATEGORIA_N1 - único/LL - Casual Ville Tricot Moda/outputs/forecast_transposed_GRU_LL_categoria_casual_ville_tricot_moda_final.csv'#,
    #'Categoria/CATEGORIA_N1/LL/outputs/forecast_transposed_LSTM_LL_categoria_final.csv',
    #'Categoria/CATEGORIA_N1/LL/outputs/forecast_transposed_NHITS_LL_categoria_final.csv',
    #'Categoria/CATEGORIA_N1/LL/outputs/forecast_transposed_NBEATSx_LL_categoria_final.csv'
]

# Variável para armazenar o caminho completo do arquivo encontrado
found_path_LL_categoria = None

# Verificar se os arquivos existem
for path in paths_LL_categorian1:
    if os.path.exists(path):
        found_path_LL_categoria = path  # Salva o caminho completo do arquivo
        print(f"Arquivo encontrado: {found_path_LL_categoria}")
        break

if not found_path_LL_categoria:
    print("Nenhum arquivo correspondente foi encontrado.")

print(f"Caminho completo do arquivo encontrado: {found_path_LL_categoria}")

#################
#geral
data_LL_categoria = pd.read_csv(found_path_LL_categoria)

# Adicionar "LL_" às colunas, exceto 'mes_ano'
#data_DD_categoria.columns = ['mes_ano' if col == 'mes_ano' else f'DD_{col}' for col in data_DD_categoria.columns]

####################
# Renomear as colunas
data_LL_categoria = data_LL_categoria.rename(columns={data_LL_categoria.columns[0]: 'mes_ano'})


# Transformar o DataFrame
df_LL_categoria_casual_ville_tricot_moda = data_LL_categoria.melt(
    id_vars=['mes_ano'],        # Coluna que será mantida fixa
    var_name='categoria',     # Nova coluna que conterá os nomes das colunas originais
    value_name='venda'     # Nova coluna que conterá os valores das colunas originais
)

df_LL_categoria_casual_ville_tricot_moda['modelo'] = 'categoria único'
df_LL_categoria_casual_ville_tricot_moda['marca'] = 'LL'

# COMMAND ----------

# MAGIC %md
# MAGIC ### couro

# COMMAND ----------

# LL

# Lista de caminhos possíveis
paths_LL_categorian1 = [
    'CATEGORIA_N1 - único/LL - Couro/outputs/forecast_transposed_GRU_LL_categoria_couro_final.csv'#,
    #'Categoria/CATEGORIA_N1/LL/outputs/forecast_transposed_LSTM_LL_categoria_final.csv',
    #'Categoria/CATEGORIA_N1/LL/outputs/forecast_transposed_NHITS_LL_categoria_final.csv',
    #'Categoria/CATEGORIA_N1/LL/outputs/forecast_transposed_NBEATSx_LL_categoria_final.csv'
]

# Variável para armazenar o caminho completo do arquivo encontrado
found_path_LL_categoria = None

# Verificar se os arquivos existem
for path in paths_LL_categorian1:
    if os.path.exists(path):
        found_path_LL_categoria = path  # Salva o caminho completo do arquivo
        print(f"Arquivo encontrado: {found_path_LL_categoria}")
        break

if not found_path_LL_categoria:
    print("Nenhum arquivo correspondente foi encontrado.")

print(f"Caminho completo do arquivo encontrado: {found_path_LL_categoria}")

#################
#geral
data_LL_categoria = pd.read_csv(found_path_LL_categoria)

# Adicionar "LL_" às colunas, exceto 'mes_ano'
#data_DD_categoria.columns = ['mes_ano' if col == 'mes_ano' else f'DD_{col}' for col in data_DD_categoria.columns]

####################
# Renomear as colunas
data_LL_categoria = data_LL_categoria.rename(columns={data_LL_categoria.columns[0]: 'mes_ano'})


# Transformar o DataFrame
df_LL_categoria_couro = data_LL_categoria.melt(
    id_vars=['mes_ano'],        # Coluna que será mantida fixa
    var_name='categoria',     # Nova coluna que conterá os nomes das colunas originais
    value_name='venda'     # Nova coluna que conterá os valores das colunas originais
)

df_LL_categoria_couro['modelo'] = 'categoria único'
df_LL_categoria_couro['marca'] = 'LL'

# COMMAND ----------

# MAGIC %md
# MAGIC ### fluidos plano

# COMMAND ----------

# nao rodou

# COMMAND ----------

# MAGIC %md
# MAGIC ### jeans sarja

# COMMAND ----------

# LL

# Lista de caminhos possíveis
paths_LL_categorian1 = [
    'CATEGORIA_N1 - único/LL - Jeans Sarja/outputs/forecast_transposed_GRU_LL_categoria_jeans_sarja_final.csv'#,
    #'Categoria/CATEGORIA_N1/LL/outputs/forecast_transposed_LSTM_LL_categoria_final.csv',
    #'Categoria/CATEGORIA_N1/LL/outputs/forecast_transposed_NHITS_LL_categoria_final.csv',
    #'Categoria/CATEGORIA_N1/LL/outputs/forecast_transposed_NBEATSx_LL_categoria_final.csv'
]

# Variável para armazenar o caminho completo do arquivo encontrado
found_path_LL_categoria = None

# Verificar se os arquivos existem
for path in paths_LL_categorian1:
    if os.path.exists(path):
        found_path_LL_categoria = path  # Salva o caminho completo do arquivo
        print(f"Arquivo encontrado: {found_path_LL_categoria}")
        break

if not found_path_LL_categoria:
    print("Nenhum arquivo correspondente foi encontrado.")

print(f"Caminho completo do arquivo encontrado: {found_path_LL_categoria}")

#################
#geral
data_LL_categoria = pd.read_csv(found_path_LL_categoria)

# Adicionar "LL_" às colunas, exceto 'mes_ano'
#data_DD_categoria.columns = ['mes_ano' if col == 'mes_ano' else f'DD_{col}' for col in data_DD_categoria.columns]

####################
# Renomear as colunas
data_LL_categoria = data_LL_categoria.rename(columns={data_LL_categoria.columns[0]: 'mes_ano'})


# Transformar o DataFrame
df_LL_categoria_jeans_sarja = data_LL_categoria.melt(
    id_vars=['mes_ano'],        # Coluna que será mantida fixa
    var_name='categoria',     # Nova coluna que conterá os nomes das colunas originais
    value_name='venda'     # Nova coluna que conterá os valores das colunas originais
)

df_LL_categoria_jeans_sarja['modelo'] = 'categoria único'
df_LL_categoria_jeans_sarja['marca'] = 'LL'

# COMMAND ----------

# MAGIC %md
# MAGIC ### outros

# COMMAND ----------

# LL

# Lista de caminhos possíveis
paths_LL_categorian1 = [
    'CATEGORIA_N1 - único/LL - Outros/outputs/forecast_transposed_GRU_LL_categoria_outros_final.csv'#,
    #'Categoria/CATEGORIA_N1/LL/outputs/forecast_transposed_LSTM_LL_categoria_final.csv',
    #'Categoria/CATEGORIA_N1/LL/outputs/forecast_transposed_NHITS_LL_categoria_final.csv',
    #'Categoria/CATEGORIA_N1/LL/outputs/forecast_transposed_NBEATSx_LL_categoria_final.csv'
]

# Variável para armazenar o caminho completo do arquivo encontrado
found_path_LL_categoria = None

# Verificar se os arquivos existem
for path in paths_LL_categorian1:
    if os.path.exists(path):
        found_path_LL_categoria = path  # Salva o caminho completo do arquivo
        print(f"Arquivo encontrado: {found_path_LL_categoria}")
        break

if not found_path_LL_categoria:
    print("Nenhum arquivo correspondente foi encontrado.")

print(f"Caminho completo do arquivo encontrado: {found_path_LL_categoria}")

#################
#geral
data_LL_categoria = pd.read_csv(found_path_LL_categoria)

# Adicionar "LL_" às colunas, exceto 'mes_ano'
#data_DD_categoria.columns = ['mes_ano' if col == 'mes_ano' else f'DD_{col}' for col in data_DD_categoria.columns]

####################
# Renomear as colunas
data_LL_categoria = data_LL_categoria.rename(columns={data_LL_categoria.columns[0]: 'mes_ano'})


# Transformar o DataFrame
df_LL_categoria_outros = data_LL_categoria.melt(
    id_vars=['mes_ano'],        # Coluna que será mantida fixa
    var_name='categoria',     # Nova coluna que conterá os nomes das colunas originais
    value_name='venda'     # Nova coluna que conterá os valores das colunas originais
)

df_LL_categoria_outros['modelo'] = 'categoria único'
df_LL_categoria_outros['marca'] = 'LL'

# COMMAND ----------

# MAGIC %md
# MAGIC ### seda

# COMMAND ----------

# LL

# Lista de caminhos possíveis
paths_LL_categorian1 = [
    'CATEGORIA_N1 - único/LL - Seda/outputs/forecast_transposed_GRU_LL_categoria_seda_final.csv'#,
    #'Categoria/CATEGORIA_N1/LL/outputs/forecast_transposed_LSTM_LL_categoria_final.csv',
    #'Categoria/CATEGORIA_N1/LL/outputs/forecast_transposed_NHITS_LL_categoria_final.csv',
    #'Categoria/CATEGORIA_N1/LL/outputs/forecast_transposed_NBEATSx_LL_categoria_final.csv'
]

# Variável para armazenar o caminho completo do arquivo encontrado
found_path_LL_categoria = None

# Verificar se os arquivos existem
for path in paths_LL_categorian1:
    if os.path.exists(path):
        found_path_LL_categoria = path  # Salva o caminho completo do arquivo
        print(f"Arquivo encontrado: {found_path_LL_categoria}")
        break

if not found_path_LL_categoria:
    print("Nenhum arquivo correspondente foi encontrado.")

print(f"Caminho completo do arquivo encontrado: {found_path_LL_categoria}")

#################
#geral
data_LL_categoria = pd.read_csv(found_path_LL_categoria)

# Adicionar "LL_" às colunas, exceto 'mes_ano'
#data_DD_categoria.columns = ['mes_ano' if col == 'mes_ano' else f'DD_{col}' for col in data_DD_categoria.columns]

####################
# Renomear as colunas
data_LL_categoria = data_LL_categoria.rename(columns={data_LL_categoria.columns[0]: 'mes_ano'})


# Transformar o DataFrame
df_LL_categoria_seda = data_LL_categoria.melt(
    id_vars=['mes_ano'],        # Coluna que será mantida fixa
    var_name='categoria',     # Nova coluna que conterá os nomes das colunas originais
    value_name='venda'     # Nova coluna que conterá os valores das colunas originais
)

df_LL_categoria_seda['modelo'] = 'categoria único'
df_LL_categoria_seda['marca'] = 'LL'

# COMMAND ----------

# Concatenar os DataFrames
df_final_categoria_LL_unico = pd.concat([df_LL_categoria_acessorio, df_LL_categoria_alfaiataria, df_LL_categoria_casual_ville_tricot_moda, df_LL_categoria_couro, df_LL_categoria_jeans_sarja, df_LL_categoria_outros, df_LL_categoria_seda], ignore_index=True)

df_final_categoria_LL_unico

# COMMAND ----------

# MAGIC %md
# MAGIC # GRIFFE

# COMMAND ----------

# MAGIC %md
# MAGIC ## DD

# COMMAND ----------

# DD

# Lista de caminhos possíveis
paths_DD_griffe = [
    'Categoria/Griffe/DD/outputs/forecast_transposed_GRU_DD_griffe_final.csv',
    'Categoria/Griffe/DD/outputs/forecast_transposed_LSTM_DD_categoria_final.csv',
    'Categoria/Griffe/DD/outputs/forecast_transposed_NHITS_DD_categoria_final.csv',
    'Categoria/Griffe/DD/outputs/forecast_transposed_NBEATSx_DD_categoria_final.csv'
]

# Variável para armazenar o caminho completo do arquivo encontrado
found_path_DD_griffe = None

# Verificar se os arquivos existem
for path in paths_DD_griffe:
    if os.path.exists(path):
        found_path_DD_griffe = path  # Salva o caminho completo do arquivo
        print(f"Arquivo encontrado: {found_path_DD_griffe}")
        break

if not found_path_DD_griffe:
    print("Nenhum arquivo correspondente foi encontrado.")

print(f"Caminho completo do arquivo encontrado: {found_path_DD_griffe}")

#################
#geral
data_DD_griffe = pd.read_csv(found_path_DD_griffe)

# Adicionar "LL_" às colunas, exceto 'mes_ano'
#data_DD_categoria.columns = ['mes_ano' if col == 'mes_ano' else f'DD_{col}' for col in data_DD_categoria.columns]

####################
# Renomear as colunas
data_DD_griffe = data_DD_griffe.rename(columns={data_DD_griffe.columns[0]: 'mes_ano'})


# Transformar o DataFrame
df_DD_griffe = data_DD_griffe.melt(
    id_vars=['mes_ano'],   # Coluna que será mantida fixa
    var_name='categoria',  # Nova coluna que conterá os nomes das colunas originais
    value_name='venda'     # Nova coluna que conterá os valores das colunas originais
)

df_DD_griffe['modelo'] = 'griffe geral'
df_DD_griffe['marca'] = 'DD'

# COMMAND ----------

# MAGIC %md
# MAGIC ## JJ

# COMMAND ----------

# JJ

# Lista de caminhos possíveis
paths_JJ_griffe = [
    'Categoria/Griffe/JJ/outputs/forecast_transposed_GRU_JJ_griffe_final.csv',
    'Categoria/Griffe/JJ/outputs/forecast_transposed_LSTM_JJ_categoria_final.csv',
    'Categoria/Griffe/JJ/outputs/forecast_transposed_NHITS_JJ_categoria_final.csv',
    'Categoria/Griffe/JJ/outputs/forecast_transposed_NBEATSx_JJ_categoria_final.csv'
]

# Variável para armazenar o caminho completo do arquivo encontrado
found_path_JJ_griffe = None

# Verificar se os arquivos existem
for path in paths_JJ_griffe:
    if os.path.exists(path):
        found_path_JJ_griffe = path  # Salva o caminho completo do arquivo
        print(f"Arquivo encontrado: {found_path_JJ_griffe}")
        break

if not found_path_JJ_griffe:
    print("Nenhum arquivo correspondente foi encontrado.")

print(f"Caminho completo do arquivo encontrado: {found_path_JJ_griffe}")

#################
#geral
data_JJ_griffe = pd.read_csv(found_path_JJ_griffe)

# Adicionar "LL_" às colunas, exceto 'mes_ano'
#data_DD_categoria.columns = ['mes_ano' if col == 'mes_ano' else f'DD_{col}' for col in data_DD_categoria.columns]

####################
# Renomear as colunas
data_JJ_griffe = data_JJ_griffe.rename(columns={data_JJ_griffe.columns[0]: 'mes_ano'})


# Transformar o DataFrame
df_JJ_griffe = data_JJ_griffe.melt(
    id_vars=['mes_ano'],   # Coluna que será mantida fixa
    var_name='categoria',  # Nova coluna que conterá os nomes das colunas originais
    value_name='venda'     # Nova coluna que conterá os valores das colunas originais
)

df_JJ_griffe['modelo'] = 'griffe geral'
df_JJ_griffe['marca'] = 'JJ'

# COMMAND ----------

# MAGIC %md
# MAGIC ## LL

# COMMAND ----------

# LL

# Lista de caminhos possíveis
paths_LL_griffe = [
    'Categoria/Griffe/LL/outputs/forecast_transposed_GRU_LL_griffe_final.csv',
    'Categoria/Griffe/LL/outputs/forecast_transposed_LSTM_LL_categoria_final.csv',
    'Categoria/Griffe/LL/outputs/forecast_transposed_NHITS_LL_categoria_final.csv',
    'Categoria/Griffe/LL/outputs/forecast_transposed_NBEATSx_LL_categoria_final.csv'
]

# Variável para armazenar o caminho completo do arquivo encontrado
found_path_LL_griffe = None

# Verificar se os arquivos existem
for path in paths_LL_griffe:
    if os.path.exists(path):
        found_path_LL_griffe = path  # Salva o caminho completo do arquivo
        print(f"Arquivo encontrado: {found_path_LL_griffe}")
        break

if not found_path_LL_griffe:
    print("Nenhum arquivo correspondente foi encontrado.")

print(f"Caminho completo do arquivo encontrado: {found_path_LL_griffe}")

#################
#geral
data_LL_griffe = pd.read_csv(found_path_LL_griffe)

# Adicionar "LL_" às colunas, exceto 'mes_ano'
#data_DD_categoria.columns = ['mes_ano' if col == 'mes_ano' else f'DD_{col}' for col in data_DD_categoria.columns]

####################
# Renomear as colunas
data_LL_griffe = data_LL_griffe.rename(columns={data_LL_griffe.columns[0]: 'mes_ano'})


# Transformar o DataFrame
df_LL_griffe = data_LL_griffe.melt(
    id_vars=['mes_ano'],   # Coluna que será mantida fixa
    var_name='categoria',  # Nova coluna que conterá os nomes das colunas originais
    value_name='venda'     # Nova coluna que conterá os valores das colunas originais
)

df_LL_griffe['modelo'] = 'griffe geral'
df_LL_griffe['marca'] = 'LL'

# COMMAND ----------

# Concatenar os DataFrames
df_final_griffe = pd.concat([df_DD_griffe, df_LL_griffe, df_JJ_griffe], ignore_index=True)

df_final_griffe

# COMMAND ----------

# MAGIC %md
# MAGIC # GRIFFE ÚNICOS

# COMMAND ----------

# MAGIC %md
# MAGIC ## DD

# COMMAND ----------

# MAGIC %md
# MAGIC ### fem

# COMMAND ----------

# DD

# Lista de caminhos possíveis
paths_DD_griffe = [
    'Griffe - único/DD - Fem/outputs/forecast_transposed_GRU_DD_fem_final.csv'#,
    #'Categoria/Griffe/DD/outputs/forecast_transposed_LSTM_DD_categoria_final.csv',
    #'Categoria/Griffe/DD/outputs/forecast_transposed_NHITS_DD_categoria_final.csv',
    #'Categoria/Griffe/DD/outputs/forecast_transposed_NBEATSx_DD_categoria_final.csv'
]

# Variável para armazenar o caminho completo do arquivo encontrado
found_path_DD_griffe = None

# Verificar se os arquivos existem
for path in paths_DD_griffe:
    if os.path.exists(path):
        found_path_DD_griffe = path  # Salva o caminho completo do arquivo
        print(f"Arquivo encontrado: {found_path_DD_griffe}")
        break

if not found_path_DD_griffe:
    print("Nenhum arquivo correspondente foi encontrado.")

print(f"Caminho completo do arquivo encontrado: {found_path_DD_griffe}")

#################
#geral
data_DD_griffe = pd.read_csv(found_path_DD_griffe)

# Adicionar "LL_" às colunas, exceto 'mes_ano'
#data_DD_categoria.columns = ['mes_ano' if col == 'mes_ano' else f'DD_{col}' for col in data_DD_categoria.columns]

####################
# Renomear as colunas
data_DD_griffe = data_DD_griffe.rename(columns={data_DD_griffe.columns[0]: 'mes_ano'})


# Transformar o DataFrame
df_DD_griffe_fem = data_DD_griffe.melt(
    id_vars=['mes_ano'],   # Coluna que será mantida fixa
    var_name='categoria',  # Nova coluna que conterá os nomes das colunas originais
    value_name='venda'     # Nova coluna que conterá os valores das colunas originais
)

df_DD_griffe_fem['modelo'] = 'griffe único'
df_DD_griffe_fem['marca'] = 'DD'

# COMMAND ----------

# MAGIC %md
# MAGIC ### masc

# COMMAND ----------

# DD

# Lista de caminhos possíveis
paths_DD_griffe = [
    'Griffe - único/DD - Masc/outputs/forecast_transposed_GRU_DD_masc_final.csv'#,
    #'Categoria/Griffe/DD/outputs/forecast_transposed_LSTM_DD_categoria_final.csv',
    #'Categoria/Griffe/DD/outputs/forecast_transposed_NHITS_DD_categoria_final.csv',
    #'Categoria/Griffe/DD/outputs/forecast_transposed_NBEATSx_DD_categoria_final.csv'
]

# Variável para armazenar o caminho completo do arquivo encontrado
found_path_DD_griffe = None

# Verificar se os arquivos existem
for path in paths_DD_griffe:
    if os.path.exists(path):
        found_path_DD_griffe = path  # Salva o caminho completo do arquivo
        print(f"Arquivo encontrado: {found_path_DD_griffe}")
        break

if not found_path_DD_griffe:
    print("Nenhum arquivo correspondente foi encontrado.")

print(f"Caminho completo do arquivo encontrado: {found_path_DD_griffe}")

#################
#geral
data_DD_griffe = pd.read_csv(found_path_DD_griffe)

# Adicionar "LL_" às colunas, exceto 'mes_ano'
#data_DD_categoria.columns = ['mes_ano' if col == 'mes_ano' else f'DD_{col}' for col in data_DD_categoria.columns]

####################
# Renomear as colunas
data_DD_griffe = data_DD_griffe.rename(columns={data_DD_griffe.columns[0]: 'mes_ano'})


# Transformar o DataFrame
df_DD_griffe_masc = data_DD_griffe.melt(
    id_vars=['mes_ano'],   # Coluna que será mantida fixa
    var_name='categoria',  # Nova coluna que conterá os nomes das colunas originais
    value_name='venda'     # Nova coluna que conterá os valores das colunas originais
)

df_DD_griffe_masc['modelo'] = 'griffe único'
df_DD_griffe_masc['marca'] = 'DD'

# COMMAND ----------

# Concatenar os DataFrames
df_final_griffe_DD_unico = pd.concat([df_DD_griffe_masc, df_DD_griffe_fem], ignore_index=True)

df_final_griffe_DD_unico

# COMMAND ----------

# MAGIC %md
# MAGIC ## JJ

# COMMAND ----------

# MAGIC %md
# MAGIC ### fem

# COMMAND ----------

# JJ

# Lista de caminhos possíveis
paths_JJ_griffe = [
    'Griffe - único/JJ - Fem/outputs/forecast_transposed_GRU_JJ_fem_final.csv'#,
    #'Categoria/Griffe/JJ/outputs/forecast_transposed_LSTM_JJ_categoria_final.csv',
    #'Categoria/Griffe/JJ/outputs/forecast_transposed_NHITS_JJ_categoria_final.csv',
    #'Categoria/Griffe/JJ/outputs/forecast_transposed_NBEATSx_JJ_categoria_final.csv'
]

# Variável para armazenar o caminho completo do arquivo encontrado
found_path_JJ_griffe = None

# Verificar se os arquivos existem
for path in paths_JJ_griffe:
    if os.path.exists(path):
        found_path_JJ_griffe = path  # Salva o caminho completo do arquivo
        print(f"Arquivo encontrado: {found_path_JJ_griffe}")
        break

if not found_path_JJ_griffe:
    print("Nenhum arquivo correspondente foi encontrado.")

print(f"Caminho completo do arquivo encontrado: {found_path_JJ_griffe}")

#################
#geral
data_JJ_griffe = pd.read_csv(found_path_JJ_griffe)

# Adicionar "LL_" às colunas, exceto 'mes_ano'
#data_DD_categoria.columns = ['mes_ano' if col == 'mes_ano' else f'DD_{col}' for col in data_DD_categoria.columns]

####################
# Renomear as colunas
data_JJ_griffe = data_JJ_griffe.rename(columns={data_JJ_griffe.columns[0]: 'mes_ano'})


# Transformar o DataFrame
df_JJ_griffe_fem = data_JJ_griffe.melt(
    id_vars=['mes_ano'],   # Coluna que será mantida fixa
    var_name='categoria',  # Nova coluna que conterá os nomes das colunas originais
    value_name='venda'     # Nova coluna que conterá os valores das colunas originais
)

df_JJ_griffe_fem['modelo'] = 'griffe único'
df_JJ_griffe_fem['marca'] = 'JJ'

# COMMAND ----------

# MAGIC %md
# MAGIC ### masc

# COMMAND ----------

# JJ

# Lista de caminhos possíveis
paths_JJ_griffe = [
    'Griffe - único/JJ - Masc/outputs/forecast_transposed_GRU_JJ_masc_final.csv'#,
    #'Categoria/Griffe/JJ/outputs/forecast_transposed_LSTM_JJ_categoria_final.csv',
    #'Categoria/Griffe/JJ/outputs/forecast_transposed_NHITS_JJ_categoria_final.csv',
    #'Categoria/Griffe/JJ/outputs/forecast_transposed_NBEATSx_JJ_categoria_final.csv'
]

# Variável para armazenar o caminho completo do arquivo encontrado
found_path_JJ_griffe = None

# Verificar se os arquivos existem
for path in paths_JJ_griffe:
    if os.path.exists(path):
        found_path_JJ_griffe = path  # Salva o caminho completo do arquivo
        print(f"Arquivo encontrado: {found_path_JJ_griffe}")
        break

if not found_path_JJ_griffe:
    print("Nenhum arquivo correspondente foi encontrado.")

print(f"Caminho completo do arquivo encontrado: {found_path_JJ_griffe}")

#################
#geral
data_JJ_griffe = pd.read_csv(found_path_JJ_griffe)

# Adicionar "LL_" às colunas, exceto 'mes_ano'
#data_DD_categoria.columns = ['mes_ano' if col == 'mes_ano' else f'DD_{col}' for col in data_DD_categoria.columns]

####################
# Renomear as colunas
data_JJ_griffe = data_JJ_griffe.rename(columns={data_JJ_griffe.columns[0]: 'mes_ano'})


# Transformar o DataFrame
df_JJ_griffe_masc = data_JJ_griffe.melt(
    id_vars=['mes_ano'],   # Coluna que será mantida fixa
    var_name='categoria',  # Nova coluna que conterá os nomes das colunas originais
    value_name='venda'     # Nova coluna que conterá os valores das colunas originais
)

df_JJ_griffe_masc['modelo'] = 'griffe único'
df_JJ_griffe_masc['marca'] = 'JJ'

# COMMAND ----------

# Concatenar os DataFrames
df_final_griffe_JJ_unico = pd.concat([df_JJ_griffe_masc, df_JJ_griffe_fem], ignore_index=True)

df_final_griffe_JJ_unico

# COMMAND ----------

# MAGIC %md
# MAGIC ## LL

# COMMAND ----------

# MAGIC %md
# MAGIC ### beaute

# COMMAND ----------

# LL

# Lista de caminhos possíveis
paths_LL_griffe = [
    'Griffe - único/LL - Beaute/outputs/forecast_transposed_GRU_LL_beaute_final.csv',
    #'Categoria/Griffe/LL/outputs/forecast_transposed_LSTM_LL_categoria_final.csv',
    #'Categoria/Griffe/LL/outputs/forecast_transposed_NHITS_LL_categoria_final.csv',
    #'Categoria/Griffe/LL/outputs/forecast_transposed_NBEATSx_LL_categoria_final.csv'
]

# Variável para armazenar o caminho completo do arquivo encontrado
found_path_LL_griffe = None

# Verificar se os arquivos existem
for path in paths_LL_griffe:
    if os.path.exists(path):
        found_path_LL_griffe = path  # Salva o caminho completo do arquivo
        print(f"Arquivo encontrado: {found_path_LL_griffe}")
        break

if not found_path_LL_griffe:
    print("Nenhum arquivo correspondente foi encontrado.")

print(f"Caminho completo do arquivo encontrado: {found_path_LL_griffe}")

#################
#geral
data_LL_griffe = pd.read_csv(found_path_LL_griffe)

# Adicionar "LL_" às colunas, exceto 'mes_ano'
#data_DD_categoria.columns = ['mes_ano' if col == 'mes_ano' else f'DD_{col}' for col in data_DD_categoria.columns]

####################
# Renomear as colunas
data_LL_griffe = data_LL_griffe.rename(columns={data_LL_griffe.columns[0]: 'mes_ano'})


# Transformar o DataFrame
df_LL_griffe_beaute = data_LL_griffe.melt(
    id_vars=['mes_ano'],   # Coluna que será mantida fixa
    var_name='categoria',  # Nova coluna que conterá os nomes das colunas originais
    value_name='venda'     # Nova coluna que conterá os valores das colunas originais
)

df_LL_griffe_beaute['modelo'] = 'griffe geral'
df_LL_griffe_beaute['marca'] = 'LL'

# COMMAND ----------

# MAGIC %md
# MAGIC ### casa

# COMMAND ----------

# LL

# Lista de caminhos possíveis
paths_LL_griffe = [
    'Griffe - único/LL - Casa/outputs/forecast_transposed_GRU_LL_casa_final.csv',
    #'Categoria/Griffe/LL/outputs/forecast_transposed_LSTM_LL_categoria_final.csv',
    #'Categoria/Griffe/LL/outputs/forecast_transposed_NHITS_LL_categoria_final.csv',
    #'Categoria/Griffe/LL/outputs/forecast_transposed_NBEATSx_LL_categoria_final.csv'
]

# Variável para armazenar o caminho completo do arquivo encontrado
found_path_LL_griffe = None

# Verificar se os arquivos existem
for path in paths_LL_griffe:
    if os.path.exists(path):
        found_path_LL_griffe = path  # Salva o caminho completo do arquivo
        print(f"Arquivo encontrado: {found_path_LL_griffe}")
        break

if not found_path_LL_griffe:
    print("Nenhum arquivo correspondente foi encontrado.")

print(f"Caminho completo do arquivo encontrado: {found_path_LL_griffe}")

#################
#geral
data_LL_griffe = pd.read_csv(found_path_LL_griffe)

# Adicionar "LL_" às colunas, exceto 'mes_ano'
#data_DD_categoria.columns = ['mes_ano' if col == 'mes_ano' else f'DD_{col}' for col in data_DD_categoria.columns]

####################
# Renomear as colunas
data_LL_griffe = data_LL_griffe.rename(columns={data_LL_griffe.columns[0]: 'mes_ano'})


# Transformar o DataFrame
df_LL_griffe_casa = data_LL_griffe.melt(
    id_vars=['mes_ano'],   # Coluna que será mantida fixa
    var_name='categoria',  # Nova coluna que conterá os nomes das colunas originais
    value_name='venda'     # Nova coluna que conterá os valores das colunas originais
)

df_LL_griffe_casa['modelo'] = 'griffe geral'
df_LL_griffe_casa['marca'] = 'LL'

# COMMAND ----------

# MAGIC %md
# MAGIC ### deux

# COMMAND ----------

# LL

# Lista de caminhos possíveis
paths_LL_griffe = [
    'Griffe - único/LL - Deux/outputs/forecast_transposed_GRU_LL_deux_final.csv',
    #'Categoria/Griffe/LL/outputs/forecast_transposed_LSTM_LL_categoria_final.csv',
    #'Categoria/Griffe/LL/outputs/forecast_transposed_NHITS_LL_categoria_final.csv',
    #'Categoria/Griffe/LL/outputs/forecast_transposed_NBEATSx_LL_categoria_final.csv'
]

# Variável para armazenar o caminho completo do arquivo encontrado
found_path_LL_griffe = None

# Verificar se os arquivos existem
for path in paths_LL_griffe:
    if os.path.exists(path):
        found_path_LL_griffe = path  # Salva o caminho completo do arquivo
        print(f"Arquivo encontrado: {found_path_LL_griffe}")
        break

if not found_path_LL_griffe:
    print("Nenhum arquivo correspondente foi encontrado.")

print(f"Caminho completo do arquivo encontrado: {found_path_LL_griffe}")

#################
#geral
data_LL_griffe = pd.read_csv(found_path_LL_griffe)

# Adicionar "LL_" às colunas, exceto 'mes_ano'
#data_DD_categoria.columns = ['mes_ano' if col == 'mes_ano' else f'DD_{col}' for col in data_DD_categoria.columns]

####################
# Renomear as colunas
data_LL_griffe = data_LL_griffe.rename(columns={data_LL_griffe.columns[0]: 'mes_ano'})


# Transformar o DataFrame
df_LL_griffe_deux = data_LL_griffe.melt(
    id_vars=['mes_ano'],   # Coluna que será mantida fixa
    var_name='categoria',  # Nova coluna que conterá os nomes das colunas originais
    value_name='venda'     # Nova coluna que conterá os valores das colunas originais
)

df_LL_griffe_deux['modelo'] = 'griffe geral'
df_LL_griffe_deux['marca'] = 'LL'

# COMMAND ----------

# MAGIC %md
# MAGIC ### noir

# COMMAND ----------

# nao rodou

# COMMAND ----------

# Concatenar os DataFrames
df_final_griffe_LL_unico = pd.concat([df_LL_griffe_beaute, df_LL_griffe_casa, df_LL_griffe_deux], ignore_index=True)

df_final_griffe_LL_unico

# COMMAND ----------

# MAGIC %md
# MAGIC # agrupando dataframes

# COMMAND ----------

# Concatenar os DataFrames
final_data = pd.concat([df_final, df_final_categoria, df_final_categoria_DD_unico, df_final_categoria_JJ_unico, df_final_griffe, df_final_griffe_DD_unico, df_final_griffe_JJ_unico, df_final_categoria_LL_unico, df_final_griffe_LL_unico], ignore_index=True)

final_data

# COMMAND ----------

# MAGIC %md
# MAGIC # CONVERTENDO SPARK E SALVANDO NA TABELA

# COMMAND ----------

# Criar a SparkSession
spark = SparkSession.builder.appName("pandas to spark").getOrCreate()

# COMMAND ----------

# Converter o DataFrame pandas para Spark
sparkdf = spark.createDataFrame(final_data)
sparkdf.display()

# COMMAND ----------

BLOB_PATH = "/mnt/powerbi/Projecao/"

# Salva o DataFrame `sparkdf` como um único arquivo Parquet no Blob Storage
(sparkdf
 .coalesce(1)  # Combina todas as partições em uma única
 .write
 .mode('overwrite')  # Substitui o arquivo existente
 .format('parquet')
 .save(BLOB_PATH)
)

# Obtém o nome do único arquivo Parquet gerado (deve ser "part-00000")
parquet_name = [x.name for x in dbutils.fs.ls(BLOB_PATH) if "part" in x.name][0]

# Renomeia o arquivo Parquet gerado para `data.parquet`
dbutils.fs.mv(f"{BLOB_PATH}/{parquet_name}", f"{BLOB_PATH}/data.parquet")

# Opcional: Remove outros arquivos/partes que não são necessários
for file in dbutils.fs.ls(BLOB_PATH):
    if "part" not in file.name and file.name != "data.parquet":
        dbutils.fs.rm(f"{BLOB_PATH}/{file.name}")

# COMMAND ----------

# Caminho do arquivo Parquet
BLOB_PATH = "/mnt/powerbi/Projecao/"
PARQUET_FILE = f"{BLOB_PATH}/data.parquet"

# Lê o arquivo Parquet e cria um DataFrame Spark
sparkdf_read = spark.read.format("parquet").load(PARQUET_FILE)

# Mostra as primeiras linhas do DataFrame para verificar o conteúdo
sparkdf_read.display()

# COMMAND ----------

#sql(f"DROP TABLE SANDBOX.FACT_PROJECOES")
#dbutils.fs.rm('/SANDBOX/FACT/FACT_PROJECOES', True)

# COMMAND ----------

#dbutils.fs.rm('/SANDBOX/FACT/FACT_PROJECOES', True)

# COMMAND ----------

# ARRUMAR os nomes das colunas

sql("""
    CREATE TABLE IF NOT EXISTS GOLD_PLANEJAMENTO.FACT_PROJECAO (
      MES_ANO varchar(10) COMMENT 'Ano e mês da previsão',
      MARCA varchar(10) COMMENT 'Marca',
      MODELO varchar(10) COMMENT 'Modelo',
      CATEGORIA varchar(10) COMMENT 'Categoria',
      VENDA decimal(14,2) COMMENT 'VLF VALOR DA PREVISÃO'
    )
    USING DELTA LOCATION '/GOLD_PLANEJAMENTO/FACT/FACT_PROJECAO' --'dbfs:/SANDBOX/FACT/PROJECAO'
    """)

# COMMAND ----------

sparkdf.write \
  .format("delta") \
  .mode("overwrite") \
  .option("overwriteSchema", "true") \
  .save('/GOLD_PLANEJAMENTO/FACT/FACT_PROJECAO') #('SANDBOX/FACT/PROJECAO') #('dbfs:/SANDBOX/FACT/PROJECAO')

# COMMAND ----------

# MAGIC %sql
# MAGIC
# MAGIC select * from gold_planejamento.fact_projecao where mes_ano = '2025-10' and marca = 'DD' and categoria = 'Alfaiataria'

# COMMAND ----------


