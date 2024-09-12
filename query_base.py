from pyspark.sql import SparkSession
from configuracoes import marca

# Inicializar a sessão Spark
spark = SparkSession.builder \
    .appName("Consulta de Liquidacao") \
    .getOrCreate()

print(marca)

if marca == 'JJ':
  marca_sigla = 'John John' 
  griffe = ['John John Masc', 'John John Fem']
  data_inicio_base = '2013-01-01'
  path = 'base_JJ.csv'
if marca == 'DD':
  marca_sigla = 'Dudalina' 
  griffe = ['Dudalina Masc', 'Dudalina Fem']
  data_inicio_base = '2018-01-01'
  path = 'base_DD.csv'
if marca == 'LL':
  marca_sigla = 'Le Lis' 
  griffe = ['Le Lis Blanc Deux', 'Le Lis Casa', 'Le Lis Beaute']
  data_inicio_base = '2013-01-01'
  path = 'base_LL.csv'

# Transformar a lista 'griffe' em uma string SQL-friendly
griffe = "', '".join(griffe)

if marca == 'JJ':
  query = f""" 
    SELECT A.DATA, A.MARCA_SIGLA, split_part(A.ID_LOJA_VENDA, ':',2) as CODIGO_FILIAL, 
           A.CANAL_ORIGEM, A.LINHA, A.GRUPO, A.TIPO_VENDA, A.STATUS_PRODUTO, 
           B.CIDADE, B.UF, C.GRIFFE, sum(A.VLF) AS VLF, SUM(A.QLF) AS QLF
    FROM gold_planejamento.fact_faturamento_B2c A
    JOIN gold.dim_filiais B ON split_part(A.ID_LOJA_VENDA, ':',2) = B.CODIGO_FILIAL
    JOIN gold_planejamento.dim_produtos C on A.PRODUTO = C.PRODUTO
    WHERE A.MARCA_SIGLA = '{marca_sigla}'
      AND C.GRIFFE in ('{griffe}')
      AND DATA >= '{data_inicio_base}'
    GROUP BY A.DATA, A.MARCA_SIGLA, A.ID_LOJA_VENDA, A.CANAL_ORIGEM, A.LINHA, A.GRUPO, A.TIPO_VENDA, A.STATUS_PRODUTO, B.CIDADE, B.UF, C.GRIFFE
    """
  data = spark.sql(query).toPandas()
  # Salvar o DataFrame como um arquivo CSV na mesma pasta
  data.head().to_csv('base_JJ.csv', index=False)

if marca == 'DD':
  query = f""" 
    SELECT A.DATA, A.MARCA_SIGLA, split_part(A.ID_LOJA_VENDA, ':',2) as CODIGO_FILIAL, 
           A.CANAL_ORIGEM, A.LINHA, A.GRUPO, A.TIPO_VENDA, A.STATUS_PRODUTO, 
           B.CIDADE, B.UF, C.GRIFFE, sum(A.VLF) AS VLF, SUM(A.QLF) AS QLF
    FROM gold_planejamento.fact_faturamento_B2c A
    JOIN gold.dim_filiais B ON split_part(A.ID_LOJA_VENDA, ':',2) = B.CODIGO_FILIAL
    JOIN gold_planejamento.dim_produtos C on A.PRODUTO = C.PRODUTO
    WHERE A.MARCA_SIGLA = '{marca_sigla}'
      AND C.GRIFFE in ('{griffe}')
      AND DATA >= '{data_inicio_base}'
    GROUP BY A.DATA, A.MARCA_SIGLA, A.ID_LOJA_VENDA, A.CANAL_ORIGEM, A.LINHA, A.GRUPO, A.TIPO_VENDA, A.STATUS_PRODUTO, B.CIDADE, B.UF, C.GRIFFE
    """
  data = spark.sql(query).toPandas()
  # Salvar o DataFrame como um arquivo CSV na mesma pasta
  data.to_csv('base_DD.csv', index=False)

if marca == 'LL':
  query = f""" 
    SELECT A.DATA, A.MARCA_SIGLA, split_part(A.ID_LOJA_VENDA, ':',2) as CODIGO_FILIAL, 
           A.CANAL_ORIGEM, A.LINHA, A.GRUPO, A.TIPO_VENDA, A.STATUS_PRODUTO, 
           B.CIDADE, B.UF, C.GRIFFE, sum(A.VLF) AS VLF, SUM(A.QLF) AS QLF
    FROM gold_planejamento.fact_faturamento_B2c A
    JOIN gold.dim_filiais B ON split_part(A.ID_LOJA_VENDA, ':',2) = B.CODIGO_FILIAL
    JOIN gold_planejamento.dim_produtos C on A.PRODUTO = C.PRODUTO
    WHERE A.MARCA_SIGLA = '{marca_sigla}'
      AND C.GRIFFE in ('{griffe}')
      AND DATA >= '{data_inicio_base}'
    GROUP BY A.DATA, A.MARCA_SIGLA, A.ID_LOJA_VENDA, A.CANAL_ORIGEM, A.LINHA, A.GRUPO, A.TIPO_VENDA, A.STATUS_PRODUTO, B.CIDADE, B.UF, C.GRIFFE
    """
  data = spark.sql(query).toPandas()
  # Salvar o DataFrame como um arquivo CSV na mesma pasta
  data.to_csv('base_LL.csv', index=False)

data.head(1)

len(data)