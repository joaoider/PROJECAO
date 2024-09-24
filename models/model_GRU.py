print('model_GRU.py iniciado')

from imports import *
from base import data_neural, futr_df #, static_df
from configuracoes import horizon, freq, max_steps, learning_rate, batch_size, variaveis_futuras, variaveis_historicas

model = [GRU(
            max_steps=max_steps, #:int=1000
            h = horizon, #:int
            input_size=-1, #:int=-1,
            encoder_n_layers=2, #:int=2
            decoder_layers=2, #:int=2
            encoder_hidden_size=200, #:int=200
            decoder_hidden_size=200, #:int=200
            encoder_activation='tanh', #:str='tanh'
            context_size=10, #:int=10
            loss=MAE(),
            valid_loss=MAE(),
            futr_exog_list = variaveis_futuras,
            hist_exog_list = variaveis_historicas,
            learning_rate = learning_rate, #:float=0.001
            batch_size = batch_size,
            scaler_type='robust', #:str='robust'
            random_seed=1,
        )]

nf = NeuralForecast(models = model, freq = freq)
nf.fit(df = data_neural) #, static_df = static_df)

# Código para mostrar o dataframe com datas e Id esperadas 
#expected_future = nf.make_future_dataframe()
#print('expected_future')
#print(expected_future)

#Código para verificar valores faltantes no meu dataframe futuro
#missing_future = nf.get_missing_future(futr_df = futr_df)
#print('missing_future')
#print(missing_future)

# Duplicando as linhas
#futr_df_complete = pd.concat([futr_df.copy(), futr_df.copy()], ignore_index=True)
# Criando a nova coluna unique_id
#futr_df_complete['unique_id'] = ['Dudalina Masc'] * len(futr_df) + ['Dudalina Fem'] * len(futr_df)

data_neural_hat = nf.predict(futr_df = futr_df) #.reset_index()
#print('data_neural_hat')
#print(data_neural_hat)

print('model_GRU.py finalizado')