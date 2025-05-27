import time
import sys
import os

try:
    # Marcação de início de execução
    start_time = time.time()

    # MÓDULO PRINCIPAL
    print('main_LSTM_final.py iniciado')

    # Definir o diretório onde os parâmetros estão salvos
    output_dir = 'outputs'
    json_parametros_path = f'{output_dir}/parametros_melhor_modelo_LSTM.json'

    print('Marca: ', marca)
    print('###############################')

    # Verificar se o arquivo JSON de parâmetros existe
    if not os.path.exists(json_parametros_path):
        print(f"Arquivo de parâmetros {json_parametros_path} não encontrado. Encerrando execução.")
        sys.exit(0)

    import json
    import importlib
    import matplotlib.pyplot as plt
    import pandas as pd
    from configuracoes_modelos.imports import *
    from JJ_configuracoes import marca
    from JJ_base import data_neural, futr_df

    # Carregar os parâmetros do modelo vencedor a partir do JSON
    with open(json_parametros_path, 'r') as f:
        parametros = json.load(f)

    # Exibir os parâmetros carregados
    print(f"Parâmetros carregados: {parametros}")

    # Atribuir os parâmetros às variáveis correspondentes
    max_steps = parametros['max_steps']
    learning_rate = parametros['learning_rate']
    batch_size = parametros['batch_size']
    encoder_hidden_size = parametros['encoder_hidden_size']
    decoder_hidden_size = parametros['decoder_hidden_size']
    encoder_n_layers = parametros['encoder_n_layers']
    decoder_layers = parametros['decoder_layers']
    context_size = parametros['context_size']
    encoder_bias = parametros['encoder_bias']
    encoder_dropout = parametros['encoder_dropout']
    num_lr_decays = parametros['num_lr_decays']
    early_stop_patience_steps = parametros['early_stop_patience_steps']
    val_check_steps = parametros['val_check_steps']
    random_seed = parametros['random_seed']
    drop_last_loader = parametros['drop_last_loader']

    # Exibir os parâmetros selecionados
    print(f'Parâmetros selecionados: max_steps={max_steps}, learning_rate={learning_rate}, '
      f'batch_size={batch_size}, encoder_hidden_size={encoder_hidden_size}, '
      f'decoder_hidden_size={decoder_hidden_size}, encoder_n_layers={encoder_n_layers}, '
      f'decoder_layers={decoder_layers}, context_size={context_size}, '
      f'encoder_bias={encoder_bias}, encoder_dropout={encoder_dropout}, '
      f'num_lr_decays={num_lr_decays}, early_stop_patience_steps={early_stop_patience_steps}, '
      f'val_check_steps={val_check_steps}, random_seed={random_seed}, '
      f'drop_last_loader={drop_last_loader}')

    # Inicializa a variável para armazenar o dataframe final de previsões
    data_neural_hat_final = None

    # Carregar o módulo do modelo LSTM dinamicamente
    modulo_modelo = importlib.import_module('models.model_LSTM_final')

    # Ajustar para chamar a função correta, no caso do LSTM
    funcao_treinar = getattr(modulo_modelo, 'treinar_LSTM')  # Função específica para o LSTM

    # Nome para a coluna de previsão (ajustado para usar as variáveis, não args)
    col_name = (f'LSTM_steps{max_steps}_lr{learning_rate}_batch{batch_size}_'
            f'encoder{encoder_hidden_size}_decoder{decoder_hidden_size}_'
            f'enc_layers{encoder_n_layers}_dec_layers{decoder_layers}_'
            f'context{context_size}_bias{encoder_bias}_dropout{encoder_dropout}')

    # Treinar o modelo com os parâmetros carregados
    data_neural_hat = funcao_treinar(max_steps, learning_rate, batch_size,
                                 encoder_hidden_size, decoder_hidden_size,
                                 encoder_n_layers, decoder_layers, context_size,
                                 encoder_bias, encoder_dropout, num_lr_decays,
                                 early_stop_patience_steps, val_check_steps,
                                 random_seed, drop_last_loader)

    # Verificar se a previsão foi gerada corretamente
    if data_neural_hat is not None:
        print("Previsão gerada com sucesso.")
        
        # Renomeia a coluna de previsões com o nome do modelo e parâmetros testados
        data_neural_hat.rename(columns={'LSTM': col_name}, inplace=True)

        # Salvar o resultado final em CSV
        csv_file_path = f'{output_dir}/melhor_modelo_forecast_LSTM_final_{marca}.csv'
        data_neural_hat.to_csv(csv_file_path, index=False)
        print(f"Previsão salva com sucesso: {csv_file_path}")

        # Agora vamos fazer o groupby por mês e somar os valores
        data_neural_hat['ds'] = pd.to_datetime(data_neural_hat['ds'])  # Converter a coluna de datas para datetime
        data_neural_hat['month'] = data_neural_hat['ds'].dt.to_period('M')  # Extrair o mês
        previsao_mensal = data_neural_hat.groupby('month')[col_name].sum().reset_index()

        # Salvar o resultado mensal em um CSV
        csv_mensal_path = f'{output_dir}/melhor_modelo_forecast_LSTM_mensal_{marca}.csv'
        previsao_mensal.to_csv(csv_mensal_path, index=False)
        print(f"Previsão mensal salva com sucesso: {csv_mensal_path}")

        # Plotar as previsões
        data_neural_hat.set_index('ds')[col_name].plot(linewidth=2)
        plt.ylabel('VLF', fontsize=12)
        plt.xlabel('Date', fontsize=12)
        plt.title(f'Previsões LSTM ({col_name})', fontsize=14)
        plt.grid()

        # Salvar o gráfico como imagem
        plot_file_path = f'{output_dir}/melhor_modelo_plot_image_LSTM_final_{marca}.png'
        plt.savefig(plot_file_path)
        print(f"Gráfico salvo com sucesso: {plot_file_path}")
    else:
        print("Erro: Não foi possível gerar a previsão.")

    # Exibir o tempo total de execução
    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Tempo de execução total: {execution_time:.2f} segundos")
    print('main_LSTM_final.py finalizado')

except SystemExit as e:
    if e.code == 0:
        print("Execução encerrada normalmente.")
    else:
        raise  # Re-lança se for outro tipo de saída inesperada
