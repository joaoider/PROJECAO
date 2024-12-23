# Databricks notebook source
import pandas as pd
from pyspark.sql import SparkSession

# COMMAND ----------

# Caminhos dos arquivos CSV
path_LL = 'outputs/LL/melhor_modelo_forecast_GRU_mensal_LL.csv'
path_LLc = 'outputs/forecast_transposed_GRU_DD_categoria_final.csv'
path_DD = 'outputs/DD/melhor_modelo_forecast_LSTM_mensal_DD.csv'
path_DDc = 'outputs/forecast_transposed_GRU_DD_categoria_final.csv'
path_JJ = 'outputs/JJ/melhor_modelo_forecast_LSTM_mensal_JJ.csv'
path_JJc = 'outputs/forecast_transposed_GRU_DD_categoria_final.csv'

# COMMAND ----------

data_LL = pd.read_csv(path_LL)
data_LLc = pd.read_csv(path_LLc)
data_DD = pd.read_csv(path_DD)
data_DDc = pd.read_csv(path_DDc)
data_JJ = pd.read_csv(path_JJ)
data_JJc = pd.read_csv(path_JJc)

# COMMAND ----------

data_JJc.head(1)

# COMMAND ----------

# Renomear as colunas
data_LL = data_LL.rename(columns={data_LL.columns[0]: 'mes_ano', data_LL.columns[1]: 'LL'})
data_DD = data_DD.rename(columns={data_DD.columns[0]: 'mes_ano', data_DD.columns[1]: 'DD'})
data_JJ = data_JJ.rename(columns={data_JJ.columns[0]: 'mes_ano', data_JJ.columns[1]: 'JJ'})

# Adicionar "LL_" às colunas, exceto 'mes_ano'
data_LLc.columns = ['mes_ano' if col == 'mes_ano' else f'LL_{col}' for col in data_LLc.columns]
data_DDc.columns = ['mes_ano' if col == 'mes_ano' else f'DD_{col}' for col in data_DDc.columns]
data_JJc.columns = ['mes_ano' if col == 'mes_ano' else f'JJ_{col}' for col in data_JJc.columns]

data_LLc.rename(columns={'LL_Jeans e Sarja': 'LL_Jeans_e_Sarja'}, inplace=True)
data_LLc.rename(columns={'LL_Tecido Plano': 'LL_Tecido_Plano'}, inplace=True)
data_LLc.rename(columns={'LL_Total': 'LL_Total_Linhas'}, inplace=True)

data_DDc.rename(columns={'DD_Jeans e Sarja': 'DD_Jeans_e_Sarja'}, inplace=True)
data_DDc.rename(columns={'DD_Tecido Plano': 'DD_Tecido_Plano'}, inplace=True)
data_DDc.rename(columns={'DD_Total': 'DD_Total_Linhas'}, inplace=True)

data_JJc.rename(columns={'JJ_Jeans e Sarja': 'JJ_Jeans_e_Sarja'}, inplace=True)
data_JJc.rename(columns={'JJ_Tecido Plano': 'JJ_Tecido_Plano'}, inplace=True)
data_JJc.rename(columns={'JJ_Total': 'JJ_Total_Linhas'}, inplace=True)

# COMMAND ----------

# Combinar os DataFrames
merged_data = data_LL.merge(data_LLc, on='mes_ano').merge(data_DD, on='mes_ano').merge(data_DDc, on='mes_ano').merge(data_JJ, on='mes_ano').merge(data_JJc, on='mes_ano')
merged_data

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


