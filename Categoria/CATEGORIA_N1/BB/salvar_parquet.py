from pyspark.sql import SparkSession

import pandas as pd
import os
from BB_configuracoes import marca
modelo = 'GRU'
sufixo = 'categoria'
output_dir = "outputs"

def ler_forecast_csv(output_dir, marca, modelo="GRU", sufixo="categoria_final"):
    """
    Lê um arquivo CSV de previsão com base no modelo e marca fornecidos.

    Parâmetros:
    - output_dir: Caminho do diretório onde o CSV está salvo.
    - marca: Nome da marca usado no nome do arquivo.
    - modelo: Nome do modelo utilizado (padrão: 'GRU').
    - sufixo: Sufixo usado no nome do arquivo (padrão: 'categoria_final').

    Retorna:
    - Um DataFrame pandas com os dados lidos.
    """
    csv_file_path = os.path.join(output_dir, f'forecast_{modelo}_{marca}_{sufixo}.csv')
    
    if not os.path.exists(csv_file_path):
        raise FileNotFoundError(f"Arquivo CSV não encontrado: {csv_file_path}")
    
    print(f"Lendo o arquivo: {csv_file_path}")
    df = pd.read_csv(csv_file_path)
    return df

def salvar_em_parquet(df_pandas, blob_path="/mnt/analytics/planejamento/datascience/", nome_final="data.parquet"):
    """
    Converte um DataFrame pandas para Spark, salva como arquivo Parquet no Blob Storage
    e renomeia o arquivo final.

    Parâmetros:
    - df_pandas: DataFrame do pandas a ser convertido.
    - blob_path: Caminho no Blob Storage onde o arquivo será salvo.
    - nome_final: Nome final do arquivo Parquet.
    """
    # Criar a SparkSession (caso não exista)
    spark = SparkSession.builder.appName("pandas to spark").getOrCreate()

    # Converter para Spark DataFrame
    sparkdf = spark.createDataFrame(df_pandas)

    # Salvar como um único arquivo Parquet
    (sparkdf
     .coalesce(1)
     .write
     .mode('overwrite')
     .format('parquet')
     .save(blob_path)
    )

    # Obter o nome do arquivo gerado
    parquet_name = [x.name for x in dbutils.fs.ls(blob_path) if "part" in x.name][0]

    # Renomear o arquivo para o nome final desejado
    dbutils.fs.mv(f"{blob_path}/{parquet_name}", f"{blob_path}/{nome_final}")

    # Remover arquivos extras
    for file in dbutils.fs.ls(blob_path):
        if "part" not in file.name and file.name != nome_final:
            dbutils.fs.rm(f"{blob_path}/{file.name}")



df_forecast = ler_forecast_csv(output_dir, marca)
salvar_em_parquet(df_forecast)
