from configuracoes_modelos.imports import *
from LL_configuracoes import marca
from LL_configuracoes import data_inicio_base

def rodar_modelo_vencedor():
    # Definir a pasta de saída como 'outputs'
    pasta_saida = 'outputs'

    # Verificar se o arquivo com os parâmetros do melhor modelo existe
    caminho_parametros = None
    modelo_vencedor = None

    # Identificar o modelo vencedor com base nos arquivos de parâmetros salvos
    if os.path.exists(f'{pasta_saida}/melhor_modelo_parametros_LSTM_{marca}.csv'):
        caminho_parametros = f'{pasta_saida}/melhor_modelo_parametros_LSTM_{marca}.csv'
        modelo_vencedor = 'LSTM'
    elif os.path.exists(f'{pasta_saida}/melhor_modelo_parametros_NHITS_{marca}.csv'):
        caminho_parametros = f'{pasta_saida}/melhor_modelo_parametros_NHITS_{marca}.csv'
        modelo_vencedor = 'NHITS'
    elif os.path.exists(f'{pasta_saida}/melhor_modelo_parametros_GRU_{marca}.csv'):
        caminho_parametros = f'{pasta_saida}/melhor_modelo_parametros_GRU_{marca}.csv'
        modelo_vencedor = 'GRU'
    elif os.path.exists(f'{pasta_saida}/melhor_modelo_parametros_NBEATSx_{marca}.csv'):
        caminho_parametros = f'{pasta_saida}/melhor_modelo_parametros_NBEATSx_{marca}.csv'
        modelo_vencedor = 'NBEATSx'
    else:
        print("Erro: Nenhum arquivo de parâmetros do melhor modelo foi encontrado.")
        return

    print(f"Modelo vencedor: {modelo_vencedor}")

    # Carregar os parâmetros do modelo vencedor (remover colunas de métricas como MAE, RMSE, MAPE)
    parametros_df = pd.read_csv(caminho_parametros)
    parametros_relevantes = parametros_df.drop(columns=['MAE', 'RMSE', 'MAPE']).iloc[0].to_dict()

    # Salvar os parâmetros relevantes em um arquivo JSON para carregar posteriormente
    with open(f'{pasta_saida}/parametros_melhor_modelo_{modelo_vencedor}.json', 'w') as f:
        json.dump(parametros_relevantes, f)

    print(f"Parâmetros do melhor modelo ({modelo_vencedor}) salvos em JSON.")

    # Executar o script correto com base no modelo vencedor
    if modelo_vencedor == 'LSTM':
        script_a_executar = 'main_LSTM_final.py'
    elif modelo_vencedor == 'NHITS':
        script_a_executar = 'main_NHITS_final.py'
    elif modelo_vencedor == 'GRU':
        script_a_executar = 'main_GRU_final.py'
    elif modelo_vencedor == 'NBEATSx':
        script_a_executar = 'main_NBEATSx_final.py'
    else:
        print("Erro: Modelo vencedor desconhecido.")
        return

    try:
        # Subprocesso para executar o script do modelo vencedor
        subprocess.run(['python', script_a_executar], check=True)
        print(f"{modelo_vencedor} executado com sucesso!")
    except subprocess.CalledProcessError as e:
        print(f"Erro ao executar o script {script_a_executar}: {e}")


    # Chamar a função para rodar o modelo vencedor
print('Executando melhor modelo...')
rodar_modelo_vencedor()