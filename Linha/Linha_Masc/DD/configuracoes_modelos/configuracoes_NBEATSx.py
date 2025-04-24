print('configuracoes_NBEATSx.py iniciado')

from configuracoes_modelos.imports import *
from itertools import product

# Modelo a ser utilizado
modelo = 'NBEATSx'

# Configurações específicas de parâmetros para o NBEATSx
parametros_modelos = {
    'NBEATSx': {
        'max_steps': [1], #, 2],  # ajustando para maior flexibilidade
        'learning_rate': [0.001], #, 0.01],  # várias opções de taxa de aprendizado
        'batch_size': [32], #, 64],  # diferentes tamanhos de lote
        'activation': ['ReLU'], #, 'Softplus']  # ativação específica para NBEATSx
    }
}

# Função para gerar combinações de parâmetros para o NBEATSx
def gerar_combinacoes_parametros(modelo):
    params = parametros_modelos[modelo]
    return list(product(params['max_steps'], params['learning_rate'], params['batch_size'], params['activation']))

print('configuracoes_NBEATSx.py finalizado')