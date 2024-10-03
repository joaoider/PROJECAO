print('configuracoes_NHITS.py iniciado')

from configuracoes.imports import *
from itertools import product 

# Definições específicas para o modelo NHITS
freq = 'D'  # Frequência dos dados Diário
horizon = 365  # Dias futuros para previsão
variaveis_futuras = ['dayofweek', 'monthofyear', 'dia_das_maes', 'dia_dos_pais', 'dia_dos_namorados', 'halloween', 'black_friday', 'natal', 'copa_do_mundo', 'eleicoes', 'dia_do_trabalhador', 'dia_de_finados', 'confraternizacao_universal', 'independencia_do_brasil', 'nossa_senhora_aparecida', 'proclamacao_da_republica', 'sexta_feira_santa', 'pascoa', 'carnaval', 'covid', 'liquidacao']
variaveis_historicas = ['QLF']

# Definir a marca
marca = 'LL'
data_inicio_base = '2013-01-01'

# Modelo a ser utilizado
modelo = 'NHITS'

# Parâmetros do modelo NHITS
parametros_modelos = {
    'NHITS': {
        'max_steps': [1], # Número máximo de iterações
        'learning_rate': [0.001],#, 0.0001],  # 0.001 Taxa de aprendizado
        'batch_size': [32],#, 64],  # 32 Tamanho do batch
        'activation': ['ReLU'],#, 'Softplus'],  # Funções de ativação
        'n_blocks': [[1, 1, 1]],  # Número de blocos por stack (camada)
        'mlp_units': [[[512, 512], [512, 512], [512, 512]]],  # Unidades MLP por bloco
        'n_pool_kernel_size': [[2, 2, 1]],  # Tamanho do kernel para pooling
        'n_freq_downsample': [[4, 2, 1]],  # Taxas de downsample por frequência
        'pooling_mode': ['MaxPool1d'],#, 'AvgPool1d'],  # Modos de pooling
        'dropout_prob_theta': [0.0],#, 0.1],  # Probabilidade de dropout
        'scaler_type': ['identity'],#, 'robust'],  # Tipo de normalização dos dados
        'windows_batch_size': [1024],  # Tamanho do batch para janela de inferência
        'step_size': [1],  # Tamanho do passo
        'random_seed': [1],  # Semente aleatória para reprodutibilidade
        'num_lr_decays': [3],  # Número de decaimentos de taxa de aprendizado
        'start_padding_enabled': [False], #, True],  # Habilitar preenchimento de início
    }
}

# Função para gerar combinações de parâmetros
def gerar_combinacoes_parametros(modelo):
    params = parametros_modelos[modelo]
    return list(product(
        params['max_steps'],
        params['learning_rate'], 
        params['batch_size'], 
        params['activation'],
        params['n_blocks'],
        params['mlp_units'],
        params['n_pool_kernel_size'],
        params['n_freq_downsample'],
        params['pooling_mode'],
        params['dropout_prob_theta'],
        params['scaler_type'],
        params['windows_batch_size'],
        params['step_size'],
        params['random_seed'],
        params['num_lr_decays'],
        params['start_padding_enabled']
    ))

print('configuracoes_NHITS.py finalizado')