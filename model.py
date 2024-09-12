from imports import *
from base import data_neural, futr_df #, static_df
from configuracoes import horizon, freq

max_steps=1

model = [LSTM(
            max_steps=max_steps, #padrão = 1000
            h=horizon, 
            input_size=-1, #padrão = -1, base toda
            batch_size=32, #padrão = 32
            encoder_hidden_size=200, #padrão = 200
            encoder_n_layers=2, #padrão = 2
            decoder_hidden_size=200, #padrão = 200
            decoder_layers=2, #padrão = 2
            context_size=10, #padrão = 10
              #float=1e-3, Learning rate between (0, 1).
            learning_rate=0.001, #quanto menor, melhor # padrão = 0.001
              #str list, future exogenous columns.
            futr_exog_list = ['dayofweek', 'monthofyear', 'dia_das_maes', 'dia_dos_pais', 'dia_dos_namorados', 'halloween', 'black_friday', 'natal', 'copa_do_mundo', 'eleicoes', 'dia_do_trabalhador', 'dia_de_finados', 'confraternizacao_universal', 'independencia_do_brasil', 'nossa_senhora_aparecida', 'proclamacao_da_republica', 'sexta_feira_santa', 'pascoa', 'carnaval'],
              #str list, historic exogenous columns.
            hist_exog_list = ['QLF'],
              #PyTorch module, instantiated train loss class from losses collection.   
            loss=MAE(),
              #PyTorch module=loss, instantiated valid loss class from losses collection.
            valid_loss=MAE(),
              #str=‘robust’, type of scaler for temporal inputs normalization see temporal scalers.                       
            scaler_type='robust' #sugerido documentação #'robust'
              )]

"""
model = [LSTM(
            max_steps=max_steps, #padrão = 1000
            h=horizon, 
            input_size=-1, #padrão = -1, base toda
            batch_size=32, #padrão = 32
            encoder_hidden_size=200, #padrão = 200
            encoder_n_layers=2, #padrão = 2
            decoder_hidden_size=200, #padrão = 200
            decoder_layers=2, #padrão = 2
            context_size=10, #padrão = 10
              #float=1e-3, Learning rate between (0, 1).
            learning_rate=0.001, #quanto menor, melhor # padrão = 0.001
              #str list, future exogenous columns.
            futr_exog_list = ['dayofweek', 'monthofyear', 'dia_das_maes', 'dia_dos_pais', 'dia_dos_namorados', 'halloween', 'black_friday', 'natal', 'copa_do_mundo', 'eleicoes', 'dia_do_trabalhador', 'dia_de_finados', 'confraternizacao_universal', 'independencia_do_brasil', 'nossa_senhora_aparecida', 'proclamacao_da_republica', 'sexta_feira_santa', 'pascoa', 'carnaval'],
              #str list, historic exogenous columns.
            hist_exog_list = ['QLF'],
              #PyTorch module, instantiated train loss class from losses collection.   
            loss=MAE(),
              #PyTorch module=loss, instantiated valid loss class from losses collection.
            valid_loss=MAE(),
              #str=‘robust’, type of scaler for temporal inputs normalization see temporal scalers.                       
            scaler_type='robust' #sugerido documentação #'robust'
              ),
         NHITS(
            max_steps=max_steps, #int=1000,
            h = horizon,
            input_size = 5*horizon,
            futr_exog_list = ['dayofweek', 'monthofyear', 'dia_das_maes', 'dia_dos_pais', 'dia_dos_namorados', 'halloween', 'black_friday', 'natal', 'copa_do_mundo', 'eleicoes', 'dia_do_trabalhador', 'dia_de_finados', 'confraternizacao_universal', 'independencia_do_brasil', 'nossa_senhora_aparecida', 'proclamacao_da_republica', 'sexta_feira_santa', 'pascoa', 'carnaval', 'covid'],
            hist_exog_list = ['QLF'],
            scaler_type = 'robust',
            learning_rate=0.001, #float=0.001
            batch_size=32, #int=32
            loss=MAE(),
            valid_loss=MAE(),
            activation = 'ReLU'# str, activation from [‘ReLU’, ‘Softplus’, ‘Tanh’, ‘SELU’, ‘LeakyReLU’, ‘PReLU’, ‘Sigmoid’].
            ),
        BiTCN(
            max_steps=max_steps, #int=1000,
            h = horizon,
            input_size = 5*horizon,
            futr_exog_list = ['dayofweek', 'monthofyear', 'dia_das_maes', 'dia_dos_pais', 'dia_dos_namorados', 'halloween', 'black_friday', 'natal', 'copa_do_mundo', 'eleicoes', 'dia_do_trabalhador', 'dia_de_finados', 'confraternizacao_universal', 'independencia_do_brasil', 'nossa_senhora_aparecida', 'proclamacao_da_republica', 'sexta_feira_santa', 'pascoa', 'carnaval', 'covid'],
            hist_exog_list = ['QLF'],
            scaler_type = 'robust',
            learning_rate=0.001, #float=0.001
            batch_size=32, #int=32
            loss=MAE(),
            valid_loss=MAE(),
            ),
        GRU(
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
            futr_exog_list = ['dayofweek', 'monthofyear', 'dia_das_maes', 'dia_dos_pais', 'dia_dos_namorados', 'halloween', 'black_friday', 'natal', 'copa_do_mundo', 'eleicoes', 'dia_do_trabalhador', 'dia_de_finados', 'confraternizacao_universal', 'independencia_do_brasil', 'nossa_senhora_aparecida', 'proclamacao_da_republica', 'sexta_feira_santa', 'pascoa', 'carnaval', 'covid'],
            hist_exog_list = ['QLF'],
            learning_rate=0.001, #:float=0.001
            batch_size=32,
            scaler_type='robust', #:str='robust'
            random_seed=1,
        ),
        NBEATSx(
            max_steps=max_steps, #:int=1000
            input_size=5*horizon,
            h=horizon,
            n_harmonics=2,
            n_polynomials=2,
            activation='ReLU',
            learning_rate=0.001, #:float=0.001   
            num_lr_decays=3, #:int=3
            early_stop_patience_steps=-1, #:int=-1
            val_check_steps=100, #:int=100
            batch_size=32,
            random_seed=1, #:int=1
            )
        ]
"""

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