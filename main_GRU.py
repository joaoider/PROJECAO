import time
# Marcação de início de execução
start_time = time.time()

# MÓDULO PRINCIPAL
print('main_GRU.py iniciado')

# Importar módulos e dataframes necessários
from configuracoes.imports import *
from configuracoes.configuracoes_GRU import marca, gerar_combinacoes_parametros
from base import data_neural_train, data_neural_test  # Certifique-se de que 'data_neural_test' tenha a coluna 'y'

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

# Inicializa um DataFrame para armazenar as métricas por modelo
metricas_dict = {}

# Carregar o módulo do modelo GRU dinamicamente
modulo_modelo = importlib.import_module('models.model_GRU')

# Ajustar para chamar a função correta, no caso do GRU
funcao_treinar = getattr(modulo_modelo, 'treinar_GRU')  # Função específica para o GRU

# Gerar as combinações de parâmetros para o GRU
param_combinations = gerar_combinacoes_parametros('GRU')

# Inicializar DataFrame de métricas para armazenar todas as combinações
metricas_df_final = pd.DataFrame(columns=[
    'max_steps', 'learning_rate', 'batch_size', 
    'encoder_hidden_size', 'decoder_hidden_size', 
    'encoder_n_layers', 'decoder_layers', 'context_size',
    'encoder_activation', 'encoder_bias', 'encoder_dropout', 
    'num_lr_decays', 'early_stop_patience_steps', 'val_check_steps',
    'scaler_type', 'random_seed', 'MAE', 'MSE', 'RMSE', 'MAPE'
])

# Iterar sobre as combinações de parâmetros
for params in param_combinations:
    (max_steps, learning_rate, batch_size, encoder_hidden_size, decoder_hidden_size, 
     encoder_n_layers, decoder_layers, context_size, encoder_activation, 
     encoder_bias, encoder_dropout, num_lr_decays, early_stop_patience_steps, 
     val_check_steps, scaler_type, random_seed, num_workers_loader, 
     drop_last_loader, optimizer, lr_scheduler) = params

    col_name = (f'GRU_steps{max_steps}_lr{learning_rate}_batch{batch_size}_'
                f'encoder{encoder_hidden_size}_decoder{decoder_hidden_size}_'
                f'enc_layers{encoder_n_layers}_dec_layers{decoder_layers}_context{context_size}_'
                f'activation{encoder_activation}_bias{encoder_bias}_dropout{encoder_dropout}_'
                f'lr_decays{num_lr_decays}_early_stop{early_stop_patience_steps}_'
                f'val_check{val_check_steps}_scaler{scaler_type}_seed{random_seed}')

    print(f'Testando parâmetros: max_steps={max_steps}, learning_rate={learning_rate}, '
          f'batch_size={batch_size}, encoder_hidden_size={encoder_hidden_size}, '
          f'decoder_hidden_size={decoder_hidden_size}, encoder_n_layers={encoder_n_layers}, '
          f'decoder_layers={decoder_layers}, context_size={context_size}, encoder_activation={encoder_activation}, '
          f'encoder_bias={encoder_bias}, encoder_dropout={encoder_dropout}, num_lr_decays={num_lr_decays}, '
          f'early_stop_patience_steps={early_stop_patience_steps}, val_check_steps={val_check_steps}, '
          f'scaler_type={scaler_type}, random_seed={random_seed}, num_workers_loader={num_workers_loader}, '
          f'drop_last_loader={drop_last_loader}, optimizer={optimizer}, lr_scheduler={lr_scheduler}')
    
    # Treinar o modelo com os parâmetros atuais
    data_neural_hat = funcao_treinar(max_steps, learning_rate, batch_size, 
                                     encoder_hidden_size, decoder_hidden_size, 
                                     encoder_n_layers, decoder_layers, context_size, 
                                     encoder_activation, encoder_bias, encoder_dropout, 
                                     num_lr_decays, early_stop_patience_steps, 
                                     val_check_steps, scaler_type, random_seed, 
                                     num_workers_loader, drop_last_loader, 
                                     optimizer, lr_scheduler)

    # Verificar se a previsão foi gerada corretamente
    if data_neural_hat is not None:
        print("Previsão gerada com sucesso.")
        
        # Renomeia a coluna de previsões com o nome do modelo e parâmetros testados
        data_neural_hat.rename(columns={'GRU': col_name}, inplace=True)

        # Verificar se a coluna 'y' existe no data_neural_test
        if 'y' not in data_neural_test.columns:
            print("Erro: A coluna 'y' não está presente no conjunto de teste (data_neural_test). Verifique se os dados estão corretos.")
            break  # Interrompe a execução se 'y' não estiver presente
        else:
            print("'y' encontrado no conjunto de teste.")

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

        # Calcular as métricas para todos os dados (sem agrupar por dia)
        mae = mean_absolute_error(data_neural_hat_final_plot['y'], data_neural_hat_final_plot[col_name])
        mse = mean_squared_error(data_neural_hat_final_plot['y'], data_neural_hat_final_plot[col_name])
        rmse = np.sqrt(mse)
        mape = np.mean(np.abs((data_neural_hat_final_plot['y'] - data_neural_hat_final_plot[col_name]) / data_neural_hat_final_plot['y'])) * 100

        # Adicionar as métricas ao DataFrame final
        new_metrics = pd.DataFrame({
            'max_steps': [max_steps],
            'learning_rate': [learning_rate],
            'batch_size': [batch_size],
            'encoder_hidden_size': [encoder_hidden_size],
            'decoder_hidden_size': [decoder_hidden_size],
            'encoder_n_layers': [encoder_n_layers],
            'decoder_layers': [decoder_layers],
            'context_size': [context_size],
            'encoder_activation': [encoder_activation],
            'encoder_bias': [encoder_bias],
            'encoder_dropout': [encoder_dropout],
            'num_lr_decays': [num_lr_decays],
            'early_stop_patience_steps': [early_stop_patience_steps],
            'val_check_steps': [val_check_steps],
            'scaler_type': [scaler_type],
            'random_seed': [random_seed],
            'MAE': [mae],
            'MSE': [mse],
            'RMSE': [rmse],
            'MAPE': [mape]
        })

        # Concatenar o DataFrame de novas métricas ao DataFrame final
        metricas_df_final = pd.concat([metricas_df_final, new_metrics], ignore_index=True)

# Após o loop, salvar o resultado final e métricas
if not metricas_df_final.empty:
    # Gerar o nome do arquivo CSV com base no horário atual
    horario_csv_salvo_gru = datetime.now().strftime('%H-%M-%S')
    csv_file_path = f'{output_dir}/forecast_with_metrics_GRU_{horario_csv_salvo_gru}.csv'
    metricas_df_final.to_csv(csv_file_path, index=False)

    # Exibir a mensagem de sucesso com o nome do arquivo e horário
    print(f"Resultado final salvo com sucesso: {csv_file_path} às {horario_csv_salvo_gru}")
    
    # Salvar o nome do arquivo CSV em um arquivo texto para ser utilizado posteriormente
    with open(f'{output_dir}/nome_arquivo_csv_gru.txt', 'w') as f:
        f.write(csv_file_path)  # Escrever o caminho completo do arquivo CSV
    print(f"Nome do arquivo CSV salvo com sucesso em {output_dir}/nome_arquivo_csv_gru.txt")
else:
    print("Nenhuma métrica foi calculada.")

# Plotar os valores reais e as previsões dos modelos
if 'y' in data_neural_hat_final_plot.columns:
    # Verificar quais colunas estão disponíveis para plotagem
    colunas_para_plotar = ['y', col_name]  # 'y' e a coluna da previsão gerada
    colunas_existentes = [col for col in colunas_para_plotar if col in data_neural_hat_final_plot.columns]
    
    # Plotar os valores reais e as previsões
    data_neural_hat_final_plot.set_index('ds')[colunas_existentes].plot(linewidth=2)

    # Configurações de rótulos e título do gráfico
    plt.ylabel('VLF', fontsize=12)
    plt.xlabel('Date', fontsize=12)
    plt.title(f'Valores Reais vs Previsões ({col_name})', fontsize=14)
    plt.grid()

    # Salvar o gráfico como imagem
    plot_file_path = f'{output_dir}/plot_image_GRU_{horario_atual}.png'
    plt.savefig(plot_file_path)
    print(f"Gráfico salvo com sucesso: {plot_file_path}")
else:
    print("Erro: Não foi possível plotar os dados porque a coluna 'y' não está presente.")

# Exibir o tempo total de execução
end_time = time.time()
execution_time = end_time - start_time
print(f"Tempo de execução total: {execution_time:.2f} segundos")

print('main_GRU.py finalizado')