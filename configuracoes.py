print('configuracoes.py iniciado')

freq = 'D' # frequencia dos dados Diário

horizon = 365 # dias futuros para previsao

variaveis_futuras = ['dayofweek', 'monthofyear', 'dia_das_maes', 'dia_dos_pais', 'dia_dos_namorados', 'halloween', 'black_friday', 'natal', 'copa_do_mundo', 'eleicoes', 'dia_do_trabalhador', 'dia_de_finados', 'confraternizacao_universal', 'independencia_do_brasil', 'nossa_senhora_aparecida', 'proclamacao_da_republica', 'sexta_feira_santa', 'pascoa', 'carnaval', 'covid', 'liquidacao']

variaveis_historicas = ['QLF']

# marcas
# 'JJ', 'DD', 'LL'
marca = ['JJ', 'LL']

# modelos disponíveis
# LSTM, NHITS, BiTCN, GRU, NBEATSx
modelo = ['LSTM', 'NHITS']

max_steps = 1
activation = 'ReLU'
learning_rate = 0.1 # padrao 0.001
batch_size = 1 # padrão 32
encoder_hidden_size = 1 # padrão 200
decoder_hidden_size = 1 # padrão 200
encoder_n_layers = 1 # padrão 2
decoder_layers = 1 # padrão 2
context_size = 1 # padrão 10

print('configuracoes.py finalizado')