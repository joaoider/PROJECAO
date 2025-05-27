from pyspark.sql import SparkSession
import pandas as pd
import os
from DD_configuracoes import marca, data_inicio_futr

with open('outputs/modelo_vencedor.txt', 'r') as f:
    modelo_vencedor = f.read().strip()
print(f"Modelo vencedor carregado: {modelo_vencedor}")

output_dir = "outputs"

def ler_forecast_csv(output_dir, marca, modelo_vencedor):
    csv_file_path = os.path.join(output_dir, f'melhor_modelo_forecast_{modelo_vencedor}_final_{marca}.csv')
    if not os.path.exists(csv_file_path):
        raise FileNotFoundError(f"Arquivo CSV não encontrado: {csv_file_path}")
    print(f"Lendo o arquivo: {csv_file_path}")
    df = pd.read_csv(csv_file_path)
    # Identificar a terceira coluna (que não é 'unique_id' nem 'ds')
    outras_colunas = [col for col in df.columns if col not in ['unique_id', 'ds']]
    if len(outras_colunas) != 1:
        raise ValueError("Esperava exatamente uma terceira coluna além de 'unique_id' e 'ds'.")
    terceira_coluna = outras_colunas[0]
    # Renomear para 'value' e criar a coluna 'atributos'
    df['atributos'] = terceira_coluna
    df = df.rename(columns={terceira_coluna: 'value'})
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
