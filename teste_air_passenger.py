import subprocess
import pandas as pd
import os
from datetime import datetime

def encontrar_melhor_modelo():
    # Obter a data atual
    data_hoje = datetime.now().strftime('%Y-%m-%d')

    # Criar o diretório 'outputs/data_hoje' se não existir
    pasta_saida = f'outputs/{data_hoje}'
    if not os.path.exists(pasta_saida):
        os.makedirs(pasta_saida)

    # Caminho para os arquivos CSV dentro da pasta com a data de hoje
    caminho_lstm = os.path.join(pasta_saida, 'forecast_with_metrics_LSTM.csv').replace("\\", "/")
    caminho_nhits = os.path.join(pasta_saida, 'forecast_with_metrics_NHITS.csv').replace("\\", "/")
    caminho_gru = os.path.join(pasta_saida, 'forecast_with_metrics_GRU.csv').replace("\\", "/")

    # Ler os arquivos CSV para cada modelo a partir da pasta com a data de hoje
    lstm_df = pd.read_csv(caminho_lstm)
    nhits_df = pd.read_csv(caminho_nhits)
    gru_df = pd.read_csv(caminho_gru)

    # Encontrar a linha com os menores valores de MAE, MSE, RMSE e MAPE em cada dataframe
    melhor_lstm = lstm_df.loc[lstm_df[['MAE', 'MSE', 'RMSE', 'MAPE']].sum(axis=1).idxmin()]
    melhor_nhits = nhits_df.loc[nhits_df[['MAE', 'MSE', 'RMSE', 'MAPE']].sum(axis=1).idxmin()]
    melhor_gru = gru_df.loc[gru_df[['MAE', 'MSE', 'RMSE', 'MAPE']].sum(axis=1).idxmin()]

    # Criar um DataFrame com os melhores de cada modelo
    todos_melhores = pd.DataFrame({
        'Modelo': ['LSTM', 'NHITS', 'GRU'],
        'MAE': [melhor_lstm['MAE'], melhor_nhits['MAE'], melhor_gru['MAE']],
        'MSE': [melhor_lstm['MSE'], melhor_nhits['MSE'], melhor_gru['MSE']],
        'RMSE': [melhor_lstm['RMSE'], melhor_nhits['RMSE'], melhor_gru['RMSE']],
        'MAPE': [melhor_lstm['MAPE'], melhor_nhits['MAPE'], melhor_gru['MAPE']],
    })

    # Encontrar o melhor modelo baseado na soma de MAE, MSE, RMSE e MAPE
    melhor_modelo = todos_melhores.loc[todos_melhores[['MAE', 'MSE', 'RMSE', 'MAPE']].sum(axis=1).idxmin()]

    # Exibir o melhor modelo e seus parâmetros
    print(f"O melhor modelo é o {melhor_modelo['Modelo']} com os seguintes parâmetros:")

    # Inicializar uma variável para armazenar os parâmetros do melhor modelo
    parametros_melhor_modelo = None

    # Exibir e salvar os parâmetros do melhor modelo
    if melhor_modelo['Modelo'] == 'LSTM':
        print(melhor_lstm)
        parametros_melhor_modelo = melhor_lstm
    elif melhor_modelo['Modelo'] == 'NHITS':
        print(melhor_nhits)
        parametros_melhor_modelo = melhor_nhits
    else:
        print(melhor_gru)
        parametros_melhor_modelo = melhor_gru

    # Criar um DataFrame com os parâmetros do melhor modelo
    df_parametros_melhor_modelo = pd.DataFrame([parametros_melhor_modelo])

    # Salvar o DataFrame com os parâmetros em um arquivo CSV dentro da pasta com a data de hoje
    arquivo_csv = f'{pasta_saida}/melhor_modelo_parametros_{melhor_modelo["Modelo"]}.csv'
    df_parametros_melhor_modelo.to_csv(arquivo_csv, index=False)

    print(f"Parâmetros do melhor modelo ({melhor_modelo['Modelo']}) salvos com sucesso em {arquivo_csv}.")

if __name__ == "__main__":
    encontrar_melhor_modelo()