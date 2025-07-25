print('model_GRU_final.py iniciado')

from configs.configuracoes_GRU import *
from base import data_neural, futr_df
from funcoes import get_output_dir
# from configuracoes_modelos.imports import *

# Função para treinar o modelo GRU
def treinar_GRU(max_steps, learning_rate, batch_size, encoder_hidden_size, decoder_hidden_size, 
                encoder_n_layers, decoder_layers, context_size, encoder_activation, 
                encoder_bias, encoder_dropout, num_lr_decays, early_stop_patience_steps, 
                val_check_steps, scaler_type, random_seed):
    
    print(f'treinar_GRU iniciado com max_steps={max_steps}, learning_rate={learning_rate}, batch_size={batch_size}, '
          f'encoder_hidden_size={encoder_hidden_size}, decoder_hidden_size={decoder_hidden_size}, '
          f'encoder_n_layers={encoder_n_layers}, decoder_layers={decoder_layers}, context_size={context_size}, '
          f'encoder_activation={encoder_activation}, encoder_bias={encoder_bias}, encoder_dropout={encoder_dropout}, '
          f'num_lr_decays={num_lr_decays}, early_stop_patience_steps={early_stop_patience_steps}, '
          f'val_check_steps={val_check_steps}, scaler_type={scaler_type}, random_seed={random_seed} ')
    
    # Definir o modelo GRU com os parâmetros variáveis
    model = [GRU(
                max_steps=max_steps,  # Número máximo de iterações
                h=horizon,  # Horizonte de previsão
                input_size=-1,  # Tamanho do input
                encoder_n_layers=encoder_n_layers,  # Camadas do codificador
                decoder_layers=decoder_layers,  # Camadas do decodificador
                encoder_hidden_size=encoder_hidden_size,  # Tamanho da camada oculta do codificador
                decoder_hidden_size=decoder_hidden_size,  # Tamanho da camada oculta do decodificador
                encoder_activation=encoder_activation,  # Função de ativação do codificador
                encoder_bias=encoder_bias,  # Bias no encoder
                encoder_dropout=encoder_dropout,  # Dropout no encoder
                context_size=context_size,  # Tamanho do contexto
                loss=MAE(),  # Função de perda
                valid_loss=MAE(),  # Função de perda para validação
                futr_exog_list=variaveis_futuras,  # Variáveis exógenas futuras
                hist_exog_list=variaveis_historicas,  # Variáveis exógenas históricas
                learning_rate=learning_rate,  # Taxa de aprendizado
                batch_size=batch_size,  # Tamanho do batch
                num_lr_decays=num_lr_decays,  # Número de decaimentos da taxa de aprendizado
                early_stop_patience_steps=early_stop_patience_steps,  # Paciência para early stopping
                val_check_steps=val_check_steps,  # Verificação de validação a cada N passos
                scaler_type=scaler_type,  # Tipo de normalização dos dados
                random_seed=random_seed  # Semente aleatória
            )]

    # Instanciar e treinar o modelo
    nf = NeuralForecast(models = model, freq = freq)
    nf.fit(df = data_neural)

    # Gerar previsões
    data_neural_hat = nf.predict(futr_df = futr_df)

    print('treinar_GRU finalizado')
    return data_neural_hat