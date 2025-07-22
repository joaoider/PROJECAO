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
    MARCA, FREQ, HORIZON, VARIAVEIS_FUTURAS, VARIAVEIS_HISTORICAS, MODEL_PARAM_GRID
)
from utils.data_processing import DataProcessor
from utils.special_dates import SpecialDates, marcar_evento_range
from utils.queries import DataQueries
from utils.metrics import calculate_metrics, save_metrics, compare_models
from models.base_model import BaseModel
from utils.save_config_vars import salvar_variaveis_csv
import os
import pandas as pd
from pyspark.sql import SparkSession
import itertools

# Função utilitária para converter string de loss em função/classe
LOSS_MAP = {
    'MAE': lambda: MAE(),
    'MSE': lambda: MSE(),
    'RMSE': lambda: RMSE(),
    'MAPE': lambda: MAPE(),
    # Adicione outros losses se necessário
}
try:
    from neuralforecast.losses.pytorch import MAE, MSE, RMSE, MAPE
except ImportError:
    # Se não estiver disponível, defina dummies para evitar erro de import
    MAE = MSE = RMSE = MAPE = None

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

    # Marcar Black Friday com range de 1 dia antes e 1 dia depois
    black_friday_dates = [
        '2013-11-29', '2014-11-28', '2015-11-27', '2016-11-25', '2017-11-24',
        '2018-11-23', '2019-11-29', '2020-11-27', '2021-11-26', '2022-11-25',
        '2023-11-24', '2024-11-29', '2025-11-28', '2026-11-28'
    ]
    data_neural = marcar_evento_range(data_neural, 'black_friday', black_friday_dates, days_before=1, days_after=1)

    # Marcar Carnaval com range de 3 dias antes e 2 dias depois
    carnaval_dates = [
        '2013-02-11', '2014-03-03', '2015-02-16', '2016-02-08', '2017-02-27',
        '2018-02-12', '2019-03-04', '2020-02-24', '2021-02-15', '2022-02-28',
        '2023-02-20', '2024-02-12', '2025-03-04', '2026-02-17'
    ]
    data_neural = marcar_evento_range(data_neural, 'carnaval', carnaval_dates, days_before=3, days_after=2)
    
    # Marcar Confraternização Universal com range de 1 dia antes e 0 dias depois
    confraternizacao_universal_dates = [
        '2013-01-01', '2014-01-01', '2015-01-01', '2016-01-01', '2017-01-01',
        '2018-01-01', '2019-01-01', '2020-01-01', '2021-01-01', '2022-01-01',
        '2023-01-01', '2024-01-01', '2025-01-01', '2026-01-01'
    ]
    data_neural = marcar_evento_range(data_neural, 'confraternizacao_universal', confraternizacao_universal_dates, days_before=1, days_after=0)
    
    # Marcar Copa do Mundo com range de 0 dias antes e 0 dias depois
    copa_do_mundo_dates = [
        '2014-06-12', '2014-06-17', '2014-06-23', '2014-06-28', '2014-07-04',
        '2014-07-08', '2014-07-12', '2018-06-14', '2018-06-17', '2018-06-22',
        '2018-07-02', '2018-07-06', '2022-11-20', '2022-11-24', '2022-11-28',
        '2022-12-02', '2022-12-05', '2022-12-09', '2026-07-11'
    ]
    data_neural = marcar_evento_range(data_neural, 'copa_do_mundo', copa_do_mundo_dates, days_before=0, days_after=0)
    
    # Marcar COVID com range de 60 dias antes e 240 dias depois
    covid_dates = [
        '2020-03-01'
    ]
    data_neural = marcar_evento_range(data_neural, 'covid', covid_dates, days_before=60, days_after=240)
    
    # Marcar Dia das Mães com range de 7 dias antes e 1 dia depois
    dia_das_maes_dates = [
        '2013-05-12', '2014-05-11', '2015-05-10', '2016-05-08', '2017-05-14',
        '2018-05-13', '2019-05-12', '2020-05-10', '2021-05-09', '2022-05-08',
        '2023-05-14', '2024-05-12', '2025-05-11', '2026-05-10'
    ]
    data_neural = marcar_evento_range(data_neural, 'dia_das_maes', dia_das_maes_dates, days_before=7, days_after=1)
    
    # Marcar Dia de Finados com range de 0 dias antes e 0 dias depois
    dia_de_finados_dates = [
        '2013-11-02', '2014-11-02', '2015-11-02', '2016-11-02', '2017-11-02',
        '2018-11-02', '2019-11-02', '2020-11-02', '2021-11-02', '2022-11-02',
        '2023-11-02', '2024-11-02', '2025-11-02', '2026-11-02'
    ]
    data_neural = marcar_evento_range(data_neural, 'dia_de_finados', dia_de_finados_dates, days_before=0, days_after=0)
    
    # Marcar Dia dos Namorados com range de 7 dias antes e 1 dia depois
    dia_dos_namorados_dates = [
        '2013-06-12', '2014-06-12', '2015-06-12', '2016-06-12', '2017-06-12',
        '2018-06-12', '2019-06-12', '2020-06-12', '2021-06-12', '2022-06-12',
        '2023-06-12', '2024-06-12', '2025-06-12', '2026-06-12'
    ]
    data_neural = marcar_evento_range(data_neural, 'dia_dos_namorados', dia_dos_namorados_dates, days_before=7, days_after=1)
    
    # Marcar Dia dos Pais com range de 7 dias antes e 1 dia depois
    dia_dos_pais_dates = [
        '2013-08-11', '2014-08-10', '2015-08-09', '2016-08-14', '2017-08-13',
        '2018-08-12', '2019-08-11', '2020-08-09', '2021-08-08', '2022-08-14',
        '2023-08-13', '2024-08-11', '2025-08-10', '2026-08-09'
    ]
    data_neural = marcar_evento_range(data_neural, 'dia_dos_pais', dia_dos_pais_dates, days_before=7, days_after=1)
    
    # Marcar Dia do Trabalhador com range de 0 dias antes e 0 dias depois
    dia_do_trabalhador_dates = [
        '2013-05-01', '2014-05-01', '2015-05-01', '2016-05-01', '2017-05-01',
        '2018-05-01', '2019-05-01', '2020-05-01', '2021-05-01', '2022-05-01',
        '2023-05-01', '2024-05-01', '2025-05-01', '2026-05-01'
    ]
    data_neural = marcar_evento_range(data_neural, 'dia_do_trabalhador', dia_do_trabalhador_dates, days_before=0, days_after=0)
    
    # Marcar Eleições com range de 0 dias antes e 0 dias depois
    eleicoes_dates = [
        '2018-10-07', '2018-10-28', '2022-10-02', '2022-10-30', '2024-10-06', '2024-10-27', '2026-10-04', '2026-10-25'
    ]
    data_neural = marcar_evento_range(data_neural, 'eleicoes', eleicoes_dates, days_before=0, days_after=0)
    
    # Marcar Halloween com range de 1 dia antes e 1 dia depois
    halloween_dates = [
        '2013-10-31', '2014-10-31', '2015-10-31', '2016-10-31', '2017-10-31',
        '2018-10-31', '2019-10-31', '2020-10-31', '2021-10-31', '2022-10-31',
        '2023-10-31', '2024-10-31', '2025-10-31', '2026-10-31'
    ]
    data_neural = marcar_evento_range(data_neural, 'halloween', halloween_dates, days_before=1, days_after=1)
    
    # Marcar Independência do Brasil com range de 0 dias antes e 0 dias depois
    independencia_do_brasil_dates = [
        '2013-09-07', '2014-09-07', '2015-09-07', '2016-09-07', '2017-09-07',
        '2018-09-07', '2019-09-07', '2020-09-07', '2021-09-07', '2022-09-07',
        '2023-09-07', '2024-09-07', '2025-09-07', '2026-09-07'
    ]
    data_neural = marcar_evento_range(data_neural, 'independencia_do_brasil', independencia_do_brasil_dates, days_before=0, days_after=0)
    
    # Marcar Natal com range de 7 dias antes e 0 dias depois
    natal_dates = [
        '2013-12-25', '2014-12-25', '2015-12-25', '2016-12-25', '2017-12-25',
        '2018-12-25', '2019-12-25', '2020-12-25', '2021-12-25', '2022-12-25',
        '2023-12-25', '2024-12-25', '2025-12-25', '2026-12-25'
    ]
    data_neural = marcar_evento_range(data_neural, 'natal', natal_dates, days_before=7, days_after=0)
    
    # Marcar Nossa Senhora Aparecida com range de 0 dias antes e 0 dias depois
    nossa_senhora_aparecida_dates = [
        '2013-10-12', '2014-10-12', '2015-10-12', '2016-10-12', '2017-10-12',
        '2018-10-12', '2019-10-12', '2020-10-12', '2021-10-12', '2022-10-12',
        '2023-10-12', '2024-10-12', '2025-10-12', '2026-10-12'
    ]
    data_neural = marcar_evento_range(data_neural, 'nossa_senhora_aparecida', nossa_senhora_aparecida_dates, days_before=0, days_after=0)
    
    # Marcar Páscoa com range de 0 dias antes e 0 dias depois
    pascoa_dates = [
        '2013-03-31', '2014-04-20', '2015-04-05', '2016-03-27', '2017-04-16',
        '2018-04-01', '2019-04-21', '2020-04-12', '2021-04-04', '2022-04-17',
        '2023-04-09', '2024-03-31', '2025-04-20', '2026-04-05'
    ]
    data_neural = marcar_evento_range(data_neural, 'pascoa', pascoa_dates, days_before=0, days_after=0)
    
    # Marcar Proclamação da República com range de 0 dias antes e 0 dias depois
    proclamacao_da_republica_dates = [
        '2013-11-15', '2014-11-15', '2015-11-15', '2016-11-15', '2017-11-15',
        '2018-11-15', '2019-11-15', '2020-11-15', '2021-11-15', '2022-11-15',
        '2023-11-15', '2024-11-15', '2025-11-15', '2026-11-15'
    ]
    data_neural = marcar_evento_range(data_neural, 'proclamacao_da_republica', proclamacao_da_republica_dates, days_before=0, days_after=0)
    
    # Adicionar coluna com o dia da semana (0=Monday, ..., 6=Sunday)
    data_neural['dia_da_semana'] = pd.to_datetime(data_neural['ds']).dt.day_name()
    day_mapping = {
        'Monday': 0,
        'Tuesday': 1,
        'Wednesday': 2,
        'Thursday': 3,
        'Friday': 4,
        'Saturday': 5,
        'Sunday': 6
    }
    data_neural['dayofweek'] = data_neural['dia_da_semana'].map(day_mapping)
    data_neural = data_neural.drop(columns=['dia_da_semana'])
    
    # Adicionar coluna com o mês do ano (1=Janeiro, ..., 12=Dezembro)
    from utils.special_dates import process_mes_do_ano
    data_neural = process_mes_do_ano(data_neural)
    
    # Salva os dados processados
    processor.save_processed_data(
        data_neural,
        PROCESSED_DATA_DIR / marca / tipo_previsao
    )
    
    logger.info(f"Processamento de dados concluído para marca {marca} e tipo {tipo_previsao}")
    return data_neural

def train_and_evaluate_models(data_neural: pd.DataFrame, marca: str, tipo_previsao: str):
    """Treina e avalia todos os modelos para uma marca e tipo específico, realizando grid search."""
    logger.info(f"Iniciando treinamento e avaliação dos modelos para marca {marca} e tipo {tipo_previsao}")
    
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
    
    results = {}
    # Para cada modelo selecionado
    for model_name in MODELOS_A_EXECUTAR:
        if model_name not in model_classes:
            continue
        ModelClass = model_classes[model_name]
        param_grid = MODEL_PARAM_GRID.get(model_name, {})
        # Gerar todas as combinações possíveis do grid
        keys, values = zip(*param_grid.items()) if param_grid else ([], [])
        for param_values in itertools.product(*values):
            params = dict(zip(keys, param_values))
            # Converter 'loss' de string para função/classe se necessário
            if model_name == 'GRU' and 'loss' in params and isinstance(params['loss'], str):
                if params['loss'] in LOSS_MAP:
                    params['loss'] = LOSS_MAP[params['loss']]()
            logger.info(f"Treinando {model_name} com params: {params}")
            # Instanciar o modelo com os parâmetros do grid
            model = ModelClass(**params) if params else ModelClass()
            # Treinar e avaliar
            model.fit(data_neural)
            predictions = model.predict(data_neural)
            metrics = calculate_metrics(
                data_neural['y'],
                predictions['y_pred']
            )
            # Chave única para cada combinação
            result_key = f"{model_name}_{'_'.join([str(v) for v in param_values])}" if param_values else model_name
            results[result_key] = {
                'model': model,
                'metrics': metrics,
                'params': params
            }
            # Salvar as métricas
            save_metrics(
                metrics,
                result_key,
                marca,
                str(FORECASTS_DIR / marca / tipo_previsao)
            )
    logger.info(f"Treinamento e avaliação dos modelos concluído para marca {marca} e tipo {tipo_previsao}")
    return results

def find_best_model(results: dict, marca: str, tipo_previsao: str):
    """Encontra o melhor modelo/configuração baseado nas métricas para uma marca e tipo específico."""
    logger.info(f"Identificando melhor modelo/configuração para marca {marca} e tipo {tipo_previsao}")
    # Compara os modelos/configurações usando MAPE
    best_model = min(
        results.items(),
        key=lambda x: x[1]['metrics']['MAPE']
    )
    logger.info(f"Melhor modelo/configuração para marca {marca} e tipo {tipo_previsao}: {best_model[0]} com MAPE: {best_model[1]['metrics']['MAPE']:.2f}% e params: {best_model[1]['params']}")
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
    
    # Salva as previsões em CSV
    csv_path = FORECASTS_DIR / marca / tipo_previsao / f'previsoes_finais_{best_model[0]}.csv'
    predictions.to_csv(csv_path, index=False)
    logger.info(f"Previsões finais salvas com sucesso para marca {marca} e tipo {tipo_previsao}")

    # Salva as previsões em Parquet usando Spark
    try:
        spark = SparkSession.builder.appName("pandas_to_spark").getOrCreate()
        logger.info(f"Convertendo CSV para Parquet usando Spark: {csv_path}")
        df_pandas = pd.read_csv(csv_path)
        sparkdf = spark.createDataFrame(df_pandas)
        parquet_path = str(FORECASTS_DIR / marca / tipo_previsao / f'previsoes_finais_{best_model[0]}.parquet')
        sparkdf.coalesce(1).write.mode('overwrite').parquet(parquet_path)
        logger.info(f"Parquet salvo com sucesso em {parquet_path}")
    except Exception as e:
        logger.error(f"Erro ao salvar Parquet: {e}")

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