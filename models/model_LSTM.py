print('model_LSTM.py iniciado')

# Importações
from imports import *
from base import data_neural_dfs, futr_df_dfs  # DataFrames armazenados para cada marca
from configuracoes import horizon, freq, max_steps, learning_rate, batch_size, variaveis_futuras, variaveis_historicas, encoder_hidden_size, decoder_hidden_size, encoder_n_layers, decoder_layers, context_size

# Dicionário para armazenar as previsões
data_neural_hat_dfs = {}

# Iterar sobre as marcas
for m in data_neural_dfs:
    print(f"Rodando o modelo para a marca: {m}")
    
    # Pegar o DataFrame correspondente da marca
    data_neural = data_neural_dfs[m]
    futr_df = futr_df_dfs.get(f'futr_df_{m}')
    
    # Verificar se os DataFrames existem
    if data_neural is not None and futr_df is not None:
        
        # Definir o modelo LSTM
        model = [LSTM(
            max_steps = max_steps, 
            h = horizon, 
            input_size = -1, 
            batch_size=batch_size, 
            encoder_hidden_size = encoder_hidden_size, 
            encoder_n_layers = encoder_n_layers, 
            decoder_hidden_size = decoder_hidden_size, 
            decoder_layers = decoder_layers, 
            context_size = context_size, 
            learning_rate = learning_rate, 
            futr_exog_list = variaveis_futuras,
            hist_exog_list = variaveis_historicas,
            loss = MAE(),
            valid_loss = MAE(),
            scaler_type = 'robust'
        )]
        
        # Instanciar e treinar o modelo
        nf = NeuralForecast(models=model, freq=freq)
        nf.fit(df=data_neural)
        
        # Gerar previsões
        data_neural_hat = nf.predict(futr_df=futr_df)
        
        # Armazenar o DataFrame de previsão no dicionário
        data_neural_hat_dfs[f'data_neural_hat_{m}'] = data_neural_hat
        
        # Mostrar as primeiras linhas do DataFrame de previsão
        print(f"\nDataFrame de previsão para {m}:")
        print(data_neural_hat.head())

# Agora os DataFrames de previsão estão armazenados no dicionário `data_neural_hat_dfs`

print('model_LSTM.py finalizado')