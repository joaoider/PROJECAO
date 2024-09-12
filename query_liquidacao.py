from pyspark.sql import SparkSession
from configuracoes import marca

# Inicializar a sessão Spark
spark = SparkSession.builder \
    .appName("Consulta de Liquidacao") \
    .getOrCreate()

print(marca)
data_inicio_liqui = '2012-01-01'

if marca == 'JJ':
  path_liqui = 'base_liqui_JJ.csv'
  query = f""" 
  select * from gold.dim_colecoes_liquidacao where marca = '{marca}' and DATA_INICIO_LIQUIDACAO >= '{data_inicio_liqui}' """
  data_liqui = spark.sql(query).toPandas()
  # Salvar o DataFrame como um arquivo CSV na mesma pasta
  data_liqui.to_csv('base_liqui_JJ.csv', index=False)
  
if marca == 'DD':
  path_liqui = 'base_liqui_DD.csv'
  query = f""" 
    select * from gold.dim_colecoes_liquidacao where marca = '{marca}' and DATA_INICIO_LIQUIDACAO >= '{data_inicio_liqui}' """
  data_liqui = spark.sql(query).toPandas()
  # Salvar o DataFrame como um arquivo CSV na mesma pasta
  data_liqui.to_csv('base_liqui_DD.csv', index=False)
  
if marca == 'LL':
  path_liqui = 'base_liqui_LL.csv'
  query = f""" 
    select * from gold.dim_colecoes_liquidacao where marca = '{marca}' and DATA_INICIO_LIQUIDACAO >= '{data_inicio_liqui}' """
  # Salvar o DataFrame como um arquivo CSV na mesma pasta
  data_liqui = spark.sql(query).toPandas()
  data_liqui.to_csv('base_liqui_LL.csv', index=False)
