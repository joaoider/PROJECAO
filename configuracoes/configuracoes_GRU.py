print('configuracoes_GRU.py iniciado')

from configuracoes.imports import *

# Definições específicas para o modelo GRU
freq = 'D'  # frequência dos dados Diário
horizon = 365  # dias futuros para previsão
variaveis_futuras = ['dayofweek', 'monthofyear', 'dia_das_maes', 'dia_dos_pais', 'dia_dos_namorados', 'halloween', 'black_friday', 'natal', 'copa_do_mundo', 'eleicoes', 'dia_do_trabalhador', 'dia_de_finados', 'confraternizacao_universal', 'independencia_do_brasil', 'nossa_senhora_aparecida', 'proclamacao_da_republica', 'sexta_feira_santa', 'pascoa', 'carnaval', 'covid', 'liquidacao']
variaveis_historicas = ['QLF']

# Definir a marca
marca = 'LL'
data_inicio_base = '2013-01-01'

# Modelo a ser utilizado
modelo = 'GRU'

# Parâmetros do modelo GRU
parametros_modelos = {
    'GRU': {
        'max_steps': [1],  # Número máximo de iterações
        'learning_rate': [0.001],#, 0.0001],  # 0.001 Taxa de aprendizado
        'batch_size': [32],#, 64],  # 32 Tamanho do batch
        'encoder_hidden_size': [200],#, 300],  # 200 Tamanho da camada oculta do encoder
        'decoder_hidden_size': [200],#, 300],  # 200 Tamanho da camada oculta do decoder
        'encoder_n_layers': [2],#, 3],  # 2 Camadas do encoder
        'decoder_layers': [2],#, 3],  # 2 Camadas do decoder
        'context_size': [10],#, 20],  # 10 Tamanho do contexto
        'encoder_activation': ['tanh'],#, 'relu'],  # Função de ativação do encoder
        'encoder_bias': [True],  # Uso de bias no encoder
        'encoder_dropout': [0.0],#, 0.2],  # 0.0 Dropout no encoder
        'num_lr_decays': [-1],  # Número de decaimentos da taxa de aprendizado
        'early_stop_patience_steps': [-1],  # Paciência para early stopping
        'val_check_steps': [100],#, 200],  # 100 Verificação de validação a cada N passos
        'scaler_type': ['robust', 'identity'],  # Tipo de normalização dos dados
        'random_seed': [1],  # Semente aleatória para reprodutibilidade
        'num_workers_loader': [0],  # Número de workers para o loader
        'drop_last_loader': [False],  # Se o último batch será descartado se incompleto
        'optimizer': [None],  # Otimizador (pode ser customizado)
        'lr_scheduler': [None],  # Scheduler da taxa de aprendizado
    }
}

# Função para gerar combinações de parâmetros para o GRU
def gerar_combinacoes_parametros(modelo):
    params = parametros_modelos[modelo]
    return list(product(
        params['max_steps'], 
        params['learning_rate'], 
        params['batch_size'], 
        params['encoder_hidden_size'], 
        params['decoder_hidden_size'], 
        params['encoder_n_layers'], 
        params['decoder_layers'], 
        params['context_size'], 
        params['encoder_activation'],
        params['encoder_bias'],
        params['encoder_dropout'],
        params['num_lr_decays'],
        params['early_stop_patience_steps'],
        params['val_check_steps'],
        params['scaler_type'],
        params['random_seed'],
        params['num_workers_loader'],
        params['drop_last_loader'],
        params['optimizer'],
        params['lr_scheduler']
    ))

print('configuracoes_GRU.py finalizado')