import time
# Marcação de início de execução
start_time = time.time()

# MÓDULO PRINCIPAL
print('main_GRU_categoria_final.py iniciado')

# Importar módulos e dataframes necessários
from configuracoes_modelos.imports import *
from BB_configuracoes import marca, horizon
from configuracoes_modelos.configuracoes_GRU import gerar_combinacoes_parametros
from BB_base_categoria import data_neural, futr_df, unique_ids  # Certifique-se que 'unique_ids' está no 'base_categoria'

print('Iniciando previsões com GRU')
print('###############################')

# Criar a pasta com a data do dia, se não existir
data_atual = datetime.now().strftime('%Y-%m-%d')
output_dir = 'outputs'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Carregar o módulo do modelo GRU dinamicamente
modulo_modelo = importlib.import_module('models.model_GRU_categoria_final')

# Ajustar para chamar a função correta, no caso do GRU
funcao_treinar = getattr(modulo_modelo, 'treinar_GRU')  # Função específica para o GRU

# Gerar as combinações de parâmetros para o GRU
param_combinations = gerar_combinacoes_parametros('GRU')



# Iterar sobre as combinações de parâmetros (apenas rodar o modelo)
for params in param_combinations:
    (max_steps, learning_rate, batch_size, encoder_hidden_size, decoder_hidden_size, 
     encoder_n_layers, decoder_layers, context_size, encoder_activation, 
     encoder_bias, encoder_dropout, num_lr_decays, early_stop_patience_steps, 
     val_check_steps, scaler_type, random_seed, loss) = params

    print(f'Testando parâmetros: max_steps={max_steps}, learning_rate={learning_rate}, '
          f'batch_size={batch_size}, encoder_hidden_size={encoder_hidden_size}, '
          f'decoder_hidden_size={decoder_hidden_size}, encoder_n_layers={encoder_n_layers}, '
          f'decoder_layers={decoder_layers}, context_size={context_size}, encoder_activation={encoder_activation}, '
          f'encoder_bias={encoder_bias}, encoder_dropout={encoder_dropout}, num_lr_decays={num_lr_decays}, '
          f'early_stop_patience_steps={early_stop_patience_steps}, val_check_steps={val_check_steps}, '
          f'scaler_type={scaler_type}, random_seed={random_seed}, loss={loss}')

    # Treinar o modelo com os parâmetros atuais
    data_neural_hat = funcao_treinar(max_steps, learning_rate, batch_size, 
                                     encoder_hidden_size, decoder_hidden_size, 
                                     encoder_n_layers, decoder_layers, context_size, 
                                     encoder_activation, encoder_bias, encoder_dropout, 
                                     num_lr_decays, early_stop_patience_steps, 
                                     val_check_steps, scaler_type, random_seed, loss)

    # Verificar se a previsão foi gerada corretamente
    if data_neural_hat is not None:
        print("Previsão gerada com sucesso.")
        
        # Adicionar a coluna 'unique_id' dividindo em blocos de 365 valores
        num_unique_ids = len(unique_ids)
        total_rows = len(data_neural_hat)
        rows_per_id = horizon
        
        # Criando a lista de unique_ids repetida em blocos de 365
        ids_repeated = []
        for i in range(num_unique_ids):
            ids_repeated.extend([unique_ids[i]] * rows_per_id)

        # Ajustando o tamanho da lista caso tenha mais ou menos que o esperado
        ids_repeated = ids_repeated[:total_rows]  # Caso o total de linhas seja menor que o necessário
        
        # Adiciona a coluna 'unique_id'
        data_neural_hat['unique_id'] = ids_repeated

        # Salvar o DataFrame gerado diretamente em um arquivo CSV
        csv_file_path = os.path.join(output_dir, f'forecast_GRU_{marca}_categoria_malha_final.csv')
        data_neural_hat.to_csv(csv_file_path, index=False)
        print(f"Previsões salvas com sucesso em: {csv_file_path}")

        # -------------------- Parte 2: Criando o novo DataFrame agrupado --------------------

        data_neural_hat_mes = data_neural_hat.copy()

        # Converter a coluna 'ds' para o formato datetime
        data_neural_hat_mes['ds'] = pd.to_datetime(data_neural_hat_mes['ds'])

        # Criar uma nova coluna 'mes_ano' para agrupar por mês/ano
        data_neural_hat_mes['mes_ano'] = data_neural_hat_mes['ds'].dt.to_period('M')

        # Garantir que 'unique_id' não seja um índice, apenas uma coluna
        if 'unique_id' in data_neural_hat_mes.index.names:
            data_neural_hat_mes = data_neural_hat_mes.reset_index(drop=True)

        # Agrupar os dados por 'unique_id' e 'mes_ano' e somar os valores de 'GRU'
        df_grouped = data_neural_hat_mes.groupby(['unique_id', 'mes_ano'])['GRU'].sum().unstack()

        # Adicionar a linha 'Total' com a soma dos valores de cada coluna
        df_grouped.loc['Total'] = df_grouped.sum()

        # Salvar o novo DataFrame agrupado com a linha de soma
        csv_grouped_file_path = os.path.join(output_dir, f'forecast_grouped_GRU_{marca}_categoria_malha_final.csv')
        df_grouped.to_csv(csv_grouped_file_path)
        print(f"DataFrame agrupado por mês/ano salvo com sucesso em: {csv_grouped_file_path}")

        # Supondo que df_grouped seja o DataFrame original
        # Resetar o índice para transformar 'unique_id' em uma coluna
        transposed_df = df_grouped.reset_index()

        # Transpor o DataFrame para ter as datas como primeira coluna e unique_ids como colunas
        transposed_df = transposed_df.set_index('unique_id').T.reset_index()

        # Renomear a coluna 'index' para 'Data'
        transposed_df.rename(columns={'index': 'Data'}, inplace=True)

        # Salvar o novo DataFrame transformado
        csv_transposed_file_path = os.path.join(output_dir, f'forecast_transposed_GRU_{marca}_categoria_malha_final.csv')
        transposed_df.to_csv(csv_transposed_file_path, index=False)
        print(f"DataFrame transposto salvo com sucesso em: {csv_transposed_file_path}")

# Exibir o tempo total de execução
end_time = time.time()
execution_time = end_time - start_time
print(f"Tempo de execução total: {execution_time:.2f} segundos")

print('main_GRU_categoria_final.py finalizado')