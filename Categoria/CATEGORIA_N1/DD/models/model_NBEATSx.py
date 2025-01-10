print('model_NBEATSx.py iniciado')

from configuracoes_modelos.imports import *
from base import data_neural_train, futr_df_test
from DD_configuracoes import horizon, freq

# Função para treinar o modelo NBEATSx
def treinar_NBEATSx(max_steps, learning_rate, batch_size, activation):
    print(f'model_NBEATSx.py iniciado com max_steps={max_steps}, learning_rate={learning_rate}, batch_size={batch_size}, activation={activation}')
    
    # Definir o modelo NBEATSx com os parâmetros variáveis
    model = [NBEATSx(
                max_steps=max_steps,  # Número máximo de iterações
                input_size=5 * horizon,  # Tamanho do input, ajustado para o horizonte
                h=horizon,  # Horizonte de previsão
                n_harmonics=2,  # Número de harmônicos
                n_polynomials=2,  # Número de polinômios
                activation=activation,  # Função de ativação (ReLU, Softplus, etc.)
                learning_rate=learning_rate,  # Taxa de aprendizado
                num_lr_decays=3,  # Número de reduções na taxa de aprendizado
                early_stop_patience_steps=-1,  # Paciência para o early stopping
                val_check_steps=100,  # Intervalo de checagem de validação
                batch_size=batch_size,  # Tamanho do batch
                random_seed=1  # Semente aleatória para reprodutibilidade
            )]

    # Instanciar e treinar o modelo
    nf = NeuralForecast(models = model, freq = freq)
    nf.fit(df = data_neural_train)

    # Gerar previsões
    data_neural_hat = nf.predict(futr_df = futr_df_test)

    print('model_NBEATSx.py finalizado')
    return data_neural_hat