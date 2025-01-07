print('query_base.py iniciado')

from pyspark.sql import SparkSession
from configuracoes import marca

# Inicializar a sessão Spark
spark = SparkSession.builder \
    .appName("Consulta de Liquidacao") \
    .getOrCreate()


# Definir um dicionário para as configurações de cada marca
configuracoes_marca = {
    'JJ': {
        'marca_sigla': 'John John',
        'griffe': ['John John Fem', 'John John Masc'],
        'data_inicio_base': '2013-01-01',
        'path': 'base_JJ.csv'
    },
    'DD': {
        'marca_sigla': 'Dudalina',
        'griffe': ['Dudalina Masc', 'Dudalina Fem'],
        'data_inicio_base': '2018-01-01',
        'path': 'base_DD.csv'
    },
    'LL': {
        'marca_sigla': 'Le Lis',
        'griffe': ['Le Lis Blanc Deux', 'Le Lis Casa', 'Le Lis Beaute'],
        'data_inicio_base': '2013-01-01',
        'path': 'base_LL.csv'
    }
}

# Garantir que a variável marca seja uma lista
if isinstance(marca, str):
    marca = [marca]  # Se for string, transformar em lista

# Criar um dicionário para armazenar os DataFrames
dataframes = {}

# Iterar sobre as marcas
for m in marca:
    if m in configuracoes_marca:
        conf = configuracoes_marca[m]
        marca_sigla = conf['marca_sigla']
        griffe = "', '".join(conf['griffe'])  # Transformar lista de griffes em string SQL-friendly
        data_inicio_base = conf['data_inicio_base']
        path = conf['path']

        # Query dinâmica para cada marca
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
        
        # Executar a consulta e converter para Pandas DataFrame
        df = spark.sql(query).toPandas()

        # Salvar o DataFrame como um arquivo CSV na mesma pasta
        #df.head(1).to_csv(path, index=False)
        #print(f"Arquivo salvo para {marca_sigla} em {path}")
        
        # Armazenar o DataFrame no dicionário com um nome baseado na marca
        dataframes[f'data_{m}'] = df

# Exibir o conteúdo do dicionário de DataFrames
#for nome, df in dataframes.items():
    #print(f"\nPrimeira linha do DataFrame {nome}:")
    #print(df.head(1))

print('query_base.py finalizado')