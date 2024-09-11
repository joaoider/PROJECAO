# Databricks notebook source
from configuracoes import marca

# COMMAND ----------

print(marca)

# COMMAND ----------

if marca == 'JJ':
  data_inicio_base = '2013-01-01'

  query = f""" 
    SELECT A.DATA, A.MARCA_SIGLA, split_part(A.ID_LOJA_VENDA, ':',2) as CODIGO_FILIAL, 
           A.CANAL_ORIGEM, A.LINHA, A.GRUPO, A.TIPO_VENDA, A.STATUS_PRODUTO, 
           B.CIDADE, B.UF, C.GRIFFE, sum(A.VLF) AS VLF, SUM(A.QLF) AS QLF
    FROM gold_planejamento.fact_faturamento_B2c A
    JOIN gold.dim_filiais B ON split_part(A.ID_LOJA_VENDA, ':',2) = B.CODIGO_FILIAL
    JOIN gold_planejamento.dim_produtos C on A.PRODUTO = C.PRODUTO
    WHERE A.MARCA_SIGLA = 'John John' 
      AND C.GRIFFE in ('John John Masc', 'John John Fem') 
      AND DATA >= '{data_inicio_base}'
    GROUP BY A.DATA, A.MARCA_SIGLA, A.ID_LOJA_VENDA, A.CANAL_ORIGEM, A.LINHA, A.GRUPO, A.TIPO_VENDA, A.STATUS_PRODUTO, B.CIDADE, B.UF, C.GRIFFE
    """

  data = sql(query).toPandas()

  # Salvar o DataFrame como um arquivo CSV na mesma pasta
  data.head().to_csv('base_JJ.csv', index=False)
  path = 'base_JJ.csv'

if marca == 'DD':
  data_inicio_base = '2018-01-01'

  query = f""" 
    SELECT A.DATA, A.MARCA_SIGLA, split_part(A.ID_LOJA_VENDA, ':',2) as CODIGO_FILIAL, 
           A.CANAL_ORIGEM, A.LINHA, A.GRUPO, A.TIPO_VENDA, A.STATUS_PRODUTO, 
           B.CIDADE, B.UF, C.GRIFFE, sum(A.VLF) AS VLF, SUM(A.QLF) AS QLF
    FROM gold_planejamento.fact_faturamento_B2c A
    JOIN gold.dim_filiais B ON split_part(A.ID_LOJA_VENDA, ':',2) = B.CODIGO_FILIAL
    JOIN gold_planejamento.dim_produtos C on A.PRODUTO = C.PRODUTO
    WHERE A.MARCA_SIGLA = 'Dudalina' 
      AND C.GRIFFE in ('Dudalina Masc', 'Dudalina Fem') 
      AND DATA >= '{data_inicio_base}'
    GROUP BY A.DATA, A.MARCA_SIGLA, A.ID_LOJA_VENDA, A.CANAL_ORIGEM, A.LINHA, A.GRUPO, A.TIPO_VENDA, A.STATUS_PRODUTO, B.CIDADE, B.UF, C.GRIFFE
    """

  data = sql(query).toPandas()

  # Salvar o DataFrame como um arquivo CSV na mesma pasta
  data.to_csv('base_DD.csv', index=False)
  path = 'base_DD.csv'

if marca == 'LL':
  data_inicio_base = '2013-01-01'

  query = f""" 
    SELECT A.DATA, A.MARCA_SIGLA, split_part(A.ID_LOJA_VENDA, ':',2) as CODIGO_FILIAL, 
           A.CANAL_ORIGEM, A.LINHA, A.GRUPO, A.TIPO_VENDA, A.STATUS_PRODUTO, 
           B.CIDADE, B.UF, C.GRIFFE, sum(A.VLF) AS VLF, SUM(A.QLF) AS QLF
    FROM gold_planejamento.fact_faturamento_B2c A
    JOIN gold.dim_filiais B ON split_part(A.ID_LOJA_VENDA, ':',2) = B.CODIGO_FILIAL
    JOIN gold_planejamento.dim_produtos C on A.PRODUTO = C.PRODUTO
    WHERE A.MARCA_SIGLA = 'Le Lis' 
      AND C.GRIFFE in ('Le Lis Blanc Deux', 'Le Lis Casa', 'Le Lis Beaute') 
      AND DATA >= '{data_inicio_base}'
    GROUP BY A.DATA, A.MARCA_SIGLA, A.ID_LOJA_VENDA, A.CANAL_ORIGEM, A.LINHA, A.GRUPO, A.TIPO_VENDA, A.STATUS_PRODUTO, B.CIDADE, B.UF, C.GRIFFE
    """

  data = sql(query).toPandas()

  # Salvar o DataFrame como um arquivo CSV na mesma pasta
  data.to_csv('base_LL.csv', index=False)
  path = 'base_LL.csv'

# COMMAND ----------

data.head(1)

# COMMAND ----------

len(data)

# COMMAND ----------

# Para funcionar no Databricks depois retiro o salvamento por csv e deixo só o dataframe pandas para puxar
