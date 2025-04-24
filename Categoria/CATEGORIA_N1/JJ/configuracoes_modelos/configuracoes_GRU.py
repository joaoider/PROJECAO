print('configuracoes_GRU.py iniciado')

from configuracoes_modelos.imports import *
from itertools import product

# Modelo a ser utilizado
modelo = 'GRU'

# Parâmetros do modelo GRU
parametros_modelos = {
    'GRU': {
        'max_steps': [1000],  # Número máximo de iterações
        'learning_rate': [0.001],  # 0.001 Taxa de aprendizado
        'batch_size': [64],  # 32 Tamanho do batch
        'encoder_hidden_size': [25],  # 200 Tamanho da camada oculta do encoder
        'decoder_hidden_size': [25],  # 200 Tamanho da camada oculta do decoder
        'encoder_n_layers': [2],  # 2 Camadas do encoder
        'decoder_layers': [2],  # 2 Camadas do decoder
        'context_size': [10],  # 10 Tamanho do contexto
        'encoder_activation': ['tanh'],  # relu  # Função de ativação do encoder
        'encoder_bias': [True],  # Uso de bias no encoder
        'encoder_dropout': [0.0],  # 0.0 Dropout no encoder
        'num_lr_decays': [-1],  # Número de decaimentos da taxa de aprendizado
        'early_stop_patience_steps': [-1],  # Paciência para early stopping
        'val_check_steps': [100],#, 200],  # 100 Verificação de validação a cada N passos
        'scaler_type': ['robust'], #  identity # Tipo de normalização dos dados
        'random_seed': [1],  # Semente aleatória para reprodutibilidade
        'loss': [MAE()] # (), MAE, MSE, RMSE, MAPE, DistributionLoss
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
        params['loss']
    ))

print('configuracoes_GRU.py finalizado')