"""
Configurações centralizadas do projeto.
"""
import os
from pathlib import Path
from datetime import datetime, timedelta

# Diretórios do projeto
BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATA_DIR = BASE_DIR / 'data'
RAW_DATA_DIR = DATA_DIR / 'raw'
PROCESSED_DATA_DIR = DATA_DIR / 'processed'
FORECASTS_DIR = DATA_DIR / 'forecasts'

# Configurações de datas
DATA_INICIO_BASE = '2020-01-01'
DATA_FINAL_BASE = '2024-09-30'
DATA_TRAIN = '2024-06-30'
DATA_TEST = '2024-07-01'
DATA_INICIO_FUTR = '2024-10-01'
DATA_FINAL_FUTR = '2024-12-31'
DATA_INICIO_FUTR_TEST = '2024-10-01'
DATA_FINAL_FUTR_TEST = '2024-12-31'

# Configurações das marcas e tipos
MARCAS = ['BB']#, 'LL', 'DD', 'JJ']  # Substituir pelos nomes reais das marcas
TIPOS_PREVISAO = ['GERAL']#, 'GRIFFE', 'GRIFFE_N1']

# Configurações do modelo
MARCA = os.getenv('MARCA', 'default')
TIPO_PREVISAO = os.getenv('TIPO_PREVISAO', 'GERAL')
HORIZON = int(os.getenv('HORIZON', '365'))
FREQ = os.getenv('FREQ', 'D')

# Configurações de logging
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
LOG_FILE = BASE_DIR / 'app.log'

# Configurações de modelos
MODEL_PARAM_GRID = {
    'LSTM': {
        'max_steps': [1],
        'learning_rate': [0.001],
        'batch_size': [32],
        'encoder_hidden_size': [200],
        'decoder_hidden_size': [200],
        'encoder_n_layers': [2],
        'decoder_layers': [2],
        'context_size': [10],
        'encoder_bias': [True],
        'encoder_dropout': [0.0],
        'num_lr_decays': [-1],
        'early_stop_patience_steps': [-1],
        'val_check_steps': [100],
        'random_seed': [1],
        'num_workers_loader': [0],
        'drop_last_loader': [False]
    },
    'GRU': {
        'max_steps': [1],
        'learning_rate': [0.001],
        'batch_size': [64],
        'encoder_hidden_size': [50],
        'decoder_hidden_size': [50],
        'encoder_n_layers': [2],
        'decoder_layers': [2],
        'context_size': [10],
        'encoder_activation': ['tanh'],
        'encoder_bias': [True],
        'encoder_dropout': [0.0],
        'num_lr_decays': [-1],
        'early_stop_patience_steps': [-1],
        'val_check_steps': [100],
        'scaler_type': ['robust'],
        'random_seed': [1],
        'loss': ['MAE']
    },
    'NHITS': {
        'max_steps': [1],
        'learning_rate': [0.001],
        'batch_size': [32],
        'activation': ['ReLU'],
        'n_blocks': [[1, 1, 1]],
        'mlp_units': [[[512, 512], [512, 512], [512, 512]]],
        'n_pool_kernel_size': [[2, 2, 1]],
        'n_freq_downsample': [[4, 2, 1]],
        'pooling_mode': ['MaxPool1d'],
        'dropout_prob_theta': [0.0],
        'scaler_type': ['identity'],
        'windows_batch_size': [1024],
        'step_size': [1],
        'random_seed': [1],
        'num_lr_decays': [3],
        'start_padding_enabled': [False]
    },
    'NBEATSx': {
        'max_steps': [1],
        'learning_rate': [0.001],
        'batch_size': [32],
        'activation': ['ReLU']
    }
}

# Configurações de métricas
METRICS = ['MAPE', 'RMSE', 'MAE']

# Grid de hiperparâmetros para grid search
MODEL_PARAM_GRID = {
    'LSTM': {
        'max_steps': [1],
        'learning_rate': [0.001],
        'batch_size': [32],
        'encoder_hidden_size': [200],
        'decoder_hidden_size': [200],
        'encoder_n_layers': [2],
        'decoder_layers': [2],
        'context_size': [10],
        'encoder_bias': [True],
        'encoder_dropout': [0.0],
        'num_lr_decays': [-1],
        'early_stop_patience_steps': [-1],
        'val_check_steps': [100],
        'random_seed': [1],
        'num_workers_loader': [0],
        'drop_last_loader': [False]
    },
    'GRU': {
        'max_steps': [1000],
        'learning_rate': [0.001],
        'batch_size': [64],
        'encoder_hidden_size': [50],
        'decoder_hidden_size': [50],
        'encoder_n_layers': [2],
        'decoder_layers': [2],
        'context_size': [10],
        'encoder_activation': ['tanh'],
        'encoder_bias': [True],
        'encoder_dropout': [0.0],
        'num_lr_decays': [-1],
        'early_stop_patience_steps': [-1],
        'val_check_steps': [100],
        'scaler_type': ['robust'],
        'random_seed': [1],
        'loss': ['MAE']
    },
    'NHITS': {
        'max_steps': [1],
        'learning_rate': [0.001],
        'batch_size': [32],
        'activation': ['ReLU'],
        'n_blocks': [[1, 1, 1]],
        'mlp_units': [[[512, 512], [512, 512], [512, 512]]],
        'n_pool_kernel_size': [[2, 2, 1]],
        'n_freq_downsample': [[4, 2, 1]],
        'pooling_mode': ['MaxPool1d'],
        'dropout_prob_theta': [0.0],
        'scaler_type': ['identity'],
        'windows_batch_size': [1024],
        'step_size': [1],
        'random_seed': [1],
        'num_lr_decays': [3],
        'start_padding_enabled': [False]
    },
    'NBEATSx': {
        'max_steps': [1],
        'learning_rate': [0.001],
        'batch_size': [32],
        'activation': ['ReLU']
    }
}

# Função para criar estrutura de diretórios
def create_forecast_directories():
    """Cria a estrutura de diretórios para as previsões."""
    for marca in MARCAS:
        for tipo in TIPOS_PREVISAO:
            dir_path = FORECASTS_DIR / marca / tipo
            dir_path.mkdir(parents=True, exist_ok=True)
    return FORECASTS_DIR

# Criar diretórios necessários
for directory in [RAW_DATA_DIR, PROCESSED_DATA_DIR]:
    directory.mkdir(parents=True, exist_ok=True)

# Criar estrutura de diretórios para previsões
FORECASTS_DIR = create_forecast_directories()

# Modelos a serem executados (adicione ou remova conforme desejar)
MODELOS_A_EXECUTAR = ['LSTM', 'GRU', 'NHITS', 'NBEATSx'] 

# Variáveis exógenas futuras e históricas (ajuste conforme necessário)
VARIAVEIS_FUTURAS = []
VARIAVEIS_HISTORICAS = [] 