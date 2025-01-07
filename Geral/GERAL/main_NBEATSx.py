import time
# Marcação de início de execução
start_time = time.time()

# MÓDULO PRINCIPAL
print('main_NBEATSx.py iniciado')

# Importar módulos e dataframes necessários
from configuracoes_modelos.imports import *
from configuracoes import marca
from configuracoes_modelos.configuracoes_NBEATSx import gerar_combinacoes_parametros
from base import data_neural_train, data_neural_test 

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

# Carregar o módulo do modelo NBEATSx dinamicamente
modulo_modelo = importlib.import_module('models.model_NBEATSx')

# Ajustar para chamar a função correta, no caso do NBEATSx
funcao_treinar = getattr(modulo_modelo, 'treinar_NBEATSx')  # Função específica para o NBEATSx

# Gerar as combinações de parâmetros para o NBEATSx
param_combinations = gerar_combinacoes_parametros('NBEATSx')

# Inicializar DataFrame de métricas para armazenar todas as combinações
metricas_df_final = pd.DataFrame(columns=['max_steps', 'learning_rate', 'batch_size', 'activation', 'MAE', 'RMSE'])

# Iterar sobre as combinações de parâmetros
for params in param_combinations:
    max_steps, learning_rate, batch_size, activation = params
    col_name = f'NBEATSx_steps{max_steps}_lr{learning_rate}_batch{batch_size}_activation{activation}'
    print(f'Testando parâmetros: max_steps={max_steps}, learning_rate={learning_rate}, batch_size={batch_size}, activation={activation}')
    
    # Treinar o modelo com os parâmetros atuais
    data_neural_hat = funcao_treinar(max_steps, learning_rate, batch_size, activation)

    # Verificar se a previsão foi gerada corretamente
    if data_neural_hat is not None:
        print("Previsão gerada com sucesso.")
        
        # Renomeia a coluna de previsões com o nome do modelo e parâmetros testados
        data_neural_hat.rename(columns={'NBEATSx': col_name}, inplace=True)

        # Verificar se a coluna 'y' existe no data_neural_test
        if 'y' not in data_neural_test.columns:
            print("Erro: A coluna 'y' não está presente no conjunto de teste (data_neural_test). Verifique se os dados estão corretos.")
            break  # Interrompe a execução se 'y' não estiver presente
        else:
            print("'y' encontrado no conjunto de teste.")

        # Merge com os valores reais
        # Garantir que ambas as colunas 'ds' sejam comparáveis
        data_neural_hat['ds'] = pd.to_datetime(data_neural_hat['ds'])
        data_neural_test['ds'] = pd.to_datetime(data_neural_test['ds'])

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
            'MAE': [mae],
            'RMSE': [rmse],
            'MAPE': [mape]
        })

        # Concatenar o DataFrame de novas métricas ao DataFrame final
        metricas_df_final = pd.concat([metricas_df_final, new_metrics], ignore_index=True)

# Após o loop, salvar o resultado final e métricas
if not metricas_df_final.empty:
    csv_file_path = f'{output_dir}/forecast_with_metrics_NBEATSx_{marca}.csv'
    metricas_df_final.to_csv(csv_file_path, index=False)
    print(f"Resultado final salvo com sucesso: {csv_file_path}")
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
    plot_file_path = f'{output_dir}/plot_image_NBEATSx_{marca}.png'
    plt.savefig(plot_file_path)
    print(f"Gráfico salvo com sucesso: {plot_file_path}")
else:
    print("Erro: Não foi possível plotar os dados porque a coluna 'y' não está presente.")

# Exibir o tempo total de execução
end_time = time.time()
execution_time = end_time - start_time
print(f"Tempo de execução total: {execution_time:.2f} segundos")

print('main_NBEATSx.py finalizado')