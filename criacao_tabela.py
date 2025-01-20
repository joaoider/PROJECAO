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
    'período': data_DD['mes_ano'],
    'marca': 'DD',
    'modelo': 'geral',
    'categoria': 'total',
    'venda': data_DD['DD']
})

df_DD

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
    'período': data_LL['mes_ano'],
    'marca': 'LL',
    'modelo': 'geral',
    'categoria': 'total',
    'venda': data_LL['LL']
})

df_LL

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
    'período': data_JJ['mes_ano'],
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

# Combinar os DataFrames
#merged_data = data_LL.merge(data_DD, on='mes_ano').merge(data_JJ, on='mes_ano').merge(data_LL, on='mes_ano')
#merged_data

# COMMAND ----------

# MAGIC %md
# MAGIC # CATEGORIA_N1

# COMMAND ----------

# DD

# Lista de caminhos possíveis
paths_DD_categorian1 = [
    'Categoria/CATEGORIA_N1/DD/outputs/forecast_transposed_GRU_DD_categoria_final.csv.csv',
    'Categoria/CATEGORIA_N1/DD/outputs/forecast_transposed_LSTM_DD_categoria_final.csv.csv',
    'Categoria/CATEGORIA_N1/DD/outputs/forecast_transposed_NHITS_DD_categoria_final.csv.csv',
    'Categoria/CATEGORIA_N1/DD/outputs/forecast_transposed_NBEATSx_DD_categoria_final.csv.csv'
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

# COMMAND ----------

# JJ

# Lista de caminhos possíveis
paths_JJ_categorian1 = [
    'Categoria/CATEGORIA_N1/JJ/outputs/forecast_transposed_GRU_JJ_categoria_final.csv.csv',
    'Categoria/CATEGORIA_N1/JJ/outputs/forecast_transposed_LSTM_JJ_categoria_final.csv.csv',
    'Categoria/CATEGORIA_N1/JJ/outputs/forecast_transposed_NHITS_JJ_categoria_final.csv.csv',
    'Categoria/CATEGORIA_N1/JJ/outputs/forecast_transposed_NBEATSx_JJ_categoria_final.csv.csv'
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

# COMMAND ----------

# LL

# Lista de caminhos possíveis
paths_LL_categorian1 = [
    'Categoria/CATEGORIA_N1/LL/outputs/forecast_transposed_GRU_LL_categoria_final.csv.csv',
    'Categoria/CATEGORIA_N1/LL/outputs/forecast_transposed_LSTM_LL_categoria_final.csv.csv',
    'Categoria/CATEGORIA_N1/LL/outputs/forecast_transposed_NHITS_LL_categoria_final.csv.csv',
    'Categoria/CATEGORIA_N1/LL/outputs/forecast_transposed_NBEATSx_LL_categoria_final.csv.csv'
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

# COMMAND ----------

# Concatenar os DataFrames
df_final_categoria = pd.concat([df_DD_categoria, df_LL_categoria, df_JJ_categoria], ignore_index=True)

df_final_categoria

# COMMAND ----------

# MAGIC %md
# MAGIC # GRIFFE

# COMMAND ----------

# DD

# Lista de caminhos possíveis
paths_DD_griffe = [
    'Categoria/Griffe/DD/outputs/forecast_transposed_GRU_DD_griffe_final.csv.csv',
    'Categoria/Griffe/DD/outputs/forecast_transposed_LSTM_DD_categoria_final.csv.csv',
    'Categoria/Griffe/DD/outputs/forecast_transposed_NHITS_DD_categoria_final.csv.csv',
    'Categoria/Griffe/DD/outputs/forecast_transposed_NBEATSx_DD_categoria_final.csv.csv'
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

# COMMAND ----------

# JJ

# Lista de caminhos possíveis
paths_JJ_griffe = [
    'Categoria/Griffe/JJ/outputs/forecast_transposed_GRU_JJ_griffe_final.csv.csv',
    'Categoria/Griffe/JJ/outputs/forecast_transposed_LSTM_JJ_categoria_final.csv.csv',
    'Categoria/Griffe/JJ/outputs/forecast_transposed_NHITS_JJ_categoria_final.csv.csv',
    'Categoria/Griffe/JJ/outputs/forecast_transposed_NBEATSx_JJ_categoria_final.csv.csv'
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

# COMMAND ----------

# LL

# Lista de caminhos possíveis
paths_LL_griffe = [
    'Categoria/Griffe/LL/outputs/forecast_transposed_GRU_LL_griffe_final.csv.csv',
    'Categoria/Griffe/LL/outputs/forecast_transposed_LSTM_LL_categoria_final.csv.csv',
    'Categoria/Griffe/LL/outputs/forecast_transposed_NHITS_LL_categoria_final.csv.csv',
    'Categoria/Griffe/LL/outputs/forecast_transposed_NBEATSx_LL_categoria_final.csv.csv'
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

# COMMAND ----------

# Concatenar os DataFrames
df_final_griffe = pd.concat([df_DD_griffe, df_LL_griffe, df_JJ_griffe], ignore_index=True)

df_final_griffe

# COMMAND ----------

# MAGIC %md
# MAGIC # agrupando dataframes

# COMMAND ----------

# Concatenar os DataFrames
merged_data = pd.concat([df_final_griffe, df_final_categoria, df_final], ignore_index=True)

# COMMAND ----------

# MAGIC %md
# MAGIC # CONVERTENDO SPARK E SALVANDO NA TABELA

# COMMAND ----------

# Criar a SparkSession
spark = SparkSession.builder.appName("pandas to spark").getOrCreate()

# COMMAND ----------

# Converter o DataFrame pandas para Spark
sparkdf = spark.createDataFrame(merged_data)
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

#sql(f"DROP TABLE SANDBOX.FACT_PROJECAO")
#dbutils.fs.rm('/SANDBOX/FACT/FACT_PROJECAO', True)

# COMMAND ----------

#dbutils.fs.rm('/SANDBOX/FACT/FACT_PROJECAO', True)

# COMMAND ----------

ARRUMAR os nomes das colunas

sql("""
    CREATE TABLE IF NOT EXISTS SANDBOX.FACT_PROJECAO (
      MES_ANO varchar(10) COMMENT 'Ano e mês da previsão',
      LL decimal(14,2) COMMENT 'VLF LL VALOR DA PREVISÃO',
      LL_Alfaiataria decimal(14,2) COMMENT 'VLF LL VALOR DA PREVISÃO linha Alfaiataria',
      LL_Jeans_e_Sarja decimal(14,2) COMMENT 'VLF LL VALOR DA PREVISÃO linha Jeans_e_Sarja',
      LL_Malha decimal(14,2) COMMENT 'VLF LL VALOR DA PREVISÃO linha Malha',
      LL_Outros decimal(14,2) COMMENT 'VLF LL VALOR DA PREVISÃO linha Outros',
      LL_Tecido_Plano decimal(14,2) COMMENT 'VLF LL VALOR DA PREVISÃO linha Tecido_Plano',
      LL_Total_Linhas decimal(14,2) COMMENT 'VLF LL VALOR DA PREVISÃO linha Total_Linhas',
      DD decimal(14,2) COMMENT 'VLF DD VALOR DA PREVISÃO',
      DD_Alfaiataria decimal(14,2) COMMENT 'VLF DD VALOR DA PREVISÃO linha Alfaiataria',
      DD_Jeans_e_Sarja decimal(14,2) COMMENT 'VLF DD VALOR DA PREVISÃO linha Jeans_e_Sarja',
      DD_Malha decimal(14,2) COMMENT 'VLF DD VALOR DA PREVISÃO linha Malha',
      DD_Outros decimal(14,2) COMMENT 'VLF DD VALOR DA PREVISÃO linha Malha',
      DD_Tecido_Plano decimal(14,2) COMMENT 'VLF DD VALOR DA PREVISÃO linha Tecido_Plano',
      DD_Total_Linhas decimal(14,2) COMMENT 'VLF DD VALOR DA PREVISÃO linha Total_Linhas',
      JJ decimal(14,2) COMMENT 'VLF JJ VALOR DA PREVISÃO',
      JJ_Alfaiataria decimal(14,2) COMMENT 'VLF JJ VALOR DA PREVISÃO linha Alfaiataria',
      JJ_Jeans_e_Sarja decimal(14,2) COMMENT 'VLF JJ VALOR DA PREVISÃO linha Jeans_e_Sarja',
      JJ_Malha decimal(14,2) COMMENT 'VLF JJ VALOR DA PREVISÃO linha Malha',
      JJ_Outros decimal(14,2) COMMENT 'VLF JJ VALOR DA PREVISÃO linha Outros',
      JJ_Tecido_Plano decimal(14,2) COMMENT 'VLF JJ VALOR DA PREVISÃO linha Tecido_Plano',
      JJ_Total_Linhas decimal(14,2) COMMENT 'VLF JJ VALOR DA PREVISÃO linha Total_Linhas'
    )
    USING DELTA LOCATION '/SANDBOX/FACT/FACT_PROJECAO' --'dbfs:/SANDBOX/FACT/PROJECAO'
    """)

# COMMAND ----------

sparkdf.write \
  .format("delta") \
  .mode("overwrite") \
  .option("overwriteSchema", "true") \
  .save('/SANDBOX/FACT/FACT_PROJECAO') #('SANDBOX/FACT/PROJECAO') #('dbfs:/SANDBOX/FACT/PROJECAO')

# COMMAND ----------

# MAGIC %sql
# MAGIC
# MAGIC select * from sandbox.fact_projecao

# COMMAND ----------


