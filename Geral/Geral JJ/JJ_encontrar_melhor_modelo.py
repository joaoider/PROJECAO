import pandas as pd
from JJ_configuracoes import marca
import os
from JJ_configuracoes import data_inicio_base
import subprocess

# Função para excluir arquivos antigos que começam com "melhor_modelo"
def excluir_arquivos_antigos(pasta, prefixo):
    # Verifica todos os arquivos na pasta
    for arquivo in os.listdir(pasta):
        # Se o arquivo começa com o prefixo "melhor_modelo"
        if arquivo.startswith(prefixo):
            caminho_arquivo = os.path.join(pasta, arquivo)
            try:
                # Exclui o arquivo
                os.remove(caminho_arquivo)
                print(f"Arquivo removido: {caminho_arquivo}")
            except Exception as e:
                print(f"Erro ao remover o arquivo {caminho_arquivo}: {e}")

def encontrar_melhor_modelo():
    # Definir a pasta de saída como 'outputs'
    pasta_saida = 'outputs'

    # Verificar se a pasta 'outputs' existe
    if not os.path.exists(pasta_saida):
        print(f"Erro: A pasta '{pasta_saida}' não existe.")
        return

    # Caminho para os arquivos CSV dos diferentes modelos
    caminho_lstm = os.path.join(pasta_saida, f'forecast_with_metrics_LSTM_{marca}.csv')
    #caminho_nhits = os.path.join(pasta_saida, f'forecast_with_metrics_NHITS_{marca}.csv')
    caminho_gru = os.path.join(pasta_saida, f'forecast_with_metrics_GRU_{marca}.csv')
    #caminho_nbeatsx = os.path.join(pasta_saida, f'forecast_with_metrics_NBEATSx_{marca}.csv')

    # Verificar se os arquivos CSV existem
    if not os.path.exists(caminho_lstm) or not os.path.exists(caminho_gru):
        print("Erro: Um ou mais arquivos de métricas não foram encontrados.")
        return

    # Ler os arquivos CSV para cada modelo
    lstm_df = pd.read_csv(caminho_lstm)
    #nhits_df = pd.read_csv(caminho_nhits)
    gru_df = pd.read_csv(caminho_gru)
    #nbeatsx_df = pd.read_csv(caminho_nbeatsx)

    # Encontrar a linha com o menor valor de MAPE em cada dataframe
    melhor_lstm = lstm_df.loc[lstm_df['MAPE'].idxmin()]
    #melhor_nhits = nhits_df.loc[nhits_df['MAPE'].idxmin()]
    melhor_gru = gru_df.loc[gru_df['MAPE'].idxmin()]
    #melhor_nbeatsx = nbeatsx_df.loc[nbeatsx_df['MAPE'].idxmin()]

    # Criar um DataFrame com os melhores de cada modelo
    todos_melhores = pd.DataFrame({
        'Modelo': ['LSTM', 'GRU'],
        'MAPE': [melhor_lstm['MAPE'], melhor_gru['MAPE']],
    })

    # Encontrar o melhor modelo baseado apenas no MAPE
    melhor_modelo = todos_melhores.loc[todos_melhores['MAPE'].idxmin()]

    # Exibir o melhor modelo e seus parâmetros
    print(f"O melhor modelo é o {melhor_modelo['Modelo']} com MAPE de {melhor_modelo['MAPE']}")


    # Inicializar uma variável para armazenar os parâmetros do melhor modelo
    parametros_melhor_modelo = None

    # Exibir e salvar os parâmetros do melhor modelo
    if melhor_modelo['Modelo'] == 'LSTM':
        print(melhor_lstm)
        parametros_melhor_modelo = melhor_lstm
    else:
        print(melhor_gru)
        parametros_melhor_modelo = melhor_gru

    # Excluir os arquivos antigos que começam com "melhor_modelo"
    excluir_arquivos_antigos(pasta_saida, "melhor_modelo")

    # Criar um DataFrame com os parâmetros do melhor modelo
    df_parametros_melhor_modelo = pd.DataFrame([parametros_melhor_modelo])

    # Salvar o DataFrame com os parâmetros em um arquivo CSV dentro da pasta 'outputs'
    arquivo_csv = f'{pasta_saida}/melhor_modelo_parametros_{melhor_modelo["Modelo"]}_{marca}.csv'
    df_parametros_melhor_modelo.to_csv(arquivo_csv, index=False)

    print(f"Parâmetros do melhor modelo ({melhor_modelo['Modelo']}) salvos com sucesso em {arquivo_csv}.")


print('Procurando melhor modelo...')
encontrar_melhor_modelo()