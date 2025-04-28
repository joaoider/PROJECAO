from pyspark.sql import SparkSession

import pandas as pd
import os
from JJ_configuracoes import marca
#from BB_rodar_modelo_vencedor import modelo_vencedor
from JJ_configuracoes import data_inicio_futr
modelo_vencedor = 'GRU'
output_dir = "outputs"

def ler_forecast_csv(output_dir, marca, modelo_vencedor):
    csv_file_path = os.path.join(output_dir, f'melhor_modelo_forecast_{modelo_vencedor}_final_{marca}.csv')
    
    if not os.path.exists(csv_file_path):
        raise FileNotFoundError(f"Arquivo CSV não encontrado: {csv_file_path}")
    
    print(f"Lendo o arquivo: {csv_file_path}")
    df = pd.read_csv(csv_file_path)
    return df

def salvar_em_parquet(df_pandas, blob_path="/mnt/analytics/planejamento/datascience/forecast_marca/"):
    spark = SparkSession.builder.appName("pandas_to_spark").getOrCreate()
    print('Convertendo para Spark DataFrame.')
    
    sparkdf = spark.createDataFrame(df_pandas)

    # Diretório temporário para cada execução
    temp_blob_path = f"{blob_path}/temp_{marca}_{data_inicio_futr}"

    # Salvar o arquivo parquet temporariamente
    print('Salvando parquet em diretório temporário.')
    (sparkdf
     .coalesce(1)
     .write
     .mode('overwrite')
     .format('parquet')
     .save(temp_blob_path)
    )

    # Nome desejado do arquivo final
    nome_final = f"{marca}_{data_inicio_futr}.parquet"

    # Obter o nome do arquivo Parquet gerado
    parquet_name = [x.name for x in dbutils.fs.ls(temp_blob_path) if x.name.startswith("part")][0]

    # Mover o arquivo parquet gerado para o diretório definitivo com o nome desejado
    dbutils.fs.mv(f"{temp_blob_path}/{parquet_name}", f"{blob_path}/{nome_final}")

    # Remover o diretório temporário usado
    dbutils.fs.rm(temp_blob_path, recurse=True)

    print(f"Parquet salvo com sucesso: {blob_path}/{nome_final}")

df_forecast = ler_forecast_csv(output_dir, marca, modelo_vencedor)
salvar_em_parquet(df_forecast)
