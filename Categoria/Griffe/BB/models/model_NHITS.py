print('model_NHITS.py iniciado')

from configuracoes_modelos.imports import *
from BB_base_categoria import data_neural_train, futr_df_test
from BB_configuracoes import horizon, freq, variaveis_futuras, variaveis_historicas

# Função para treinar o modelo NHITS
def treinar_NHITS(max_steps, learning_rate, batch_size, activation, n_blocks, mlp_units, 
                  n_pool_kernel_size, n_freq_downsample, pooling_mode, dropout_prob_theta, 
                  scaler_type, windows_batch_size, step_size, random_seed):
    
    print(f'model_NHITS.py iniciado com max_steps={max_steps}, learning_rate={learning_rate}, '
          f'batch_size={batch_size}, activation={activation}, n_blocks={n_blocks}, '
          f'mlp_units={mlp_units}, n_pool_kernel_size={n_pool_kernel_size}, '
          f'n_freq_downsample={n_freq_downsample}, pooling_mode={pooling_mode}, '
          f'dropout_prob_theta={dropout_prob_theta}, scaler_type={scaler_type}, '
          f'windows_batch_size={windows_batch_size}, step_size={step_size}, random_seed={random_seed}')
    
    # Definir o modelo NHITS com os parâmetros variáveis
    model = [NHITS(
                max_steps=max_steps, 
                h=horizon,
                input_size=5 * horizon,  # Pode ajustar conforme necessário
                futr_exog_list=variaveis_futuras,
                hist_exog_list=variaveis_historicas,
                n_blocks=n_blocks, 
                mlp_units=mlp_units, 
                n_pool_kernel_size=n_pool_kernel_size, 
                n_freq_downsample=n_freq_downsample, 
                pooling_mode=pooling_mode,
                dropout_prob_theta=dropout_prob_theta,
                scaler_type=scaler_type,
                learning_rate=learning_rate, 
                batch_size=batch_size, 
                windows_batch_size=windows_batch_size,
                step_size=step_size,
                random_seed=random_seed,
                loss=MAE(),
                valid_loss=MAE(),
                activation=activation
            )]

    # Instanciar e treinar o modelo
    nf = NeuralForecast(models=model, freq=freq)
    nf.fit(df=data_neural_train)

    # Gerar previsões
    data_neural_hat = nf.predict(futr_df=futr_df_test)

    print('model_NHITS.py finalizado')
    return data_neural_hat