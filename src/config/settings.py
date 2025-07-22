"""
Configurações centralizadas do projeto.

COMO USAR:
1. MARCAS: Selecione quais marcas processar (ex: ['BB', 'LL', 'DD'])
2. TIPOS_PREVISAO: Selecione tipos de previsão (ex: ['GERAL', 'GRIFFE'])
3. MODELOS_A_EXECUTAR: Selecione modelos para treinar (ex: ['LSTM', 'GRU'])
4. METRICS: Selecione métricas para avaliar (ex: ['MAPE', 'RMSE'])
5. VARIAVEIS_FUTURAS: Selecione variáveis futuras (ex: ['black_friday', 'natal'])
6. VARIAVEIS_HISTORICAS: Selecione variáveis históricas (ex: ['dayofweek', 'monthofyear'])

EXEMPLO DE CONFIGURAÇÃO MÍNIMA:
- MARCAS = ['BB']
- TIPOS_PREVISAO = ['GERAL']
- MODELOS_A_EXECUTAR = ['LSTM']
- METRICS = ['MAPE']
- VARIAVEIS_FUTURAS = []
- VARIAVEIS_HISTORICAS = ['dayofweek']
"""
import os
from pathlib import Path
from datetime import datetime, timedelta

# =============================================================================
# CONFIGURAÇÕES DE DIRETÓRIOS
# =============================================================================
BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATA_DIR = BASE_DIR / 'data'
RAW_DATA_DIR = DATA_DIR / 'raw'
PROCESSED_DATA_DIR = DATA_DIR / 'processed'
FORECASTS_DIR = DATA_DIR / 'forecasts'

# =============================================================================
# CONFIGURAÇÕES DE DATAS
# =============================================================================
DATA_INICIO_BASE = '2020-01-01'
DATA_FINAL_BASE = '2024-09-30'
DATA_TRAIN = '2024-06-30'
DATA_TEST = '2024-07-01'
DATA_INICIO_FUTR = '2024-10-01'
DATA_FINAL_FUTR = '2024-12-31'
DATA_INICIO_FUTR_TEST = '2024-10-01'
DATA_FINAL_FUTR_TEST = '2024-12-31'

# =============================================================================
# CONFIGURAÇÕES DE MARCAS E TIPOS DE PREVISÃO
# =============================================================================
# 🔧 MARCAS: Selecione quais marcas processar
# Opções disponíveis: ['BB', 'LL', 'DD', 'JJ'] (substitua pelos nomes reais)
MARCAS = ['BB']  # Para processar apenas BB, deixe ['BB']
# MARCAS = ['BB', 'LL', 'DD']  # Para processar múltiplas marcas

# 🔧 TIPOS_PREVISAO: Selecione tipos de previsão
# Opções disponíveis: ['GERAL', 'GRIFFE', 'GRIFFE_N1']
TIPOS_PREVISAO = ['GERAL']  # Para processar apenas GERAL
# TIPOS_PREVISAO = ['GERAL', 'GRIFFE']  # Para processar múltiplos tipos

# =============================================================================
# CONFIGURAÇÕES DE MODELOS
# =============================================================================
# 🔧 MODELOS_A_EXECUTAR: Selecione quais modelos treinar
# Opções disponíveis: ['LSTM', 'GRU', 'NHITS', 'NBEATSx']
MODELOS_A_EXECUTAR = ['LSTM', 'GRU', 'NHITS', 'NBEATSx']  # Todos os modelos
# MODELOS_A_EXECUTAR = ['LSTM']  # Apenas LSTM
# MODELOS_A_EXECUTAR = ['LSTM', 'GRU']  # Apenas LSTM e GRU

# =============================================================================
# CONFIGURAÇÕES DE MÉTRICAS
# =============================================================================
# 🔧 METRICS: Selecione quais métricas calcular
# Opções disponíveis: ['MAPE', 'RMSE', 'MAE']
METRICS = ['MAPE', 'RMSE', 'MAE']  # Todas as métricas
# METRICS = ['MAPE']  # Apenas MAPE
# METRICS = ['MAPE', 'RMSE']  # Apenas MAPE e RMSE

# =============================================================================
# CONFIGURAÇÕES DE VARIÁVEIS
# =============================================================================
# 🔧 VARIAVEIS_FUTURAS: Selecione variáveis futuras (eventos especiais)
# Opções disponíveis: ['black_friday', 'carnaval', 'natal', 'halloween', 
#                     'dia_do_trabalhador', 'eleicoes', 'independencia_do_brasil',
#                     'nossa_senhora_aparecida', 'pascoa', 'proclamacao_da_republica',
#                     'sexta_feira_santa', 'confraternizacao_universal', 'copa_do_mundo',
#                     'covid', 'dia_das_maes', 'dia_de_finados', 'dia_dos_namorados',
#                     'dia_dos_pais']
VARIAVEIS_FUTURAS = []  # Nenhuma variável futura
# VARIAVEIS_FUTURAS = ['black_friday', 'natal']  # Apenas Black Friday e Natal
# VARIAVEIS_FUTURAS = ['black_friday', 'carnaval', 'natal', 'halloween']  # Múltiplas

# 🔧 VARIAVEIS_HISTORICAS: Selecione variáveis históricas (características temporais)
# Opções disponíveis: ['dayofweek', 'monthofyear']
VARIAVEIS_HISTORICAS = []  # Nenhuma variável histórica
# VARIAVEIS_HISTORICAS = ['dayofweek']  # Apenas dia da semana
# VARIAVEIS_HISTORICAS = ['dayofweek', 'monthofyear']  # Dia da semana e mês

# =============================================================================
# CONFIGURAÇÕES AVANÇADAS (não alterar a menos que necessário)
# =============================================================================
MARCA = os.getenv('MARCA', 'default')
TIPO_PREVISAO = os.getenv('TIPO_PREVISAO', 'GERAL')
HORIZON = int(os.getenv('HORIZON', '365'))
FREQ = os.getenv('FREQ', 'D')

# Configurações de logging
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
LOG_FILE = BASE_DIR / 'app.log'

# =============================================================================
# CONFIGURAÇÕES DE MODELOS (HIPERPARÂMETROS)
# =============================================================================
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

# =============================================================================
# FUNÇÕES AUXILIARES
# =============================================================================
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