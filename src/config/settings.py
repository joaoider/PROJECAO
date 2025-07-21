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
        'hidden_size': [32, 64],
        'num_layers': [1, 2],
        'dropout': [0.1],
        'batch_size': [16, 32],
        'learning_rate': [0.001],
        'epochs': [50]
    },
    'GRU': {
        'hidden_size': [32, 64],
        'num_layers': [1, 2],
        'dropout': [0.1],
        'batch_size': [16, 32],
        'learning_rate': [0.001],
        'epochs': [50]
    },
    'NHITS': {
        'n_blocks': [2, 3],
        'mlp_units': [32, 64],
        'dropout': [0.1],
        'batch_size': [16, 32],
        'learning_rate': [0.001],
        'epochs': [50]
    },
    'NBEATSx': {
        'n_blocks': [2, 3],
        'mlp_units': [32, 64],
        'dropout': [0.1],
        'batch_size': [16, 32],
        'learning_rate': [0.001],
        'epochs': [50]
    }
}

# Configurações de métricas
METRICS = ['MAPE', 'RMSE', 'MAE']

# Grid de hiperparâmetros para grid search
MODEL_PARAM_GRID = {
    'LSTM': {
        'hidden_size': [32, 64],
        'num_layers': [1, 2],
        'dropout': [0.1],
        'batch_size': [16, 32],
        'learning_rate': [0.001],
        'epochs': [50]
    },
    'GRU': {
        'hidden_size': [32, 64],
        'num_layers': [1, 2],
        'dropout': [0.1],
        'batch_size': [16, 32],
        'learning_rate': [0.001],
        'epochs': [50]
    },
    'NHITS': {
        'n_blocks': [2, 3],
        'mlp_units': [32, 64],
        'dropout': [0.1],
        'batch_size': [16, 32],
        'learning_rate': [0.001],
        'epochs': [50]
    },
    'NBEATSx': {
        'n_blocks': [2, 3],
        'mlp_units': [32, 64],
        'dropout': [0.1],
        'batch_size': [16, 32],
        'learning_rate': [0.001],
        'epochs': [50]
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