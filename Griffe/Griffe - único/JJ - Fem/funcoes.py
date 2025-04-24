import pandas as pd
from JJ_configuracoes import marca
import os
from JJ_configuracoes import data_inicio_base
import subprocess

# Função que verifica as datas faltantes e preenche no dataframe original
def verificar_e_completar_datas_faltantes(df):
    # Calcular automaticamente a menor e a maior data no dataset
    data_inicio_base_verificacao = df['ds'].min()  # A menor data no dataset
    data_fim_base_verificacao = df['ds'].max()     # A maior data no dataset

    # Lista para armazenar datas faltantes para cada unique_id
    datas_faltantes = []

    # Etapa 1: Verificar datas faltantes para cada 'unique_id'
    for unique_id in df['unique_id'].unique():
        # Filtra o dataframe pelo unique_id atual
        df_filtrado = df[df['unique_id'] == unique_id]

        # Gera o intervalo completo de datas para o unique_id
        intervalo_completo = pd.date_range(start=data_inicio_base_verificacao, end=data_fim_base_verificacao, freq='D')

        # Extrai as datas reais presentes no dataset
        datas_reais = pd.to_datetime(df_filtrado['ds'])

        # Encontra as datas faltantes
        faltantes = intervalo_completo.difference(datas_reais)

        # Se houver datas faltantes, armazena-as
        if len(faltantes) > 0:
            datas_faltantes.append({'unique_id': unique_id, 'datas_faltantes': faltantes})

    # Etapa 2: Completar o dataframe com as datas faltantes
    dados_faltantes = []

    # Para cada unique_id com datas faltantes
    for item in datas_faltantes:
        unique_id = item['unique_id']
        faltantes = item['datas_faltantes']

        # Cria um DataFrame com as combinações faltantes e preenche as colunas com 0
        df_faltantes = pd.DataFrame({
            'unique_id': unique_id,      # Repetir o unique_id
            'ds': faltantes,             # Datas faltantes
            'y': 0,                      # Preencher y com 0
            'QLF': 0,                    # Preencher QLF com 0
            'ROL': 0,                    # Preencher ROL com 0
            'CPV': 0                     # Preencher CPV com 0
        })

        # Adiciona o DataFrame ao conjunto de dados faltantes
        dados_faltantes.append(df_faltantes)

    # Concatena todos os dados faltantes em um único DataFrame, se houver algum
    if dados_faltantes:
        df_faltantes_completo = pd.concat(dados_faltantes, ignore_index=True)
        # Concatena o DataFrame original com o DataFrame das datas faltantes
        df_completo = pd.concat([df, df_faltantes_completo], ignore_index=True)
    else:
        df_completo = df.copy()

    # Ordena o DataFrame resultante por unique_id e ds
    df_completo = df_completo.sort_values(by=['unique_id', 'ds']).reset_index(drop=True)

    return df_completo








# Função que verifica as datas faltantes e preenche no dataframe original
def verificar_e_completar_datas_faltantes_sem_unique_id(df):
    # Calcular automaticamente a menor e a maior data no dataset
    data_inicio_base_verificacao = df['ds'].min()  # A menor data no dataset
    data_fim_base_verificacao = df['ds'].max()     # A maior data no dataset

    # Gera o intervalo completo de datas
    intervalo_completo = pd.date_range(start=data_inicio_base_verificacao, end=data_fim_base_verificacao, freq='D')

    # Extrai as datas reais presentes no dataset
    datas_reais = pd.to_datetime(df['ds'])

    # Encontra as datas faltantes
    datas_faltantes = intervalo_completo.difference(datas_reais)

    # Se houver datas faltantes, cria um DataFrame com essas datas e preenche as colunas com 0
    if len(datas_faltantes) > 0:
        df_faltantes = pd.DataFrame({
            'ds': datas_faltantes,  # Datas faltantes
            'unique_id': marca,
            'y': 0,                 # Preencher y com 0
            'QLF': 0,               # Preencher QLF com 0
            'ROL': 0,               # Preencher ROL com 0
            'CPV': 0                # Preencher CPV com 0
        })

        # Exibir o DataFrame de datas faltantes
        print("Datas faltantes:")
        print(df_faltantes)

        # Concatena o DataFrame original com o DataFrame das datas faltantes
        df_completo = pd.concat([df, df_faltantes], ignore_index=True)
    else:
        df_completo = df.copy()

    # Ordena o DataFrame resultante por 'ds'
    df_completo = df_completo.sort_values(by='ds').reset_index(drop=True)

    return df_completo

# Função para salvar as variáveis em um CSV
def salvar_variaveis_csv(marca, freq, horizon, variaveis_futuras, variaveis_historicas, pasta_saida='outputs'):
    if not os.path.exists(pasta_saida):
        os.makedirs(pasta_saida)

    # Criar um DataFrame com as variáveis
    df_variaveis = pd.DataFrame({
        'Marca': [marca],
        'Freq': [freq],
        'Horizon': [horizon],
        'Variáveis Futuras': [', '.join(variaveis_futuras)],  # Concatenar as variáveis futuras
        'Variáveis Históricas': [', '.join(variaveis_historicas)],  # Concatenar as variáveis históricas
        'Data de Início Base': [data_inicio_base]
    })

    # Caminho para o arquivo CSV
    arquivo_csv = os.path.join(pasta_saida, f'variaveis_configuracoes_{marca}.csv')
    
    # Salvar o DataFrame como CSV
    df_variaveis.to_csv(arquivo_csv, index=False)
    print(f"Variáveis salvas com sucesso em {arquivo_csv}")


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

def executar_script(script_name):
    try:
        # Executa o script Python e espera que ele finalize
        result = subprocess.run(['python', script_name], check=True, capture_output=True, text=True)
        # Exibe a saída do script
        print(f"Saída do {script_name}:")
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Erro ao executar {script_name}:")
        print(e.stderr)

def encontrar_melhor_modelo():
    # Definir a pasta de saída como 'outputs'
    pasta_saida = 'outputs'

    # Verificar se a pasta 'outputs' existe
    if not os.path.exists(pasta_saida):
        print(f"Erro: A pasta '{pasta_saida}' não existe.")
        return

    # Caminho para os arquivos CSV dos diferentes modelos
    caminho_lstm = os.path.join(pasta_saida, f'forecast_with_metrics_LSTM_{marca}.csv')
    caminho_nhits = os.path.join(pasta_saida, f'forecast_with_metrics_NHITS_{marca}.csv')
    caminho_gru = os.path.join(pasta_saida, f'forecast_with_metrics_GRU_{marca}.csv')
    caminho_nbeatsx = os.path.join(pasta_saida, f'forecast_with_metrics_NBEATSx_{marca}.csv')

    # Verificar se os arquivos CSV existem
    if not os.path.exists(caminho_lstm) or not os.path.exists(caminho_nhits) or not os.path.exists(caminho_gru) or not os.path.exists(caminho_nbeatsx):
        print("Erro: Um ou mais arquivos de métricas não foram encontrados.")
        return

    # Ler os arquivos CSV para cada modelo
    lstm_df = pd.read_csv(caminho_lstm)
    nhits_df = pd.read_csv(caminho_nhits)
    gru_df = pd.read_csv(caminho_gru)
    nbeatsx_df = pd.read_csv(caminho_nbeatsx)

    # Encontrar a linha com o menor valor de MAPE em cada dataframe
    melhor_lstm = lstm_df.loc[lstm_df['MAPE'].idxmin()]
    melhor_nhits = nhits_df.loc[nhits_df['MAPE'].idxmin()]
    melhor_gru = gru_df.loc[gru_df['MAPE'].idxmin()]
    melhor_nbeatsx = nbeatsx_df.loc[nbeatsx_df['MAPE'].idxmin()]

    # Criar um DataFrame com os melhores de cada modelo
    todos_melhores = pd.DataFrame({
        'Modelo': ['LSTM', 'NHITS', 'GRU', 'NBEATSx'],
        'MAPE': [melhor_lstm['MAPE'], melhor_nhits['MAPE'], melhor_gru['MAPE'], melhor_nbeatsx['MAPE']],
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
    elif melhor_modelo['Modelo'] == 'NBEATSx':
        print(melhor_nbeatsx)
        parametros_melhor_modelo = melhor_nbeatsx
    elif melhor_modelo['Modelo'] == 'NHITS':
        print(melhor_nhits)
        parametros_melhor_modelo = melhor_nhits
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