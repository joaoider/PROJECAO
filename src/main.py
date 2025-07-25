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
    MARCA, FREQ, HORIZON, VARIAVEIS_FUTURAS, VARIAVEIS_HISTORICAS, MODEL_PARAM_GRID, METRICS
)
from utils.data_processing import DataProcessor
from utils.special_dates import SpecialDates, marcar_evento_range
from utils.queries import DataQueries
from utils.metrics import calculate_metrics, save_metrics, compare_models
from models.base_model import BaseModel
from utils.save_config_vars import salvar_variaveis_csv
import os
from pyspark.sql import SparkSession
import itertools

# Importar losses do neuralforecast
try:
    from neuralforecast.losses.pytorch import MAE, MSE, RMSE, MAPE
    # Função utilitária para converter string de loss em função/classe
    LOSS_MAP = {
        'MAE': lambda: MAE(),
        'MSE': lambda: MSE(),
        'RMSE': lambda: RMSE(),
        'MAPE': lambda: MAPE(),
        # Adicione outros losses se necessário
    }
except ImportError:
    # Se não estiver disponível, defina dummies para evitar erro de import
    MAE = MSE = RMSE = MAPE = None
    LOSS_MAP = {}

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

def load_data(marca: str, tipo_previsao: str):
    """Carrega os dados do Databricks."""
    logger.info(f"Carregando dados do Databricks para marca {marca} e tipo {tipo_previsao}")
    queries = DataQueries()
    data = queries.execute_query('vendas', marca, tipo_previsao)
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
    data_neural = marcar_evento_range(data_neural, 'black_friday', special_dates.get_black_friday_dates(), days_before=1, days_after=1)

    # Marcar Carnaval com range de 3 dias antes e 2 dias depois
    data_neural = marcar_evento_range(data_neural, 'carnaval', special_dates.get_carnaval_dates(), days_before=3, days_after=2)
    
    # Marcar Confraternização Universal com range de 1 dia antes e 0 dias depois
    data_neural = marcar_evento_range(data_neural, 'confraternizacao_universal', special_dates.get_confraternizacao_universal_dates(), days_before=1, days_after=0)
    
    # Marcar Copa do Mundo com range de 0 dias antes e 0 dias depois
    data_neural = marcar_evento_range(data_neural, 'copa_do_mundo', special_dates.get_copa_do_mundo_dates(), days_before=0, days_after=0)
    
    # Marcar COVID com range de 60 dias antes e 240 dias depois
    data_neural = marcar_evento_range(data_neural, 'covid', special_dates.get_covid_dates(), days_before=60, days_after=240)
    
    # Marcar Dia das Mães com range de 7 dias antes e 1 dia depois
    data_neural = marcar_evento_range(data_neural, 'dia_das_maes', special_dates.get_dia_das_maes_dates(), days_before=7, days_after=1)
    
    # Marcar Dia de Finados com range de 0 dias antes e 0 dias depois
    data_neural = marcar_evento_range(data_neural, 'dia_de_finados', special_dates.get_dia_de_finados_dates(), days_before=0, days_after=0)
    
    # Marcar Dia dos Namorados com range de 7 dias antes e 1 dia depois
    data_neural = marcar_evento_range(data_neural, 'dia_dos_namorados', special_dates.get_dia_dos_namorados_dates(), days_before=7, days_after=1)
    
    # Marcar Dia dos Pais com range de 7 dias antes e 1 dia depois
    data_neural = marcar_evento_range(data_neural, 'dia_dos_pais', special_dates.get_dia_dos_pais_dates(), days_before=7, days_after=1)
    
    # Marcar Dia do Trabalhador com range de 0 dias antes e 0 dias depois
    data_neural = marcar_evento_range(data_neural, 'dia_do_trabalhador', special_dates.get_dia_do_trabalhador_dates(), days_before=0, days_after=0)
    
    # Marcar Eleições com range de 0 dias antes e 0 dias depois
    data_neural = marcar_evento_range(data_neural, 'eleicoes', special_dates.get_eleicoes_dates(), days_before=0, days_after=0)
    
    # Marcar Halloween com range de 1 dia antes e 1 dia depois
    data_neural = marcar_evento_range(data_neural, 'halloween', special_dates.get_halloween_dates(), days_before=1, days_after=1)
    
    # Marcar Independência do Brasil com range de 0 dias antes e 0 dias depois
    data_neural = marcar_evento_range(data_neural, 'independencia_do_brasil', special_dates.get_independencia_do_brasil_dates(), days_before=0, days_after=0)
    
    # Marcar Natal com range de 7 dias antes e 0 dias depois
    data_neural = marcar_evento_range(data_neural, 'natal', special_dates.get_natal_dates(), days_before=7, days_after=0)
    
    # Marcar Nossa Senhora Aparecida com range de 0 dias antes e 0 dias depois
    data_neural = marcar_evento_range(data_neural, 'nossa_senhora_aparecida', special_dates.get_nossa_senhora_aparecida_dates(), days_before=0, days_after=0)
    
    # Marcar Páscoa com range de 0 dias antes e 0 dias depois
    data_neural = marcar_evento_range(data_neural, 'pascoa', special_dates.get_pascoa_dates(), days_before=0, days_after=0)
    
    # Marcar Proclamação da República com range de 0 dias antes e 0 dias depois
    data_neural = marcar_evento_range(data_neural, 'proclamacao_da_republica', special_dates.get_proclamacao_da_republica_dates(), days_before=0, days_after=0)
    
    # Marcar Sexta-Feira Santa com range de 0 dias antes e 0 dias depois
    data_neural = marcar_evento_range(data_neural, 'sexta_feira_santa', special_dates.get_sexta_feira_santa_dates(), days_before=0, days_after=0)
    
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
    
    from models.model_LSTM import LSTMModel
    from models.model_GRU import GRUModel
    from models.model_NHITS import NHITSModel
    from models.model_NBEATSx import NBEATSxModel
    
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
    """Encontra o melhor modelo/configuração baseado em todas as métricas configuradas."""
    logger.info(f"Identificando melhor modelo/configuração para marca {marca} e tipo {tipo_previsao}")
    
    # Verificar quais métricas estão configuradas
    available_metrics = METRICS
    logger.info(f"Métricas configuradas para avaliação: {available_metrics}")
    
    # Calcular pontuação composta para cada modelo
    model_scores = {}
    
    for model_key, model_data in results.items():
        metrics = model_data['metrics']
        score = 0
        metric_count = 0
        
        # Calcular pontuação baseada em todas as métricas configuradas
        for metric_name in available_metrics:
            if metric_name in metrics:
                metric_value = metrics[metric_name]
                
                # Normalizar e ponderar cada métrica
                if metric_name == 'MAPE':
                    # MAPE: menor é melhor (0-100%)
                    normalized_score = max(0, 100 - metric_value) / 100
                    score += normalized_score * 0.4  # Peso maior para MAPE
                elif metric_name == 'RMSE':
                    # RMSE: menor é melhor
                    # Normalizar baseado no range típico dos dados
                    max_rmse = max([r['metrics'].get('RMSE', 0) for r in results.values()])
                    normalized_score = max(0, (max_rmse - metric_value) / max_rmse) if max_rmse > 0 else 0
                    score += normalized_score * 0.3
                elif metric_name == 'MAE':
                    # MAE: menor é melhor
                    max_mae = max([r['metrics'].get('MAE', 0) for r in results.values()])
                    normalized_score = max(0, (max_mae - metric_value) / max_mae) if max_mae > 0 else 0
                    score += normalized_score * 0.2
                elif metric_name == 'MSE':
                    # MSE: menor é melhor
                    max_mse = max([r['metrics'].get('MSE', 0) for r in results.values()])
                    normalized_score = max(0, (max_mse - metric_value) / max_mse) if max_mse > 0 else 0
                    score += normalized_score * 0.1
                
                metric_count += 1
        
        # Calcular pontuação final normalizada
        if metric_count > 0:
            final_score = score / metric_count
        else:
            final_score = 0
            
        model_scores[model_key] = {
            'score': final_score,
            'metrics': metrics,
            'params': model_data['params'],
            'model': model_data['model']
        }
        
        logger.info(f"Modelo {model_key}: Score={final_score:.4f}, Métricas={metrics}")
    
    # Selecionar o melhor modelo baseado na pontuação composta
    best_model_key = max(model_scores.keys(), key=lambda k: model_scores[k]['score'])
    best_model_data = model_scores[best_model_key]
    
    logger.info(f"🎯 MELHOR MODELO SELECIONADO:")
    logger.info(f"   Modelo: {best_model_key}")
    logger.info(f"   Score Composto: {best_model_data['score']:.4f}")
    logger.info(f"   Métricas: {best_model_data['metrics']}")
    logger.info(f"   Parâmetros: {best_model_data['params']}")
    
    # Salvar relatório detalhado de todos os modelos
    df_report = save_model_comparison_report(model_scores, marca, tipo_previsao)
    
    # Imprimir resumo completo
    print_evaluation_summary(results, model_scores, marca, tipo_previsao)
    
    # Salvar os parâmetros do melhor modelo
    best_model_data['model'].save_model(
        FORECASTS_DIR / marca / tipo_previsao / f'melhor_modelo_parametros_{best_model_key}.csv'
    )
    
    return (best_model_key, best_model_data)

def save_model_comparison_report(model_scores: dict, marca: str, tipo_previsao: str):
    """Salva um relatório detalhado de comparação de todos os modelos."""
    
    # Criar DataFrame com todos os resultados
    report_data = []
    for model_key, data in model_scores.items():
        row = {
            'Modelo': model_key,
            'Score_Composto': data['score'],
            **data['metrics']
        }
        report_data.append(row)
    
    df_report = pd.DataFrame(report_data)
    
    # Ordenar por score composto (melhor primeiro)
    df_report = df_report.sort_values('Score_Composto', ascending=False)
    
    # Salvar relatório
    report_path = FORECASTS_DIR / marca / tipo_previsao / f'relatorio_comparacao_modelos.csv'
    df_report.to_csv(report_path, index=False)
    
    logger.info(f"📊 Relatório de comparação salvo em: {report_path}")
    logger.info(f"🏆 Top 3 modelos:")
    for i, (_, row) in enumerate(df_report.head(3).iterrows()):
        logger.info(f"   {i+1}. {row['Modelo']}: Score={row['Score_Composto']:.4f}")
    
    return df_report

def print_evaluation_summary(results: dict, model_scores: dict, marca: str, tipo_previsao: str):
    """Imprime um resumo completo do processo de avaliação."""
    logger.info("=" * 80)
    logger.info(f"📋 RESUMO COMPLETO DA AVALIAÇÃO - {marca} - {tipo_previsao}")
    logger.info("=" * 80)
    
    # Estatísticas gerais
    total_models = len(results)
    total_metrics = len(METRICS)
    
    logger.info(f"🔢 ESTATÍSTICAS GERAIS:")
    logger.info(f"   • Total de modelos testados: {total_models}")
    logger.info(f"   • Total de métricas avaliadas: {total_metrics}")
    logger.info(f"   • Métricas configuradas: {METRICS}")
    logger.info(f"   • Modelos configurados: {MODELOS_A_EXECUTAR}")
    
    # Melhores resultados por métrica
    logger.info(f"\n🏅 MELHORES RESULTADOS POR MÉTRICA:")
    for metric in METRICS:
        if any(metric in r['metrics'] for r in results.values()):
            best_for_metric = min(
                results.items(),
                key=lambda x: x[1]['metrics'].get(metric, float('inf'))
            )
            logger.info(f"   • {metric}: {best_for_metric[0]} = {best_for_metric[1]['metrics'][metric]:.4f}")
    
    # Top 5 modelos por score composto
    logger.info(f"\n🏆 TOP 5 MODELOS (Score Composto):")
    sorted_models = sorted(model_scores.items(), key=lambda x: x[1]['score'], reverse=True)
    for i, (model_key, data) in enumerate(sorted_models[:5]):
        logger.info(f"   {i+1}. {model_key}: Score={data['score']:.4f}")
        for metric, value in data['metrics'].items():
            logger.info(f"      • {metric}: {value:.4f}")
    
    logger.info("=" * 80)

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
        data = load_data(marca, tipo_previsao)
        
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
        marca_para_salvar = MARCAS[0] if MARCAS else 'default'
        salvar_variaveis_csv(marca_para_salvar, FREQ, HORIZON, VARIAVEIS_FUTURAS, VARIAVEIS_HISTORICAS, DATA_INICIO_BASE)
        
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