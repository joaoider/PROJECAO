print('configuracoes.py iniciado')

freq = 'D' # frequencia dos dados Diário
horizon = 365 # dias futuros para previsao
variaveis_futuras = ['dayofweek', 'monthofyear', 'dia_das_maes', 'dia_dos_pais', 'dia_dos_namorados', 'halloween', 'black_friday', 'natal', 'copa_do_mundo', 'eleicoes', 'dia_do_trabalhador', 'dia_de_finados', 'confraternizacao_universal', 'independencia_do_brasil', 'nossa_senhora_aparecida', 'proclamacao_da_republica', 'sexta_feira_santa', 'pascoa', 'carnaval', 'covid', 'liquidacao']
variaveis_historicas = ['QLF']
# marcas
marca = 'LL' # 'JJ', 'DD', 'LL'

if marca == 'JJ':
    data_inicio_base = '2013-01-01'
if marca == 'DD':
    data_inicio_base = '2018-01-01'
if marca == 'LL':
    data_inicio_base = '2013-01-01'

# modelos disponíveis
# LSTM, NHITS, BiTCN, GRU, NBEATSx
modelo = ['LSTM', 'NHITS']

max_steps = 1
activation = 'ReLU'
learning_rate = 0.001 # padrao 0.001
batch_size = 32 # padrão 32
encoder_hidden_size = 200 # padrão 200
decoder_hidden_size = 200 # padrão 200
encoder_n_layers = 2 # padrão 2
decoder_layers = 2 # padrão 2
context_size = 10 # padrão 10

# Configurações específicas de parâmetros para cada modelo
parametros_modelos = {
    'LSTM': {
        'max_steps': [1, 2],
        'learning_rate': [0.001, 0.01],
        'batch_size': [32, 64]
    },
    'NHITS': {
        'max_steps': [1, 2],
        'learning_rate': [0.001, 0.01],
        'batch_size': [32, 64],
        'activation': ['ReLU', 'Softplus']
    },
    'GRU': {
        'max_steps': [1, 2],
        'learning_rate': [0.001, 0.01],
        'batch_size': [32, 64]
    },
    'NBEATSx': {
        'max_steps': [1, 2],
        'learning_rate': [0.001, 0.01],
        'batch_size': [32, 64],
        'activation': ['ReLU', 'Softplus']  # Adicionado 'activation' para NBEATSx
    },
    'BiTCN': {
        'max_steps': [1, 2],
        'learning_rate': [0.001, 0.01],
        'batch_size': [32, 64]
    }
}

# Função para gerar combinações de parâmetros para cada modelo
def gerar_combinacoes_parametros(modelo):
    params = parametros_modelos[modelo]
    # Verificar se há parâmetros adicionais como 'activation' para NHITS e NBEATSx
    if 'activation' in params:
        return list(product(params['max_steps'], params['learning_rate'], params['batch_size'], params['activation']))
    else:
        return list(product(params['max_steps'], params['learning_rate'], params['batch_size']))

# Dicionário que mapeia o nome do modelo para o módulo correspondente
modelos_disponiveis = {
    'LSTM': 'models.model_LSTM',
    'NHITS': 'models.model_NHITS',
    'GRU': 'models.model_GRU',
    'NBEATSx': 'models.model_NBEATSx',
    'BiTCN': 'models.model_BiTCN'
}

# Dicionário que mapeia o nome do modelo para o módulo correspondente
modelos_utilizados = {
    'LSTM': 'models.model_LSTM'
}

print('configuracoes.py finalizado')