# Databricks notebook source
df_JJ = sql(""" SELECT A.DATA, A.MARCA_SIGLA, split_part(A.ID_LOJA_VENDA, ':',2) as CODIGO_FILIAL, A.CANAL_ORIGEM, A.LINHA, A.GRUPO, A.TIPO_VENDA, A.STATUS_PRODUTO, B.CIDADE, B.UF, C.GRIFFE, sum(A.VLF) AS VLF, SUM(A.QLF) AS QLF
FROM gold_planejamento.fact_faturamento_B2c A
JOIN gold.dim_filiais B ON split_part(A.ID_LOJA_VENDA, ':',2) = B.CODIGO_FILIAL
JOIN gold_planejamento.dim_produtos C on A.PRODUTO = C.PRODUTO
WHERE A.MARCA_SIGLA = 'John John' and C.GRIFFE in ('John John Masc', 'John John Fem')
--WHERE A.MARCA_SIGLA = 'Dudalina' and C.GRIFFE in ('Dudalina Masc', 'Dudalina Fem')
--WHERE A.MARCA_SIGLA = 'Le Lis' and C.GRIFFE in ('Le Lis Blanc Deux', 'Le Lis Casa', 'Le Lis Beaute')
GROUP BY  A.DATA, A.MARCA_SIGLA, A.ID_LOJA_VENDA, A.CANAL_ORIGEM, A.LINHA, A.GRUPO, A.TIPO_VENDA, A.STATUS_PRODUTO, B.CIDADE, B.UF, C.GRIFFE """).toPandas()

# COMMAND ----------

df_JJ.head()

# COMMAND ----------

df_DD = sql(""" SELECT A.DATA, A.MARCA_SIGLA, split_part(A.ID_LOJA_VENDA, ':',2) as CODIGO_FILIAL, A.CANAL_ORIGEM, A.LINHA, A.GRUPO, A.TIPO_VENDA, A.STATUS_PRODUTO, B.CIDADE, B.UF, C.GRIFFE, sum(A.VLF) AS VLF, SUM(A.QLF) AS QLF
FROM gold_planejamento.fact_faturamento_B2c A
JOIN gold.dim_filiais B ON split_part(A.ID_LOJA_VENDA, ':',2) = B.CODIGO_FILIAL
JOIN gold_planejamento.dim_produtos C on A.PRODUTO = C.PRODUTO
--WHERE A.MARCA_SIGLA = 'John John' and C.GRIFFE in ('John John Masc', 'John John Fem')
WHERE A.MARCA_SIGLA = 'Dudalina' and C.GRIFFE in ('Dudalina Masc', 'Dudalina Fem')
--WHERE A.MARCA_SIGLA = 'Le Lis' and C.GRIFFE in ('Le Lis Blanc Deux', 'Le Lis Casa', 'Le Lis Beaute')
GROUP BY  A.DATA, A.MARCA_SIGLA, A.ID_LOJA_VENDA, A.CANAL_ORIGEM, A.LINHA, A.GRUPO, A.TIPO_VENDA, A.STATUS_PRODUTO, B.CIDADE, B.UF, C.GRIFFE """).toPandas()

# COMMAND ----------

df_DD.head()

# COMMAND ----------

df_LL = sql(""" SELECT A.DATA, A.MARCA_SIGLA, split_part(A.ID_LOJA_VENDA, ':',2) as CODIGO_FILIAL, A.CANAL_ORIGEM, A.LINHA, A.GRUPO, A.TIPO_VENDA, A.STATUS_PRODUTO, B.CIDADE, B.UF, C.GRIFFE, sum(A.VLF) AS VLF, SUM(A.QLF) AS QLF
FROM gold_planejamento.fact_faturamento_B2c A
JOIN gold.dim_filiais B ON split_part(A.ID_LOJA_VENDA, ':',2) = B.CODIGO_FILIAL
JOIN gold_planejamento.dim_produtos C on A.PRODUTO = C.PRODUTO
--WHERE A.MARCA_SIGLA = 'John John' and C.GRIFFE in ('John John Masc', 'John John Fem')
--WHERE A.MARCA_SIGLA = 'Dudalina' and C.GRIFFE in ('Dudalina Masc', 'Dudalina Fem')
WHERE A.MARCA_SIGLA = 'Le Lis' and C.GRIFFE in ('Le Lis Blanc Deux', 'Le Lis Casa', 'Le Lis Beaute')
GROUP BY  A.DATA, A.MARCA_SIGLA, A.ID_LOJA_VENDA, A.CANAL_ORIGEM, A.LINHA, A.GRUPO, A.TIPO_VENDA, A.STATUS_PRODUTO, B.CIDADE, B.UF, C.GRIFFE """).toPandas()

# COMMAND ----------

df_LL.head()
