import time
# Marcação de início de execução
start_time = time.time()

# MÓDULO PRINCIPAL
print('main_NHITS_final.py iniciado')

# Importar módulos e dataframes necessários
from configuracoes_modelos.imports import *
from DD_configuracoes import marca
from DD_base import data_neural, futr_df

# Definir o diretório onde os parâmetros estão salvos
output_dir = 'outputs'
json_parametros_path = f'{output_dir}/parametros_melhor_modelo_NHITS.json'

print('Marca: ', marca)
print('###############################')

# Verificar se o arquivo JSON de parâmetros existe
if not os.path.exists(json_parametros_path):
    print(f"Erro: Arquivo de parâmetros {json_parametros_path} não encontrado.")
    exit(0)

# Carregar os parâmetros do modelo vencedor a partir do JSON
with open(json_parametros_path, 'r') as f:
    parametros = json.load(f)

# Exibir os parâmetros carregados
print(f"Parâmetros carregados: {parametros}")

# Atribuir os parâmetros às variáveis correspondentes
max_steps = parametros['max_steps']
learning_rate = parametros['learning_rate']
batch_size = parametros['batch_size']
activation = parametros['activation']
n_blocks = parametros['n_blocks']
mlp_units = parametros['mlp_units']
n_pool_kernel_size = parametros['n_pool_kernel_size']
n_freq_downsample = parametros['n_freq_downsample']
pooling_mode = parametros['pooling_mode']
dropout_prob_theta = parametros['dropout_prob_theta']
scaler_type = parametros['scaler_type']
windows_batch_size = parametros['windows_batch_size']
step_size = parametros['step_size']
random_seed = parametros['random_seed']

# Exibir os parâmetros selecionados
print(f'Parâmetros selecionados: max_steps={max_steps}, learning_rate={learning_rate}, '
      f'batch_size={batch_size}, activation={activation}, n_blocks={n_blocks}, '
      f'mlp_units={mlp_units}, n_pool_kernel_size={n_pool_kernel_size}, '
      f'n_freq_downsample={n_freq_downsample}, pooling_mode={pooling_mode}, '
      f'dropout_prob_theta={dropout_prob_theta}, scaler_type={scaler_type}, '
      f'windows_batch_size={windows_batch_size}, step_size={step_size}, random_seed={random_seed}')

# Inicializa a variável para armazenar o dataframe final de previsões
data_neural_hat_final = None

# Carregar o módulo do modelo NHITS dinamicamente
modulo_modelo = importlib.import_module('models.model_NHITS_final')

# Ajustar para chamar a função correta, no caso do NHITS
funcao_treinar = getattr(modulo_modelo, 'treinar_NHITS')  # Função específica para o NHITS

# Nome para a coluna de previsão
col_name = (f'NHITS_steps{max_steps}_lr{learning_rate}_batch{batch_size}_'
            f'activation{activation}_blocks{n_blocks}_mlp_units{mlp_units}_'
            f'pool_kernel{n_pool_kernel_size}_freq_downsample{n_freq_downsample}_'
            f'pooling{pooling_mode}_dropout{dropout_prob_theta}_scaler{scaler_type}_'
            f'window_batch{windows_batch_size}_step{step_size}_seed{random_seed}')

# Treinar o modelo com os parâmetros carregados
data_neural_hat = funcao_treinar(max_steps, learning_rate, batch_size, activation,
                                 n_blocks, mlp_units, n_pool_kernel_size,
                                 n_freq_downsample, pooling_mode, dropout_prob_theta,
                                 scaler_type, windows_batch_size, step_size, random_seed)

# Verificar se a previsão foi gerada corretamente
if data_neural_hat is not None:
    print("Previsão gerada com sucesso.")
    
    # Renomeia a coluna de previsões com o nome do modelo e parâmetros testados
    data_neural_hat.rename(columns={'NHITS': col_name}, inplace=True)

    # Salvar o resultado final em CSV
    csv_file_path = f'{output_dir}/melhor_modelo_forecast_NHITS_final_{marca}.csv'
    data_neural_hat.to_csv(csv_file_path, index=False)
    print(f"Previsão salva com sucesso: {csv_file_path}")

    # Agora vamos fazer o groupby por mês e somar os valores
    data_neural_hat['ds'] = pd.to_datetime(data_neural_hat['ds'])  # Converter a coluna de datas para datetime
    data_neural_hat['month'] = data_neural_hat['ds'].dt.to_period('M')  # Extrair o mês
    # Agrupar por mês e somar as previsões
    previsao_mensal = data_neural_hat.groupby('month')[col_name].sum().reset_index()
    # Salvar o resultado mensal em um CSV
    csv_mensal_path = f'{output_dir}/melhor_modelo_forecast_NHITS_mensal_{marca}.csv'
    previsao_mensal.to_csv(csv_mensal_path, index=False)
    print(f"Previsão mensal salva com sucesso: {csv_mensal_path}")

    # Plotar as previsões
    data_neural_hat.set_index('ds')[col_name].plot(linewidth=2)

    # Configurações de rótulos e título do gráfico
    plt.ylabel('VLF', fontsize=12)
    plt.xlabel('Date', fontsize=12)
    plt.title(f'Previsões NHITS ({col_name})', fontsize=14)
    plt.grid()

    # Salvar o gráfico como imagem
    plot_file_path = f'{output_dir}/melhor_modelo_plot_image_NHITS_final_{marca}.png'
    plt.savefig(plot_file_path)
    print(f"Gráfico salvo com sucesso: {plot_file_path}")
else:
    print("Erro: Não foi possível gerar a previsão.")

# Exibir o tempo total de execução
end_time = time.time()
execution_time = end_time - start_time
print(f"Tempo de execução total: {execution_time:.2f} segundos")

print('main_NHITS_final.py finalizado')