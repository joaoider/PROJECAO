# Databricks notebook source
import pandas as pd
from pyspark.sql import SparkSession
import os

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

# Variável para armazenar o caminho do arquivo encontrado
found_path = None

# Verificar se os arquivos existem
for path in paths_DD:
    if os.path.exists(path):
        found_path = path
        print(f"Arquivo encontrado: {found_path}")
        break

if not found_path:
    print("Nenhum arquivo correspondente foi encontrado.")

# COMMAND ----------

# LL

# Lista de caminhos possíveis
paths_LL = [
    'Geral/Geral LL/outputs/melhor_modelo_forecast_LSTM_mensal_LL.csv',
    'Geral/Geral LL/outputs/melhor_modelo_forecast_GRU_mensal_LL.csv',
    'Geral/Geral LL/outputs/melhor_modelo_forecast_NHITS_mensal_LL.csv',
    'Geral/Geral LL/outputs/melhor_modelo_forecast_NBEATSx_mensal_LL.csv'
]

# Variável para armazenar o caminho do arquivo encontrado
found_path = None

# Verificar se os arquivos existem
for path in paths_LL:
    if os.path.exists(path):
        found_path = path
        print(f"Arquivo encontrado: {found_path}")
        break

if not found_path:
    print("Nenhum arquivo correspondente foi encontrado.")

# COMMAND ----------

# JJ

# Lista de caminhos possíveis
paths_JJ = [
    'Geral/Geral JJ/outputs/melhor_modelo_forecast_LSTM_mensal_JJ.csv',
    'Geral/Geral JJ/outputs/melhor_modelo_forecast_GRU_mensal_JJ.csv',
    'Geral/Geral JJ/outputs/melhor_modelo_forecast_NHITS_mensal_JJ.csv',
    'Geral/Geral JJ/outputs/melhor_modelo_forecast_NBEATSx_mensal_JJ.csv'
]

# Variável para armazenar o caminho do arquivo encontrado
found_path = None

# Verificar se os arquivos existem
for path in paths_JJ:
    if os.path.exists(path):
        found_path = path
        print(f"Arquivo encontrado: {found_path}")
        break

if not found_path:
    print("Nenhum arquivo correspondente foi encontrado.")

# COMMAND ----------

#geral
data_LL = pd.read_csv(path_LL)
data_DD = pd.read_csv(path_DD)
data_JJ = pd.read_csv(path_JJ)

# COMMAND ----------

#geral

# Renomear as colunas
data_LL = data_LL.rename(columns={data_LL.columns[0]: 'mes_ano', data_LL.columns[1]: 'LL'})
data_DD = data_DD.rename(columns={data_DD.columns[0]: 'mes_ano', data_DD.columns[1]: 'DD'})
data_JJ = data_JJ.rename(columns={data_JJ.columns[0]: 'mes_ano', data_JJ.columns[1]: 'JJ'})

# COMMAND ----------

# Combinar os DataFrames
merged_data = data_LL.merge(data_DD, on='mes_ano').merge(data_JJ, on='mes_ano').merge(data_LL, on='mes_ano')
merged_data

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

# Variável para armazenar o caminho do arquivo encontrado
found_path = None

# Verificar se os arquivos existem
for path in paths_DD_categorian1:
    if os.path.exists(path):
        found_path = path
        print(f"Arquivo encontrado: {found_path}")
        break

if not found_path:
    print("Nenhum arquivo correspondente foi encontrado.")

# COMMAND ----------

# JJ

# Lista de caminhos possíveis
paths_JJ_categorian1 = [
    'Geral/Geral JJ/outputs/forecast_transposed_GRU_JJ_categoria_final.csv.csv',
    'Geral/Geral JJ/outputs/forecast_transposed_LSTM_JJ_categoria_final.csv.csv',
    'Geral/Geral JJ/outputs/forecast_transposed_NHITS_JJ_categoria_final.csv.csv',
    'Geral/Geral JJ/outputs/forecast_transposed_NBEATSx_JJ_categoria_final.csv.csv'
]

# Variável para armazenar o caminho do arquivo encontrado
found_path = None

# Verificar se os arquivos existem
for path in paths_JJ_categorian1:
    if os.path.exists(path):
        found_path = path
        print(f"Arquivo encontrado: {found_path}")
        break

if not found_path:
    print("Nenhum arquivo correspondente foi encontrado.")

# COMMAND ----------

# LL

# Lista de caminhos possíveis
paths_LL_categorian1 = [
    'Geral/Geral LL/outputs/forecast_transposed_GRU_LL_categoria_final.csv.csv',
    'Geral/Geral LL/outputs/forecast_transposed_LSTM_LL_categoria_final.csv.csv',
    'Geral/Geral LL/outputs/forecast_transposed_NHITS_LL_categoria_final.csv.csv',
    'Geral/Geral LL/outputs/forecast_transposed_NBEATSx_LL_categoria_final.csv.csv'
]

# Variável para armazenar o caminho do arquivo encontrado
found_path = None

# Verificar se os arquivos existem
for path in paths_LL_categorian1:
    if os.path.exists(path):
        found_path = path
        print(f"Arquivo encontrado: {found_path}")
        break

if not found_path:
    print("Nenhum arquivo correspondente foi encontrado.")

# COMMAND ----------

#geral
data_LL_categoria = pd.read_csv(paths_LL_categorian1)
data_DD_categoria = pd.read_csv(paths_DD_categorian1)
data_JJ_categoria = pd.read_csv(paths_JJ_categorian1)

# COMMAND ----------

#categoria

# Adicionar "LL_" às colunas, exceto 'mes_ano'
data_LL_categoria.columns = ['mes_ano' if col == 'mes_ano' else f'LL_{col}' for col in data_LL_categoria.columns]
data_DD_categoria.columns = ['mes_ano' if col == 'mes_ano' else f'DD_{col}' for col in data_DD_categoria.columns]
data_JJ_categoria.columns = ['mes_ano' if col == 'mes_ano' else f'JJ_{col}' for col in data_JJ_categoria.columns]

#data_LLc.rename(columns={'LL_Jeans e Sarja': 'LL_Jeans_e_Sarja'}, inplace=True)
#data_LLc.rename(columns={'LL_Tecido Plano': 'LL_Tecido_Plano'}, inplace=True)
#data_LLc.rename(columns={'LL_Total': 'LL_Total_Linhas'}, inplace=True)

#data_DDc.rename(columns={'DD_Jeans e Sarja': 'DD_Jeans_e_Sarja'}, inplace=True)
#data_DDc.rename(columns={'DD_Tecido Plano': 'DD_Tecido_Plano'}, inplace=True)
#data_DDc.rename(columns={'DD_Total': 'DD_Total_Linhas'}, inplace=True)

#data_JJc.rename(columns={'JJ_Jeans e Sarja': 'JJ_Jeans_e_Sarja'}, inplace=True)
#data_JJc.rename(columns={'JJ_Tecido Plano': 'JJ_Tecido_Plano'}, inplace=True)
#data_JJc.rename(columns={'JJ_Total': 'JJ_Total_Linhas'}, inplace=True)

# COMMAND ----------

# Combinar os DataFrames
merged_data2 = merged_data.merge(data_LL_categoria, on='mes_ano').merge(data_DD_categoria, on='mes_ano').merge(data_JJ_categoria, on='mes_ano')
merged_data2

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

# Variável para armazenar o caminho do arquivo encontrado
found_path = None

# Verificar se os arquivos existem
for path in paths_DD_griffe:
    if os.path.exists(path):
        found_path = path
        print(f"Arquivo encontrado: {found_path}")
        break

if not found_path:
    print("Nenhum arquivo correspondente foi encontrado.")

# COMMAND ----------

# JJ

# Lista de caminhos possíveis
paths_JJ_griffe = [
    'Categoria/Griffe/JJ/outputs/forecast_transposed_GRU_JJ_griffe_final.csv.csv',
    'Categoria/Griffe/JJ/outputs/forecast_transposed_LSTM_JJ_categoria_final.csv.csv',
    'Categoria/Griffe/JJ/outputs/forecast_transposed_NHITS_JJ_categoria_final.csv.csv',
    'Categoria/Griffe/JJ/outputs/forecast_transposed_NBEATSx_JJ_categoria_final.csv.csv'
]

# Variável para armazenar o caminho do arquivo encontrado
found_path = None

# Verificar se os arquivos existem
for path in paths_JJ_griffe:
    if os.path.exists(path):
        found_path = path
        print(f"Arquivo encontrado: {found_path}")
        break

if not found_path:
    print("Nenhum arquivo correspondente foi encontrado.")

# COMMAND ----------

# LL

# Lista de caminhos possíveis
paths_LL_griffe = [
    'Categoria/Griffe/LL/outputs/forecast_transposed_GRU_LL_griffe_final.csv.csv',
    'Categoria/Griffe/LL/outputs/forecast_transposed_LSTM_LL_categoria_final.csv.csv',
    'Categoria/Griffe/LL/outputs/forecast_transposed_NHITS_LL_categoria_final.csv.csv',
    'Categoria/Griffe/LL/outputs/forecast_transposed_NBEATSx_LL_categoria_final.csv.csv'
]

# Variável para armazenar o caminho do arquivo encontrado
found_path = None

# Verificar se os arquivos existem
for path in paths_LL_griffe:
    if os.path.exists(path):
        found_path = path
        print(f"Arquivo encontrado: {found_path}")
        break

if not found_path:
    print("Nenhum arquivo correspondente foi encontrado.")

# COMMAND ----------

#geral
data_LL_griffe = pd.read_csv(paths_LL_griffe)
data_DD_griffe = pd.read_csv(paths_DD_griffe)
data_JJ_griffe = pd.read_csv(paths_JJ_griffe)

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


