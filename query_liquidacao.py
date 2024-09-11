# Databricks notebook source
from configuracoes import marca

# COMMAND ----------

print(marca)

# COMMAND ----------

if marca == 'JJ':
  data = sql(""" select * from gold.dim_colecoes_liquidacao where marca = 'JJ' and DATA_INICIO_LIQUIDACAO >= '2012-01-01' """).toPandas()
  # Salvar o DataFrame como um arquivo CSV na mesma pasta
  data.to_csv('base_liqui_JJ.csv', index=False)
  path_liqui = 'base_liqui_JJ.csv'
if marca == 'DD':
  data = sql(""" select * from gold.dim_colecoes_liquidacao where marca = 'DD' and DATA_INICIO_LIQUIDACAO >= '2012-01-01' """).toPandas()
  # Salvar o DataFrame como um arquivo CSV na mesma pasta
  data.to_csv('base_liqui_DD.csv', index=False)
  path_liqui = 'base_liqui_DD.csv'
if marca == 'LL':
  data = sql(""" select * from gold.dim_colecoes_liquidacao where marca = 'LL' and DATA_INICIO_LIQUIDACAO >= '2012-01-01' """).toPandas()
  # Salvar o DataFrame como um arquivo CSV na mesma pasta
  data.to_csv('base_liqui_LL.csv', index=False)
  path_liqui = 'base_liqui_LL.csv'

# COMMAND ----------


