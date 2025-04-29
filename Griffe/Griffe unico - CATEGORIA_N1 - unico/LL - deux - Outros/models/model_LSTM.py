print('model_LSTM.py iniciado')

from configuracoes_modelos.imports import *
from LL_base import data_neural_train, futr_df_test
from LL_configuracoes import horizon, freq, variaveis_futuras, variaveis_historicas

def treinar_LSTM(max_steps, learning_rate, batch_size, encoder_hidden_size, decoder_hidden_size, encoder_n_layers, decoder_layers, context_size, encoder_bias, encoder_dropout, num_lr_decays, early_stop_patience_steps, val_check_steps, random_seed, num_workers_loader, drop_last_loader):
    print(f'treinar_LSTM iniciado com max_steps={max_steps}, learning_rate={learning_rate}, batch_size={batch_size}, '
          f'encoder_hidden_size={encoder_hidden_size}, decoder_hidden_size={decoder_hidden_size}, '
          f'encoder_n_layers={encoder_n_layers}, decoder_layers={decoder_layers}, context_size={context_size}, '
          f'encoder_bias={encoder_bias}, encoder_dropout={encoder_dropout}, num_lr_decays={num_lr_decays}, '
          f'early_stop_patience_steps={early_stop_patience_steps}, val_check_steps={val_check_steps}, '
          f'random_seed={random_seed}, num_workers_loader={num_workers_loader}, drop_last_loader={drop_last_loader}')
    
    # Definir o modelo LSTM com os parâmetros variáveis
    model = [LSTM(
                max_steps=max_steps,  
                h=horizon,  
                input_size=-1,  
                batch_size=batch_size, 
                encoder_hidden_size=encoder_hidden_size, 
                encoder_n_layers=encoder_n_layers, 
                decoder_hidden_size=decoder_hidden_size, 
                decoder_layers=decoder_layers, 
                context_size=context_size,  
                learning_rate=learning_rate, 
                encoder_bias=encoder_bias,  # Novo parâmetro adicionado
                encoder_dropout=encoder_dropout,  # Novo parâmetro adicionado
                num_lr_decays=num_lr_decays,  # Novo parâmetro adicionado
                early_stop_patience_steps=early_stop_patience_steps,  # Novo parâmetro adicionado
                val_check_steps=val_check_steps,  # Novo parâmetro adicionado
                futr_exog_list=variaveis_futuras,
                hist_exog_list=variaveis_historicas,
                scaler_type='robust',
                random_seed=random_seed,  # Novo parâmetro adicionado
                num_workers_loader=num_workers_loader,  # Novo parâmetro adicionado
                drop_last_loader=drop_last_loader  # Novo parâmetro adicionado
            )]

    # Instanciar e treinar o modelo
    nf = NeuralForecast(models = model, freq = freq)
    nf.fit(df = data_neural_train)

    # Gerar previsões
    data_neural_hat = nf.predict(futr_df = futr_df_test)

    print('treinar_LSTM finalizado')
    return data_neural_hat