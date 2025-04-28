from pyspark.sql import SparkSession

import pandas as pd
import os
from DD_configuracoes import marca
#from BB_rodar_modelo_vencedor import modelo_vencedor
from DD_configuracoes import data_inicio_futr
modelo = 'GRU'
griffe = 'masc'
output_dir = "outputs"

def ler_forecast_csv(output_dir, marca, modelo_vencedor):
    csv_file_path = os.path.join(output_dir, f'forecast_{modelo}_{marca}_{griffe}.csv')
    
    if not os.path.exists(csv_file_path):
        raise FileNotFoundError(f"Arquivo CSV não encontrado: {csv_file_path}")
    
    print(f"Lendo o arquivo: {csv_file_path}")
    df = pd.read_csv(csv_file_path)
    return df

def salvar_em_parquet(df_pandas, blob_path="/mnt/analytics/planejamento/datascience/forecast_marca_griffe/"):
    spark = SparkSession.builder.appName("pandas_to_spark").getOrCreate()
    print('convertendo para spark.')
    sparkdf = spark.createDataFrame(df_pandas)

    # Salvar como Parquet
    (sparkdf
     .coalesce(1)
     .write
     .mode('overwrite')
     .format('parquet')
     .save(blob_path)
    )

    # Nome desejado do arquivo final
    print('salvando parquet.')
    nome_final = f"{marca}_{griffe}_{data_inicio_futr}.parquet"

    # Renomear arquivo Parquet gerado para o nome final desejado
    parquet_name = [x.name for x in dbutils.fs.ls(blob_path) if x.name.startswith("part")][0]

    dbutils.fs.mv(f"{blob_path}/{parquet_name}", f"{blob_path}/{nome_final}")

    # Remover arquivos extras que não sejam o arquivo parquet final
    for file in dbutils.fs.ls(blob_path):
        if file.name != nome_final:
            dbutils.fs.rm(f"{blob_path}/{file.name}")
    print('parquet salvo.')


df_forecast = ler_forecast_csv(output_dir, marca, modelo)
salvar_em_parquet(df_forecast)
