"""
Arquivo principal que orquestra todo o fluxo de execução do projeto.
"""
import logging
from pathlib import Path
import pandas as pd
from datetime import datetime
from config.settings import (
    MARCAS, TIPOS_PREVISAO, DATA_INICIO_BASE, DATA_FINAL_BASE,
    DATA_TRAIN, DATA_TEST, DATA_INICIO_FUTR,
    DATA_FINAL_FUTR, FORECASTS_DIR, PROCESSED_DATA_DIR, MODELOS_A_EXECUTAR,
    MARCA, FREQ, HORIZON, VARIAVEIS_FUTURAS, VARIAVEIS_HISTORICAS
)
from utils.data_processing import DataProcessor
from utils.special_dates import SpecialDates
from utils.queries import DataQueries
from utils.metrics import calculate_metrics, save_metrics, compare_models
from models.base_model import BaseModel
from utils.save_config_vars import salvar_variaveis_csv

# Configuração do logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

def load_data():
    """Carrega os dados do Databricks."""
    logger.info("Carregando dados do Databricks")
    queries = DataQueries()
    data = queries.execute_query('vendas')
    logger.info(f"Dados carregados: {len(data)} registros")
    return data

def process_data(data: pd.DataFrame, marca: str, tipo_previsao: str):
    """Processa os dados iniciais para uma marca e tipo específico."""
    logger.info(f"Iniciando processamento de dados para marca {marca} e tipo {tipo_previsao}")
    
    # Inicializa o processador de dados
    processor = DataProcessor(
        marca=marca,
        tipo_previsao=tipo_previsao,
        data_inicio=DATA_INICIO_BASE,
        data_fim=DATA_FINAL_BASE
    )
    
    # Processa os dados
    data_neural = processor.process_data(data)
    
    # Verifica e completa datas faltantes
    data_neural = processor.verify_missing_dates(data_neural)
    
    # Adiciona informações de datas especiais
    special_dates = SpecialDates()
    dates_df = special_dates.get_all_dates()
    data_neural = pd.merge(
        data_neural,
        dates_df,
        left_on='ds',
        right_on='data',
        how='left'
    )
    
    # Salva os dados processados
    processor.save_processed_data(
        data_neural,
        PROCESSED_DATA_DIR / marca / tipo_previsao
    )
    
    logger.info(f"Processamento de dados concluído para marca {marca} e tipo {tipo_previsao}")
    return data_neural

def train_and_evaluate_models(data_neural: pd.DataFrame, marca: str, tipo_previsao: str):
    """Treina e avalia todos os modelos para uma marca e tipo específico."""
    logger.info(f"Iniciando treinamento e avaliação dos modelos para marca {marca} e tipo {tipo_previsao}")
    
    # Importa os modelos
    from models.lstm_model import LSTMModel
    from models.gru_model import GRUModel
    from models.nhits_model import NHITSModel
    from models.nbeatsx_model import NBEATSxModel
    
    model_classes = {
        'LSTM': LSTMModel,
        'GRU': GRUModel,
        'NHITS': NHITSModel,
        'NBEATSx': NBEATSxModel
    }
    
    # Lista de modelos para treinar conforme configuração
    models = [model_classes[nome] for nome in MODELOS_A_EXECUTAR if nome in model_classes]
    
    results = {}
    
    # Treina e avalia cada modelo
    for model_class in models:
        logger.info(f"Treinando modelo {model_class.__name__} para marca {marca} e tipo {tipo_previsao}")
        model = model_class()
        
        # Treina o modelo
        model.fit(data_neural)
        
        # Faz previsões
        predictions = model.predict(data_neural)
        
        # Avalia o modelo
        metrics = calculate_metrics(
            data_neural['y'],
            predictions['y_pred']
        )
        
        results[model_class.__name__] = {
            'model': model,
            'metrics': metrics
        }
        
        # Salva as métricas
        save_metrics(
            metrics,
            model_class.__name__,
            marca,
            str(FORECASTS_DIR / marca / tipo_previsao)
        )
    
    logger.info(f"Treinamento e avaliação dos modelos concluído para marca {marca} e tipo {tipo_previsao}")
    return results

def find_best_model(results: dict, marca: str, tipo_previsao: str):
    """Encontra o melhor modelo baseado nas métricas para uma marca e tipo específico."""
    logger.info(f"Identificando melhor modelo para marca {marca} e tipo {tipo_previsao}")
    
    # Compara os modelos usando MAPE
    best_model = min(
        results.items(),
        key=lambda x: x[1]['metrics']['MAPE']
    )
    
    logger.info(f"Melhor modelo para marca {marca} e tipo {tipo_previsao}: {best_model[0]} com MAPE: {best_model[1]['metrics']['MAPE']:.2f}%")
    
    # Salva os parâmetros do melhor modelo
    best_model[1]['model'].save_model(
        FORECASTS_DIR / marca / tipo_previsao / f'melhor_modelo_parametros_{best_model[0]}.csv'
    )
    
    return best_model

def run_best_model(best_model: tuple, data_neural: pd.DataFrame, marca: str, tipo_previsao: str):
    """Executa o melhor modelo para fazer previsões finais para uma marca e tipo específico."""
    logger.info(f"Executando melhor modelo para previsões finais de marca {marca} e tipo {tipo_previsao}")
    
    # Faz previsões com o melhor modelo
    predictions = best_model[1]['model'].predict(data_neural)
    
    # Salva as previsões
    predictions.to_csv(
        FORECASTS_DIR / marca / tipo_previsao / f'previsoes_finais_{best_model[0]}.csv',
        index=False
    )
    
    logger.info(f"Previsões finais salvas com sucesso para marca {marca} e tipo {tipo_previsao}")

def process_marca_tipo(marca: str, tipo_previsao: str):
    """Processa uma combinação específica de marca e tipo."""
    try:
        logger.info(f"Iniciando processamento para marca {marca} e tipo {tipo_previsao}")
        
        # Carrega os dados
        data = load_data()
        
        # Processa os dados
        data_neural = process_data(data, marca, tipo_previsao)
        
        # Treina e avalia os modelos
        results = train_and_evaluate_models(data_neural, marca, tipo_previsao)
        
        # Encontra o melhor modelo
        best_model = find_best_model(results, marca, tipo_previsao)
        
        # Executa o melhor modelo
        run_best_model(best_model, data_neural, marca, tipo_previsao)
        
        logger.info(f"Processamento concluído com sucesso para marca {marca} e tipo {tipo_previsao}")
        
    except Exception as e:
        logger.error(f"Erro durante o processamento de marca {marca} e tipo {tipo_previsao}: {e}")
        raise

def main():
    """Função principal que orquestra todo o fluxo."""
    try:
        logger.info("Iniciando execução do pipeline")

        # Salvar variáveis de configuração
        # Ajuste aqui para passar as listas corretas de variáveis futuras e históricas
        salvar_variaveis_csv(MARCA, FREQ, HORIZON, VARIAVEIS_FUTURAS, VARIAVEIS_HISTORICAS, DATA_INICIO_BASE)
        
        # Processa cada combinação de marca e tipo
        for marca in MARCAS:
            for tipo_previsao in TIPOS_PREVISAO:
                process_marca_tipo(marca, tipo_previsao)
        
        logger.info("Pipeline executado com sucesso para todas as marcas e tipos")
        
    except Exception as e:
        logger.error(f"Erro durante a execução do pipeline: {e}")
        raise

if __name__ == "__main__":
    main()