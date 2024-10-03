print('model_GRU.py iniciado')

from itertools import product
from configuracoes.imports import *
from base import data_neural_train, futr_df_test
from configuracoes.configuracoes_BiTCN import horizon, freq, variaveis_futuras, variaveis_historicas

# Função para treinar o modelo BiTCN
def treinar_BiTCN(max_steps, learning_rate, batch_size):
    print(f'model_BiTCN.py iniciado com max_steps={max_steps}, learning_rate={learning_rate}, batch_size={batch_size}')
    
    # Definir o modelo BiTCN com os parâmetros variáveis
    model = [BiTCN(
                max_steps=max_steps,  # Número máximo de iterações
                h=horizon,  # Horizonte de previsão
                input_size=5 * horizon,  # Tamanho do input
                futr_exog_list=variaveis_futuras,  # Variáveis exógenas futuras
                hist_exog_list=variaveis_historicas,  # Variáveis exógenas históricas
                scaler_type='robust',  # Tipo de normalização dos dados
                learning_rate=learning_rate,  # Taxa de aprendizado
                batch_size=batch_size,  # Tamanho do batch
                loss=MAE(),  # Função de perda
                valid_loss=MAE()  # Função de perda para validação
            )]

    # Instanciar e treinar o modelo
    nf = NeuralForecast(models=model, freq=freq)
    nf.fit(df=data_neural_train)

    # Gerar previsões
    data_neural_hat = nf.predict(futr_df=futr_df_test)

    print('model_BiTCN.py finalizado')
    return data_neural_hat