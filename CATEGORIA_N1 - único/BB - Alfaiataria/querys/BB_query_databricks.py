#base
from BB_configuracoes import marca


#from pyspark.sql import SparkSession
#spark = SparkSession.builder.getOrCreate()
#spark = SparkSession.getActiveSession()
#spark = SparkSession.builder.master("local[*]").appName("MyApp").getOrCreate()

import os
from pyspark.sql import SparkSession
# Verifique se está em um ambiente Databricks
# Inicializar a sessão Spark de forma condicional


if "DATABRICKS_RUNTIME_VERSION" in os.environ:
    spark = SparkSession.getActiveSession()
    if spark is None:
        spark = SparkSession.builder.getOrCreate()
else:
    # Configuração local
    spark = SparkSession.builder.master("local[*]").appName("MyApp").getOrCreate()


#print(marca)

def get_sales_data(marca, griffe_list, data_inicio, data_fim):
    griffe_condition = ', '.join(f"'{griffe}'" for griffe in griffe_list)
    
    query = f"""
    SELECT A.DATA, D.MARCA_SIGLA, split_part(A.ID_LOJA_VENDA, ':',2) as CODIGO_FILIAL, 
           A.CANAL_ORIGEM, A.LINHA, A.GRUPO, A.CATEGORIA_N1, A.TIPO_VENDA, A.STATUS_PRODUTO, 
           B.CIDADE, B.UF, C.GRIFFE, sum(A.VLF) AS VLF, SUM(A.QLF) AS QLF, 
           sum(A.ROL) AS ROL, sum(A.CPV) AS CPV, AVG(A.VLF) AS MEDIA_VLF, 
           AVG(A.QLF) AS MEDIA_QLF, AVG(A.ROL) AS MEDIA_ROL, AVG(A.CPV) AS MEDIA_CPV
    FROM gold_planejamento.fact_faturamento_B2c A
    JOIN gold.dim_filiais B ON split_part(A.ID_LOJA_VENDA, ':',2) = B.CODIGO_FILIAL
    JOIN gold_planejamento.dim_produtos C on A.PRODUTO = C.PRODUTO
    JOIN gold_planejamento.dim_marcas D ON A.REDE_LOJAS_VENDA = D.REDE_LOJAS
    WHERE D.MARCA_SIGLA = '{marca}' 
      AND C.GRIFFE in ({griffe_condition})
      AND DATA BETWEEN '{data_inicio}' AND '{data_fim}'
    GROUP BY A.DATA, D.MARCA_SIGLA, A.ID_LOJA_VENDA, A.CANAL_ORIGEM, A.LINHA, A.GRUPO, A.CATEGORIA_N1, 
             A.TIPO_VENDA, A.STATUS_PRODUTO, B.CIDADE, B.UF, C.GRIFFE
    """
    
    df = spark.sql(query).toPandas()
    return df

data = get_sales_data('BB', ['Bobô', 'Bobo Casa'], '2013-01-01', '2024-12-31')

data = data[data['CATEGORIA_N1'] == 'Alfaiataria']

print(len(data))
print('data', data.head())

#liquidacao  
def get_liquidacao_data(marca, data_inicio):
    query = f"""
    SELECT * 
    FROM gold.dim_colecoes_liquidacao 
    WHERE marca = '{marca}' 
      AND DATA_INICIO_LIQUIDACAO >= '{data_inicio}'
    """
    
    df = spark.sql(query).toPandas()
    return df

data_liqui = get_liquidacao_data('BB', '2012-01-01')

print(len(data_liqui))
print('data_liqui', data_liqui.head())