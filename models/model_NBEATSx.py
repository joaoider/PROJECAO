print('model_NBEATSx.py iniciado')

from imports import *
from base import data_neural, futr_df #, static_df
from configuracoes import horizon, freq, max_steps, activation, learning_rate, batch_size

model = [NBEATSx(
            max_steps=max_steps, #:int=1000
            input_size=5*horizon,
            h=horizon,
            n_harmonics=2,
            n_polynomials=2,
            activation=activation,
            learning_rate = learning_rate, #:float=0.001   
            num_lr_decays=3, #:int=3
            early_stop_patience_steps=-1, #:int=-1
            val_check_steps=100, #:int=100
            batch_size = batch_size,
            random_seed=1, #:int=1
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

print('model_NBEATSx.py finalizado')