print('configuracoes_NBEATSx.py iniciado')

from configuracoes.imports import *

# Definições específicas para o modelo NBEATSx
freq = 'D'  # frequencia dos dados Diário
horizon = 365  # dias futuros para previsao
variaveis_futuras = ['dayofweek', 'monthofyear', 'dia_das_maes', 'dia_dos_pais', 'dia_dos_namorados', 'halloween', 'black_friday', 'natal', 'copa_do_mundo', 'eleicoes', 'dia_do_trabalhador', 'dia_de_finados', 'confraternizacao_universal', 'independencia_do_brasil', 'nossa_senhora_aparecida', 'proclamacao_da_republica', 'sexta_feira_santa', 'pascoa', 'carnaval', 'covid', 'liquidacao']
variaveis_historicas = ['QLF']

# Definir a marca
marca = 'LL'
data_inicio_base = '2013-01-01'

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