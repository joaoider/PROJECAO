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
from datetime import datetime, timedelta

# Data atual para cálculos dinâmicos
DATA_ATUAL = datetime.now()

# Configurações dinâmicas baseadas na data atual
DATA_INICIO_BASE = '2020-01-01'  # Data inicial fixa para dados históricos
DATA_FINAL_BASE = DATA_ATUAL.strftime('%Y-%m-%d')  # Data atual como fim dos dados

# Período de treinamento: até 1 ano atrás da data atual
DATA_TRAIN = (DATA_ATUAL - timedelta(days=365)).strftime('%Y-%m-%d')

# Período de teste: último ano (desde 1 ano atrás até hoje)
DATA_TEST = (DATA_ATUAL - timedelta(days=365)).strftime('%Y-%m-%d')

# Período de previsões futuras: próximo ano (desde hoje até 1 ano à frente)
DATA_INICIO_FUTR = DATA_ATUAL.strftime('%Y-%m-%d')
DATA_FINAL_FUTR = (DATA_ATUAL + timedelta(days=365)).strftime('%Y-%m-%d')

# Configurações de teste futuro (mantidas para compatibilidade)
DATA_INICIO_FUTR_TEST = DATA_INICIO_FUTR
DATA_FINAL_FUTR_TEST = DATA_FINAL_FUTR

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
MODELOS_A_EXECUTAR = ['LSTM']  # Apenas LSTM
# MODELOS_A_EXECUTAR = ['LSTM', 'GRU']  # Apenas LSTM e GRU

# =============================================================================
# CONFIGURAÇÕES DE MÉTRICAS
# =============================================================================
# 🔧 METRICS: Selecione quais métricas calcular
# Opções disponíveis: ['MAPE', 'RMSE', 'MAE', 'MSE']
METRICS = ['MAPE', 'RMSE', 'MAE', 'MSE']  # Todas as métricas
# METRICS = ['MAPE']  # Apenas MAPE
# METRICS = ['MAPE', 'RMSE']  # Apenas MAPE e RMSE
# METRICS = ['MAPE', 'RMSE', 'MAE']  # MAPE, RMSE e MAE

# =============================================================================
# CONFIGURAÇÕES DE VARIÁVEIS
# =============================================================================
# 🔧 VARIAVEIS_FUTURAS: Selecione variáveis futuras (eventos especiais e características temporais)
# Opções disponíveis para eventos: ['black_friday', 'carnaval', 'natal', 'halloween', 
#                     'dia_do_trabalhador', 'eleicoes', 'independencia_do_brasil',
#                     'nossa_senhora_aparecida', 'pascoa', 'proclamacao_da_republica',
#                     'sexta_feira_santa', 'confraternizacao_universal', 'copa_do_mundo',
#                     'covid', 'dia_das_maes', 'dia_de_finados', 'dia_dos_namorados',
#                     'dia_dos_pais']
# Opções disponíveis para características temporais: ['dayofweek', 'monthofyear']
VARIAVEIS_FUTURAS = ['black_friday'] # Black Friday + dia da semana
# VARIAVEIS_FUTURAS = ['black_friday', 'natal', 'dayofweek', 'monthofyear']  # Múltiplas variáveis
# VARIAVEIS_FUTURAS = ['black_friday', 'carnaval', 'natal', 'halloween', 
#                      'dia_do_trabalhador', 'eleicoes', 'independencia_do_brasil',
#                      'nossa_senhora_aparecida', 'pascoa', 'proclamacao_da_republica',
#                      'sexta_feira_santa', 'confraternizacao_universal', 'copa_do_mundo',
#                      'covid', 'dia_das_maes', 'dia_de_finados', 'dia_dos_namorados',
#                      'dia_dos_pais', 'dayofweek', 'monthofyear']

# 🔧 VARIAVEIS_HISTORICAS: Selecione variáveis históricas (dados de vendas)
# Opções disponíveis: ['QLF', 'ROL', 'CPV']
VARIAVEIS_HISTORICAS = ['QLF']  # Apenas quantidade vendida
# VARIAVEIS_HISTORICAS = ['QLF', 'ROL']  # Quantidade e receita
# VARIAVEIS_HISTORICAS = ['QLF', 'ROL', 'CPV']  # Quantidade, receita e custo

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
        'encoder_bias': [True],
        'encoder_dropout': [0.0],
        'num_lr_decays': [-1],
        'early_stop_patience_steps': [-1],
        'val_check_steps': [100],
        'random_seed': [1]
    },
    'GRU': {
        'max_steps': [1],
        'learning_rate': [0.001],
        'batch_size': [64],
        'encoder_hidden_size': [50],
        'decoder_hidden_size': [50],
        'encoder_n_layers': [2],
        'decoder_layers': [2],
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

def create_all_directories():
    """Cria todos os diretórios necessários."""
    # Criar diretórios base
    for directory in [RAW_DATA_DIR, PROCESSED_DATA_DIR]:
        directory.mkdir(parents=True, exist_ok=True)
    
    # Criar diretórios para cada marca e tipo
    for marca in MARCAS:
        for tipo in TIPOS_PREVISAO:
            # Diretório de dados processados
            processed_dir = PROCESSED_DATA_DIR / marca / tipo
            processed_dir.mkdir(parents=True, exist_ok=True)
            
            # Diretório de previsões
            forecast_dir = FORECASTS_DIR / marca / tipo
            forecast_dir.mkdir(parents=True, exist_ok=True)
    
    return FORECASTS_DIR

# Criar todos os diretórios necessários
FORECASTS_DIR = create_all_directories()
