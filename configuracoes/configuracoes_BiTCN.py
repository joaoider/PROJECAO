print('configuracoes_BiTCN.py iniciado')

from configuracoes.imports import *

# Definições específicas para o modelo BiTCN
freq = 'D'  # frequencia dos dados Diário
horizon = 365  # dias futuros para previsao
variaveis_futuras = ['dayofweek', 'monthofyear', 'dia_das_maes', 'dia_dos_pais', 'dia_dos_namorados', 'halloween', 'black_friday', 'natal', 'copa_do_mundo', 'eleicoes', 'dia_do_trabalhador', 'dia_de_finados', 'confraternizacao_universal', 'independencia_do_brasil', 'nossa_senhora_aparecida', 'proclamacao_da_republica', 'sexta_feira_santa', 'pascoa', 'carnaval', 'covid', 'liquidacao']
variaveis_historicas = ['QLF']

# Definir a marca
marca = 'LL'
data_inicio_base = '2013-01-01'

# Modelo a ser utilizado
modelo = 'BiTCN'

max_steps = 1
activation = 'ReLU'
learning_rate = 0.001  # padrão 0.001
batch_size = 32  # padrão 32
encoder_hidden_size = 200  # padrão 200
decoder_hidden_size = 200  # padrão 200
encoder_n_layers = 2  # padrão 2
decoder_layers = 2  # padrão 2
context_size = 10  # padrão 10

# Configurações específicas de parâmetros para o BiTCN
parametros_modelos = {
    'BiTCN': {
        'max_steps': [1],#, 2],  # diferentes tamanhos de passo
        'learning_rate': [0.001], #, 0.01],  # diferentes taxas de aprendizado
        'batch_size': [32], #, 64]  # diferentes tamanhos de lote
    }
}

# Função para gerar combinações de parâmetros para o BiTCN
def gerar_combinacoes_parametros(modelo):
    params = parametros_modelos[modelo]
    return list(product(params['max_steps'], params['learning_rate'], params['batch_size']))

print('configuracoes_BiTCN.py finalizado')