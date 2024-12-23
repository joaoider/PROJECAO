# Databricks notebook source
import pandas as pd
from pyspark.sql import SparkSession

# COMMAND ----------

# Caminhos dos arquivos CSV
path_LL = 'outputs/melhor_modelo_forecast_GRU_mensal_LL.csv'
path_DD = 'outputs/melhor_modelo_forecast_LSTM_mensal_DD.csv'
path_JJ = 'outputs/melhor_modelo_forecast_LSTM_mensal_JJ.csv'

# COMMAND ----------

data_LL = pd.read_csv(path_LL)
data_DD = pd.read_csv(path_DD)
data_JJ = pd.read_csv(path_JJ)

# COMMAND ----------

# Renomear as colunas
data_LL = data_LL.rename(columns={data_LL.columns[0]: 'mes_ano', data_LL.columns[1]: 'LL'})
data_DD = data_DD.rename(columns={data_DD.columns[0]: 'mes_ano', data_DD.columns[1]: 'DD'})
data_JJ = data_JJ.rename(columns={data_JJ.columns[0]: 'mes_ano', data_JJ.columns[1]: 'JJ'})

# COMMAND ----------

# Combinar os DataFrames
merged_data = data_LL.merge(data_DD, on='mes_ano').merge(data_JJ, on='mes_ano')
merged_data

# COMMAND ----------

# Criar a SparkSession
spark = SparkSession.builder.appName("pandas to spark").getOrCreate()

# COMMAND ----------

# Converter o DataFrame pandas para Spark
sparkdf = spark.createDataFrame(merged_data)
sparkdf.show()

# COMMAND ----------

#sql(f"DROP TABLE SANDBOX.FACT_PROJECAO")
#dbutils.fs.rm('/SANDBOX/FACT/FACT_PROJECAO', True)

# COMMAND ----------

sql("""
    CREATE TABLE IF NOT EXISTS SANDBOX.FACT_PROJECAO (
      MES_ANO varchar(10) COMMENT 'Ano e mês da previsão',
      LL decimal(14,2) COMMENT 'VLF LL VALOR DA PREVISÃO',
      DD decimal(14,2) COMMENT 'VLF DD VALOR DA PREVISÃO',
      JJ decimal(14,2) COMMENT 'VLF JJ VALOR DA PREVISÃO'
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


