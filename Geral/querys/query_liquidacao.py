print('query_liquidacao.py iniciado')

from pyspark.sql import SparkSession
from configuracoes import marca

# Inicializar a sessão Spark
spark = SparkSession.builder \
    .appName("Consulta de Liquidacao") \
    .getOrCreate()
    
data_inicio_liqui = '2012-01-01'

# Garantir que a variável marca seja uma lista
if isinstance(marca, str):
    marca = [marca]  # Se for string, transformar em lista

# Criar um dicionário para armazenar os DataFrames
dataframes_liqui = {}

# Iterar sobre as marcas
for m in marca:
    path_liqui = f'base_liqui_{m}.csv'  # Gerar o caminho do arquivo dinamicamente

    # Query dinâmica para cada marca
    query = f""" 
        select * from gold.dim_colecoes_liquidacao 
        where marca = '{m}' and DATA_INICIO_LIQUIDACAO >= '{data_inicio_liqui}' """
    
    # Executar a consulta e converter para Pandas DataFrame
    data_liqui = spark.sql(query).toPandas()

    # Salvar o DataFrame como um arquivo CSV, com nome distinto para cada marca
    #data_liqui.head(1).to_csv(path_liqui, index=False)
    #print(f"Arquivo salvo para {m} em {path_liqui}")
    
    # Armazenar o DataFrame no dicionário com um nome baseado na marca
    dataframes_liqui[f'data_liqui_{m}'] = data_liqui

# Exibir a primeira linha de cada DataFrame processado e o número total de registros
#for nome, df in dataframes_liqui.items():
    #print(f"\nPrimeira linha do DataFrame {nome}:")
    #print(df.head(1))

print('query_liquidacao.py finalizado')