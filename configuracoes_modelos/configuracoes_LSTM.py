print('configuracoes_LSTM.py iniciado')

from configuracoes_modelos.imports import *
from itertools import product

# Modelo a ser utilizado
modelo = 'LSTM'

# Parâmetros do modelo LSTM
parametros_modelos = {
    'LSTM': {
        'max_steps': [1], #, 2],
        'learning_rate': [0.001],# 0.0001], # padrão 0.001
        'batch_size': [32],# 64], # padrão 32
        'encoder_hidden_size': [1],# 300], # padrão 200
        'decoder_hidden_size': [1],# 300], # padrão 200
        'encoder_n_layers': [2],# 3], # padrão 2
        'decoder_layers': [2],# 3], # padrão 2
        'context_size': [10],# 20], # padrão 10
        'encoder_bias': [True],  # Inclui bias no encoder
        'encoder_dropout': [0.0],# 0.2], # padrão 0.
        'num_lr_decays': [-1],  # Número de reduções da taxa de aprendizado
        'early_stop_patience_steps': [-1],  # Número de etapas antes de parar precocemente
        'val_check_steps': [100],# 200],  # Número de etapas entre as verificações de validação # padrão 100
        'random_seed': [1],  # Semente aleatória
        'num_workers_loader': [0],  # Número de trabalhadores para carregar os dados
        'drop_last_loader': [False]  # Descartar o último lote incompleto
    }
}

# Função para gerar combinações de parâmetros
def gerar_combinacoes_parametros(modelo):
    params = parametros_modelos[modelo]
    # Gerar todas as combinações de parâmetros
    return list(product(
        params['max_steps'], 
        params['learning_rate'], 
        params['batch_size'], 
        params['encoder_hidden_size'], 
        params['decoder_hidden_size'], 
        params['encoder_n_layers'], 
        params['decoder_layers'], 
        params['context_size'],
        params['encoder_bias'],
        params['encoder_dropout'],
        params['num_lr_decays'],
        params['early_stop_patience_steps'],
        params['val_check_steps'],
        params['random_seed'],
        params['num_workers_loader'],
        params['drop_last_loader']
    ))

print('configuracoes_LSTM.py finalizado')