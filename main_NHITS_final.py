import time
# Marcação de início de execução
start_time = time.time()

# MÓDULO PRINCIPAL
print('main_NHITS_final.py iniciado')

# Importar módulos e dataframes necessários
from configuracoes.imports import *
from configuracoes.configuracoes_NHITS import marca
from base import data_neural, futr_df

print('Marca: ', marca)
print('###############################')

# Criar a pasta com a data do dia, se não existir
data_atual = datetime.now().strftime('%Y-%m-%d')
horario_atual = datetime.now().strftime('%H-%M-%S')
output_dir = f'outputs/{data_atual}'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Inicializa a variável para armazenar o dataframe final de previsões
data_neural_hat_final = None

# Carregar o módulo do modelo NHITS dinamicamente
modulo_modelo = importlib.import_module('models.model_NHITS_final')

# Ajustar para chamar a função correta, no caso do NHITS
funcao_treinar = getattr(modulo_modelo, 'treinar_NHITS')  # Função específica para o NHITS

# Parâmetros selecionados para a previsão
max_steps = 1
learning_rate = 0.001
batch_size = 32
activation = 'ReLU'
n_blocks = [1, 1, 1]
mlp_units = [[512, 512], [512, 512], [512, 512]]
n_pool_kernel_size = [2, 2, 1]
n_freq_downsample = [4, 2, 1]
pooling_mode = 'MaxPool1d'
dropout_prob_theta = 0.0
scaler_type = 'robust'
windows_batch_size = 1024
step_size = 1
random_seed = 1

# Nome para a coluna de previsão
col_name = (f'NHITS_steps{max_steps}_lr{learning_rate}_batch{batch_size}_'
            f'activation{activation}_blocks{n_blocks}_mlp_units{mlp_units}_'
            f'pool_kernel{n_pool_kernel_size}_freq_downsample{n_freq_downsample}_'
            f'pooling{pooling_mode}_dropout{dropout_prob_theta}_scaler{scaler_type}_'
            f'window_batch{windows_batch_size}_step{step_size}_seed{random_seed}')

print(f'Parâmetros selecionados: max_steps={max_steps}, learning_rate={learning_rate}, '
      f'batch_size={batch_size}, activation={activation}, n_blocks={n_blocks}, '
      f'mlp_units={mlp_units}, n_pool_kernel_size={n_pool_kernel_size}, '
      f'n_freq_downsample={n_freq_downsample}, pooling_mode={pooling_mode}, '
      f'dropout_prob_theta={dropout_prob_theta}, scaler_type={scaler_type}, '
      f'windows_batch_size={windows_batch_size}, step_size={step_size}, random_seed={random_seed}')

# Treinar o modelo com os parâmetros selecionados
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
    csv_file_path = f'{output_dir}/forecast_NHITS_final_{horario_atual}.csv'
    data_neural_hat.to_csv(csv_file_path, index=False)
    print(f"Previsão salva com sucesso: {csv_file_path}")

    # Plotar as previsões
    data_neural_hat.set_index('ds')[col_name].plot(linewidth=2)

    # Configurações de rótulos e título do gráfico
    plt.ylabel('VLF', fontsize=12)
    plt.xlabel('Date', fontsize=12)
    plt.title(f'Previsões NHITS ({col_name})', fontsize=14)
    plt.grid()

    # Salvar o gráfico como imagem
    plot_file_path = f'{output_dir}/plot_image_NHITS_final_{horario_atual}.png'
    plt.savefig(plot_file_path)
    print(f"Gráfico salvo com sucesso: {plot_file_path}")
else:
    print("Erro: Não foi possível gerar a previsão.")

# Exibir o tempo total de execução
end_time = time.time()
execution_time = end_time - start_time
print(f"Tempo de execução total: {execution_time:.2f} segundos")

print('main_NHITS.py finalizado')