import pandas as pd
from pyspark.sql import SparkSession

# Caminhos dos arquivos CSV
path_LL = 'outputs/LL/melhor_modelo_forecast_GRU_mensal_LL.csv'
path_DD = 'outputs/DD/melhor_modelo_forecast_GRU_mensal_DD.csv'
path_JJ = 'outputs/JJ/melhor_modelo_forecast_GRU_mensal_JJ.csv'

data_LL = pd.read_csv(path_LL)
data_DD = pd.read_csv(path_DD)
data_JJ = pd.read_csv(path_JJ)

# Renomear as colunas
data_LL = data_LL.rename(columns={data_LL.columns[0]: 'mes_ano', data_LL.columns[1]: 'LL'})
data_DD = data_DD.rename(columns={data_DD.columns[0]: 'mes_ano', data_DD.columns[1]: 'DD'})
data_JJ = data_JJ.rename(columns={data_JJ.columns[0]: 'mes_ano', data_JJ.columns[1]: 'JJ'})

# Combinar os DataFrames
merged_data = data_LL.merge(data_DD, on='mes_ano').merge(data_JJ, on='mes_ano')

# Criar a SparkSession
spark = SparkSession.builder.appName("pandas to spark").getOrCreate()

# Converter o DataFrame pandas para Spark
sparkdf = spark.createDataFrame(merged_data)

sparkdf.show()

sql("""
    CREATE TABLE IF NOT EXISTS SANDBOX.FACT_PROJECAO (
      MES_ANO varchar(10) COMMENT 'Ano e mês da previsão',
      MARCA decimal(14,2) COMMENT 'VLF VALOR DA PREVISÃO'
    )
    USING DELTA LOCATION 'dbfs:/SANDBOX/FACT/PROJECAO'  --'SANDBOX/FACT/PROJECAO'
    """)

sparkdf.write \
  .format("delta") \
  .mode("overwrite") \
  .saveAsTable('dbfs:/SANDBOX/FACT/PROJECAO') #('SANDBOX/FACT/PROJECAO')