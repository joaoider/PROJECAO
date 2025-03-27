import time
# Marcação de início de execução
start_time = time.time()

# MÓDULO PRINCIPAL
print('main_NHITS.py iniciado')

# Importar módulos e dataframes necessários
from configuracoes_modelos.imports import *
from BB_configuracoes import marca
from configuracoes_modelos.configuracoes_NHITS import gerar_combinacoes_parametros
from BB_base import data_neural_train, data_neural_test  # Certifique-se de que 'data_neural_test' tenha a coluna 'y'

print('Marca: ', marca)
print('###############################')

# Criar a pasta com a data do dia, se não existir
data_atual = datetime.now().strftime('%Y-%m-%d')
horario_atual = datetime.now().strftime('%H-%M-%S')
output_dir = 'outputs'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Inicializa a variável para armazenar o dataframe final de previsões
data_neural_hat_final = None

# Inicializa um DataFrame para armazenar as métricas por modelo
metricas_dict = {}

# Carregar o módulo do modelo NHITS dinamicamente
modulo_modelo = importlib.import_module('models.model_NHITS')

# Ajustar para chamar a função correta, no caso do NHITS
funcao_treinar = getattr(modulo_modelo, 'treinar_NHITS')  # Função específica para o NHITS

# Gerar as combinações de parâmetros para o NHITS
param_combinations = gerar_combinacoes_parametros('NHITS')

# Inicializar DataFrame de métricas para armazenar todas as combinações
metricas_df_final = pd.DataFrame(columns=[
    'max_steps', 'learning_rate', 'batch_size', 'activation', 
    'n_blocks', 'mlp_units', 'n_pool_kernel_size', 
    'n_freq_downsample', 'pooling_mode', 'dropout_prob_theta', 
    'scaler_type', 'windows_batch_size', 'step_size', 'random_seed', 'MAE', 'RMSE', 'MAPE'
])

# Iterar sobre as combinações de parâmetros
for params in param_combinations:
    if len(params) == 16:  # Esperando 16 parâmetros agora
        (max_steps, learning_rate, batch_size, activation, n_blocks, 
         mlp_units, n_pool_kernel_size, n_freq_downsample, pooling_mode, 
         dropout_prob_theta, scaler_type, windows_batch_size, step_size, 
         random_seed, num_lr_decays, start_padding_enabled) = params
    else:
        print(f"Número incorreto de parâmetros recebidos: {len(params)}. Esperado: 16")
        continue
    
    col_name = (f'NHITS_steps{max_steps}_lr{learning_rate}_batch{batch_size}_'
                f'activation{activation}_blocks{n_blocks}_'
                f'mlp_units{mlp_units}_pool_kernel{n_pool_kernel_size}_'
                f'freq_downsample{n_freq_downsample}_pooling{pooling_mode}_'
                f'dropout{dropout_prob_theta}_scaler{scaler_type}_'
                f'window_batch{windows_batch_size}_step{step_size}_seed{random_seed}')
    
    print(f'Testando parâmetros: max_steps={max_steps}, learning_rate={learning_rate}, '
          f'batch_size={batch_size}, activation={activation}, n_blocks={n_blocks}, '
          f'mlp_units={mlp_units}, n_pool_kernel_size={n_pool_kernel_size}, '
          f'n_freq_downsample={n_freq_downsample}, pooling_mode={pooling_mode}, '
          f'dropout_prob_theta={dropout_prob_theta}, scaler_type={scaler_type}, '
          f'windows_batch_size={windows_batch_size}, step_size={step_size}, random_seed={random_seed}')
    
    # Treinar o modelo com os parâmetros atuais
    data_neural_hat = funcao_treinar(max_steps, learning_rate, batch_size, activation, 
                                     n_blocks, mlp_units, n_pool_kernel_size, 
                                     n_freq_downsample, pooling_mode, dropout_prob_theta, 
                                     scaler_type, windows_batch_size, step_size, random_seed)

    # Verificar se a previsão foi gerada corretamente
    if data_neural_hat is not None:
        print("Previsão gerada com sucesso.")
        
        # Renomeia a coluna de previsões com o nome do modelo e parâmetros testados
        if 'NHITS' in data_neural_hat.columns:
            data_neural_hat.rename(columns={'NHITS': col_name}, inplace=True)
        else:
            print(f"Erro: A coluna 'NHITS' não foi encontrada nas previsões.")
            continue

        # Merge com os valores reais
        data_neural_hat_final_plot = pd.merge(
            data_neural_hat, 
            data_neural_test[['ds', 'y']],  # Verificar se 'y' está presente
            on='ds', 
            how='left'
        )

        # Verificar se o merge foi bem-sucedido
        print("Colunas após o merge: ", data_neural_hat_final_plot.columns)
        if 'y' not in data_neural_hat_final_plot.columns:
            print(f"Erro: A coluna 'y' não foi encontrada após o merge.")
            continue

        # Verificar se há valores NaN nas colunas antes de calcular as métricas
        if data_neural_hat_final_plot[['y', col_name]].isna().sum().sum() > 0:
            print(f"Existem valores NaN nas colunas 'y' ou '{col_name}'. Removendo esses valores.")
            # Remover as linhas com NaN antes de calcular as métricas
            data_neural_hat_final_plot = data_neural_hat_final_plot.dropna(subset=['y', col_name])

        def root_mean_squared_error(y_true, y_pred):
            return np.sqrt(mean_squared_error(y_true, y_pred))
        # Calcular as métricas para todos os dados (sem agrupar por dia)
        mae = mean_absolute_error(data_neural_hat_final_plot['y'], data_neural_hat_final_plot[col_name])
        rmse = root_mean_squared_error(data_neural_hat_final_plot['y'], data_neural_hat_final_plot[col_name])
        mape = np.mean(np.abs((data_neural_hat_final_plot['y'] - data_neural_hat_final_plot[col_name]) / data_neural_hat_final_plot['y'])) * 100

        # Adicionar as métricas ao DataFrame final
        new_metrics = pd.DataFrame({
            'max_steps': [max_steps],
            'learning_rate': [learning_rate],
            'batch_size': [batch_size],
            'activation': [activation],
            'n_blocks': [n_blocks],
            'mlp_units': [mlp_units],
            'n_pool_kernel_size': [n_pool_kernel_size],
            'n_freq_downsample': [n_freq_downsample],
            'pooling_mode': [pooling_mode],
            'dropout_prob_theta': [dropout_prob_theta],
            'scaler_type': [scaler_type],
            'windows_batch_size': [windows_batch_size],
            'step_size': [step_size],
            'random_seed': [random_seed],
            'MAE': [mae],
            'RMSE': [rmse],
            'MAPE': [mape]
        })

        # Concatenar o DataFrame de novas métricas ao DataFrame final
        metricas_df_final = pd.concat([metricas_df_final, new_metrics], ignore_index=True)

# Após o loop, salvar o resultado final e métricas
if not metricas_df_final.empty:
    # Definir o nome fixo para o arquivo CSV
    csv_file_path = f'{output_dir}/forecast_with_metrics_NHITS_{marca}.csv'
    metricas_df_final.to_csv(csv_file_path, index=False)

    # Exibir a mensagem de sucesso com o nome do arquivo
    print(f"Resultado final salvo com sucesso: {csv_file_path}")
else:
    print("Nenhuma métrica foi calculada.")

# Plotar os valores reais e as previsões dos modelos
if 'data_neural_hat_final_plot' in locals() and 'y' in data_neural_hat_final_plot.columns:
    # Verificar quais colunas estão disponíveis para plotagem
    colunas_para_plotar = ['y', col_name]  # 'y' e a coluna da previsão gerada
    colunas_existentes = [col for col in colunas_para_plotar if col in data_neural_hat_final_plot.columns]
    
    if colunas_existentes:  # Certifique-se de que existem colunas para plotar
        # Plotar os valores reais e as previsões
        data_neural_hat_final_plot.set_index('ds')[colunas_existentes].plot(linewidth=2)

        # Configurações de rótulos e título do gráfico
        plt.ylabel('VLF', fontsize=12)
        plt.xlabel('Date', fontsize=12)
        plt.title(f'Valores Reais vs Previsões ({col_name})', fontsize=14)
        plt.grid()

        # Salvar o gráfico como imagem
        plot_file_path = f'{output_dir}/plot_image_NHITS_{marca}.png'
        plt.savefig(plot_file_path)
        print(f"Gráfico salvo com sucesso: {plot_file_path}")
    else:
        print("Erro: Não há colunas disponíveis para plotar.")
else:
    print("Erro: Não foi possível plotar os dados porque 'data_neural_hat_final_plot' não foi gerado corretamente ou a coluna 'y' está ausente.")

# Exibir o tempo total de execução
end_time = time.time()
execution_time = (end_time - start_time) / 60  # Converte para minutos
print(f"Tempo de execução total: {execution_time:.2f} minutos")

print('main_NHITS.py finalizado')