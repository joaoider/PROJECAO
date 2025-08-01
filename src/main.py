"""
Arquivo principal que orquestra todo o fluxo de execução do projeto.
"""
import logging
from pathlib import Path
import pandas as pd
from datetime import datetime, timedelta
import calendar
from config.settings import (
    MARCAS, TIPOS_PREVISAO, DATA_INICIO_BASE, DATA_FINAL_BASE,
    DATA_TRAIN, DATA_TEST, DATA_INICIO_FUTR,
    DATA_FINAL_FUTR, FORECASTS_DIR, PROCESSED_DATA_DIR, MODELOS_A_EXECUTAR,
    MARCA, FREQ, HORIZON, VARIAVEIS_FUTURAS, VARIAVEIS_HISTORICAS, MODEL_PARAM_GRID, METRICS,
    DATA_ATUAL
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

# Importar dbutils para operações no Azure Blob Storage
try:
    from pyspark.dbutils import DBUtils
    dbutils = DBUtils(SparkSession.builder.getOrCreate())
except ImportError:
    # Fallback para ambiente local
    dbutils = None

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

def load_data(marca: str, tipo_previsao: str, data_fim: str = None):
    """Carrega os dados do Databricks."""
    logger.info(f"Carregando dados do Databricks para marca {marca} e tipo {tipo_previsao}")
    if data_fim:
        logger.info(f"Limitando dados até {data_fim}")
    queries = DataQueries()
    data = queries.execute_query('vendas', marca, tipo_previsao, data_fim)
    logger.info(f"Dados carregados: {len(data)} registros")
    return data

def process_data(data: pd.DataFrame, marca: str, tipo_previsao: str, data_fim: str = None):
    """Processa os dados iniciais para uma marca e tipo específico."""
    # Usar data_fim fornecida ou DATA_FINAL_BASE padrão
    data_fim_processamento = data_fim if data_fim else DATA_FINAL_BASE
    
    logger.info(f"Iniciando processamento de dados para marca {marca} e tipo {tipo_previsao}")
    logger.info(f"Período dos dados: {DATA_INICIO_BASE} até {data_fim_processamento}")
    
    # Inicializa o processador de dados
    processor = DataProcessor(
        marca=marca,
        data_inicio=DATA_INICIO_BASE,
        data_fim=data_fim_processamento
    )
    
    # Processa os dados
    data_neural = processor.process_data(data)
    
    # Verifica e completa datas faltantes
    data_neural = processor.verify_missing_dates(data_neural)
    
    # Adiciona informações de datas especiais
    special_dates = SpecialDates()
    dates_df = special_dates.get_all_dates()
    
    # Fazer merge e preencher valores nulos
    data_neural = pd.merge(
        data_neural,
        dates_df,
        left_on='ds',
        right_on='data',
        how='left'
    )
    
    # Remover colunas de eventos que não são necessárias para o modelo
    # (elas são usadas apenas para marcar eventos específicos)
    if 'data' in data_neural.columns:
        data_neural = data_neural.drop(columns=['data'])
    if 'tipo' in data_neural.columns:
        data_neural = data_neural.drop(columns=['tipo'])
    if 'evento' in data_neural.columns:
        data_neural = data_neural.drop(columns=['evento'])

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
    logger.info(f"Período de treinamento: até {DATA_TRAIN}")
    logger.info(f"Período de teste: {DATA_TEST} até {DATA_ATUAL.strftime('%Y-%m-%d')}")
    logger.info(f"Período de previsões futuras: {DATA_INICIO_FUTR} até {DATA_FINAL_FUTR}")
    
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
            
            # Fazer previsões apenas para o período futuro (não para todos os dados históricos)
            future_start = pd.to_datetime(DATA_INICIO_FUTR)
            future_end = pd.to_datetime(DATA_FINAL_FUTR)
            
            # Criar range de datas futuras
            future_dates = pd.date_range(start=future_start, end=future_end, freq='D')
            
            # Obter unique_ids dos dados
            unique_ids = data_neural['unique_id'].unique()
            
            # Criar DataFrame apenas com datas futuras para previsão
            future_data = pd.DataFrame([
                {'ds': date, 'unique_id': uid}
                for date in future_dates
                for uid in unique_ids
            ])
            
            # Fazer previsões apenas para o período futuro
            predictions = model.predict(future_data, start_date=DATA_INICIO_FUTR, end_date=DATA_FINAL_FUTR)
            
            # Verificar a estrutura das previsões e extrair y_pred
            logger.info(f"Estrutura das previsões: {predictions.columns.tolist()}")
            
            # NeuralForecast retorna previsões com colunas específicas
            # Procurar por coluna de previsão (geralmente termina com _LSTM, _GRU, etc.)
            y_pred_col = None
            for col in predictions.columns:
                if col != 'ds' and col != 'unique_id' and not col.startswith('y'):
                    y_pred_col = col
                    break
            
            if y_pred_col is None:
                logger.error(f"Nenhuma coluna de previsão encontrada. Colunas disponíveis: {predictions.columns.tolist()}")
                continue
                
            logger.info(f"Usando coluna de previsão: {y_pred_col}")
            
            # Calcular métricas usando dados de teste (período de validação)
            # Filtrar dados para o período de teste (último ano até hoje)
            data_test = data_neural[
                (data_neural['ds'] >= pd.to_datetime(DATA_TEST)) & 
                (data_neural['ds'] <= pd.to_datetime(DATA_ATUAL.strftime('%Y-%m-%d')))
            ]
            
            if len(data_test) > 0:
                # Para o período de teste, queremos as previsões do modelo treinado
                # sobre os dados reais (não previsões de dados históricos)
                # Criar DataFrame apenas com o período de teste para previsão
                test_start = pd.to_datetime(DATA_TEST)
                test_end = pd.to_datetime(DATA_ATUAL.strftime('%Y-%m-%d'))
                
                # Criar range de datas de teste
                test_dates = pd.date_range(start=test_start, end=test_end, freq='D')
                
                # Obter unique_ids dos dados
                unique_ids = data_neural['unique_id'].unique()
                
                # Criar DataFrame apenas com datas de teste para previsão
                test_data = pd.DataFrame([
                    {'ds': date, 'unique_id': uid}
                    for date in test_dates
                    for uid in unique_ids
                ])
                
                # Fazer previsões para o período de teste
                test_predictions = model.predict(test_data, start_date=DATA_TEST, end_date=DATA_ATUAL.strftime('%Y-%m-%d'))
                
                # Calcular métricas usando dados reais vs previsões
                metrics = calculate_metrics(
                    data_test['y'],
                    test_predictions[y_pred_col]
                )
                
                # Salvar previsões de teste para uso posterior
                test_predictions_clean = test_predictions[['ds', 'unique_id', y_pred_col]].copy()
                test_predictions_clean = test_predictions_clean.rename(columns={y_pred_col: 'y_pred'})
            else:
                logger.warning("Período de teste vazio. Usando dados completos para métricas.")
                metrics = calculate_metrics(
                    data_neural['y'],
                    predictions[y_pred_col]
                )
                test_predictions_clean = None
            
            # Chave única para cada combinação
            result_key = f"{model_name}_{'_'.join([str(v) for v in param_values])}" if param_values else model_name
            results[result_key] = {
                'model': model,
                'metrics': metrics,
                'params': params,
                'test_predictions': test_predictions_clean
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
    
    # Salvar parâmetros do melhor modelo na pasta com data
    data_atual = datetime.now().strftime('%Y%m')
    pasta_data = FORECASTS_DIR / marca / tipo_previsao / data_atual
    pasta_data.mkdir(parents=True, exist_ok=True)
    
    best_model_data['model'].save_model(
        pasta_data / f'melhor_modelo_parametros_{best_model_key}.csv'
    )
    
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
    
    # Criar pasta com data atual para organizar os arquivos
    data_atual = datetime.now().strftime('%Y%m')
    pasta_data = FORECASTS_DIR / marca / tipo_previsao / data_atual
    pasta_data.mkdir(parents=True, exist_ok=True)
    
    # Salvar relatório
    report_path = pasta_data / f'relatorio_comparacao_modelos.csv'
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

def run_best_model(best_model: tuple, data_neural: pd.DataFrame, marca: str, tipo_previsao: str, results: dict = None, reference_date: datetime = None):
    """Executa o melhor modelo para fazer previsões finais para uma marca e tipo específico."""
    logger.info(f"Executando melhor modelo para previsões finais de marca {marca} e tipo {tipo_previsao}")
    logger.info(f"Gerando previsões para o período: {DATA_INICIO_FUTR} até {DATA_FINAL_FUTR}")
    
    # Faz previsões apenas para o período futuro com o melhor modelo
    # Criar dados apenas para o período futuro
    future_start = pd.to_datetime(DATA_INICIO_FUTR)
    future_end = pd.to_datetime(DATA_FINAL_FUTR)
    
    # Criar range de datas futuras
    future_dates = pd.date_range(start=future_start, end=future_end, freq='D')
    
    # Obter unique_ids dos dados
    unique_ids = data_neural['unique_id'].unique()
    
    # Criar DataFrame apenas com datas futuras para previsão
    future_data = pd.DataFrame([
        {'ds': date, 'unique_id': uid}
        for date in future_dates
        for uid in unique_ids
    ])
    
    # Fazer previsões apenas para o período futuro
    predictions = best_model[1]['model'].predict(future_data, start_date=DATA_INICIO_FUTR, end_date=DATA_FINAL_FUTR)
    
    # Criar pasta com data de referência para organizar os arquivos
    if reference_date:
        data_ref = reference_date.strftime('%Y%m')
        pasta_data = FORECASTS_DIR / marca / tipo_previsao / data_ref
    else:
        data_atual = datetime.now().strftime('%Y%m')
        pasta_data = FORECASTS_DIR / marca / tipo_previsao / data_atual
    
    pasta_data.mkdir(parents=True, exist_ok=True)
    logger.info(f"Pasta criada: {pasta_data}")
    
    # Obter dados reais de treino (1 ano antes da data de referência)
    train_start = reference_date - timedelta(days=365) if reference_date else pd.to_datetime(DATA_TRAIN)
    train_end = reference_date if reference_date else pd.to_datetime(DATA_ATUAL.strftime('%Y-%m-%d'))
    
    # Filtrar dados de treino reais
    dados_treino = data_neural[
        (data_neural['ds'] >= train_start) & 
        (data_neural['ds'] < train_end)
    ].copy()
    
    # Renomear coluna 'y' para 'y_pred' nos dados de treino para manter consistência
    dados_treino = dados_treino.rename(columns={'y': 'y_pred'})
    
    logger.info(f"Dados de treino obtidos: {len(dados_treino)} registros")
    logger.info(f"Período de treino: {dados_treino['ds'].min()} a {dados_treino['ds'].max()}")
    
    # Juntar dados de treino reais com previsões futuras
    serie_completa = pd.concat([dados_treino, predictions], ignore_index=True)
    serie_completa = serie_completa.sort_values('ds').reset_index(drop=True)
    
    logger.info(f"Série completa criada: {len(serie_completa)} registros")
    logger.info(f"Período completo: {serie_completa['ds'].min()} a {serie_completa['ds'].max()}")
    
    # Salvar série completa
    csv_path_completa = pasta_data / f'serie_completa_{best_model[0]}.csv'
    serie_completa.to_csv(csv_path_completa, index=False)
    logger.info(f"Série completa salva em: {csv_path_completa}")
    
    # Salvar série completa em Parquet
    try:
        spark = SparkSession.builder.appName("pandas_to_spark").getOrCreate()
        sparkdf_completa = spark.createDataFrame(serie_completa)
        parquet_path_completa = str(pasta_data / f'serie_completa_{best_model[0]}.parquet')
        sparkdf_completa.coalesce(1).write.mode('overwrite').parquet(parquet_path_completa)
        logger.info(f"Série completa Parquet salva em: {parquet_path_completa}")
    except Exception as e:
        logger.error(f"Erro ao salvar série completa Parquet: {e}")
    
    # Usar série completa para salvamento final
    predictions_final = serie_completa
    
    # Salva as previsões finais em CSV
    csv_path = pasta_data / f'previsoes_finais_{best_model[0]}.csv'
    predictions_final.to_csv(csv_path, index=False)
    logger.info(f"Previsões finais salvas com sucesso para marca {marca} e tipo {tipo_previsao}")

    # Salva as previsões em Parquet usando Spark (local)
    try:
        spark = SparkSession.builder.appName("pandas_to_spark").getOrCreate()
        logger.info(f"Convertendo CSV para Parquet usando Spark: {csv_path}")
        df_pandas = pd.read_csv(csv_path)
        sparkdf = spark.createDataFrame(df_pandas)
        parquet_path = str(pasta_data / f'previsoes_finais_{best_model[0]}.parquet')
        sparkdf.coalesce(1).write.mode('overwrite').parquet(parquet_path)
        logger.info(f"Parquet salvo com sucesso em {parquet_path}")
    except Exception as e:
        logger.error(f"Erro ao salvar Parquet local: {e}")

    # Salva as previsões em Parquet no Azure Blob Storage
    try:
        salvar_em_parquet_azure(predictions_final, marca, tipo_previsao, reference_date=reference_date)
        logger.info(f"Parquet salvo com sucesso no Azure Blob Storage para marca {marca} e tipo {tipo_previsao}")
    except Exception as e:
        logger.error(f"Erro ao salvar Parquet no Azure: {e}")

def salvar_em_parquet_azure(df_pandas, marca: str, tipo_previsao: str, 
                           blob_path="/mnt/analytics/planejamento/datascience/forecast_marca/",
                           reference_date: datetime = None):
    """
    Salva o DataFrame em parquet no Azure Blob Storage.
    
    Args:
        df_pandas: DataFrame pandas com as previsões
        marca: Nome da marca
        tipo_previsao: Tipo de previsão
        blob_path: Caminho do blob storage
        reference_date: Data de referência para nomear o arquivo
    """
    try:
        # Verificar se dbutils está disponível
        if dbutils is None:
            logger.warning("dbutils não disponível. Pulando salvamento no Azure Blob Storage.")
            return
            
        spark = SparkSession.builder.appName("pandas_to_spark").getOrCreate()
        logger.info('Convertendo para Spark DataFrame.')
        
        sparkdf = spark.createDataFrame(df_pandas)

        # Usar data de referência se fornecida, senão usar data atual
        if reference_date:
            data_ref = reference_date.strftime('%Y%m')
        else:
            data_ref = datetime.now().strftime('%Y%m')

        # Diretório temporário para cada execução
        temp_blob_path = f"{blob_path}/temp_{marca}_{tipo_previsao}_{data_ref}"

        # Salvar o arquivo parquet temporariamente
        logger.info('Salvando parquet em diretório temporário.')
        (sparkdf
         .coalesce(1)
         .write
         .mode('overwrite')
         .format('parquet')
         .save(temp_blob_path)
        )

        # Nome desejado do arquivo final
        nome_final = f"{marca}_{tipo_previsao}_{data_ref}.parquet"

        # Obter o nome do arquivo Parquet gerado
        parquet_name = [x.name for x in dbutils.fs.ls(temp_blob_path) if x.name.startswith("part")][0]

        # Mover o arquivo parquet gerado para o diretório definitivo com o nome desejado
        dbutils.fs.mv(f"{temp_blob_path}/{parquet_name}", f"{blob_path}/{nome_final}")

        # Remover o diretório temporário usado
        dbutils.fs.rm(temp_blob_path, recurse=True)

        logger.info(f"Parquet salvo com sucesso no Azure: {blob_path}/{nome_final}")
        
    except Exception as e:
        logger.error(f"Erro ao salvar parquet no Azure: {e}")
        raise

def generate_reference_dates():
    """
    Gera lista de datas de referência desde 2024-01-01 até a data atual.
    Cada data representa o último dia do mês anterior.
    """
    
    start_date = datetime(2024, 1, 1)
    end_date = datetime.now()
    
    reference_dates = []
    current_date = start_date
    
    while current_date <= end_date:
        # Calcular o último dia do mês anterior
        if current_date.month == 1:
            # Janeiro: usar último dia de dezembro do ano anterior
            last_month = datetime(current_date.year - 1, 12, 31)
        else:
            # Outros meses: usar último dia do mês anterior
            last_day_prev_month = calendar.monthrange(current_date.year, current_date.month - 1)[1]
            last_month = datetime(current_date.year, current_date.month - 1, last_day_prev_month)
        
        reference_dates.append(last_month)
        
        # Avançar para o próximo mês
        if current_date.month == 12:
            current_date = datetime(current_date.year + 1, 1, 1)
        else:
            current_date = datetime(current_date.year, current_date.month + 1, 1)
    
    return reference_dates

def process_marca_tipo_with_date(marca: str, tipo_previsao: str, reference_date: datetime):
    """Processa uma combinação específica de marca e tipo para uma data de referência."""
    try:
        logger.info(f"Iniciando processamento para marca {marca}, tipo {tipo_previsao} e data de referência {reference_date.strftime('%Y-%m-%d')}")
        
        # Atualizar configurações de data para esta execução
        global DATA_ATUAL, DATA_TRAIN, DATA_TEST, DATA_INICIO_FUTR, DATA_FINAL_FUTR
        
        # Salvar configurações originais
        original_data_atual = DATA_ATUAL
        original_data_train = DATA_TRAIN
        original_data_test = DATA_TEST
        original_data_inicio_futr = DATA_INICIO_FUTR
        original_data_final_futr = DATA_FINAL_FUTR
        
        try:
            # Atualizar configurações para a data de referência
            # DATA_ATUAL = data de referência (último dia do mês anterior)
            DATA_ATUAL = reference_date
            
            # DATA_TRAIN = até 1 ano antes da data de referência
            DATA_TRAIN = (reference_date - timedelta(days=365)).strftime('%Y-%m-%d')
            
            # DATA_TEST = início do período de teste (1 ano antes da referência)
            DATA_TEST = (reference_date - timedelta(days=365)).strftime('%Y-%m-%d')
            
            # DATA_INICIO_FUTR = data de referência (início das previsões futuras)
            DATA_INICIO_FUTR = reference_date.strftime('%Y-%m-%d')
            
            # DATA_FINAL_FUTR = 1 ano após a data de referência
            DATA_FINAL_FUTR = (reference_date + timedelta(days=365)).strftime('%Y-%m-%d')
            
            logger.info(f"Configurações atualizadas para data de referência {reference_date.strftime('%Y-%m-%d')}")
            logger.info(f"Período de treinamento: até {DATA_TRAIN}")
            logger.info(f"Período de teste: {DATA_TEST} até {DATA_ATUAL.strftime('%Y-%m-%d')}")
            logger.info(f"Período de previsões futuras: {DATA_INICIO_FUTR} até {DATA_FINAL_FUTR}")
            
            # Carrega os dados
            data = load_data(marca, tipo_previsao, data_fim=reference_date.strftime('%Y-%m-%d'))
            
            # Processa os dados até a data de referência
            data_neural = process_data(data, marca, tipo_previsao, data_fim=reference_date.strftime('%Y-%m-%d'))
            
            # Treina e avalia os modelos
            results = train_and_evaluate_models(data_neural, marca, tipo_previsao)
            
            # Encontra o melhor modelo
            best_model = find_best_model(results, marca, tipo_previsao)
            
            # Executa o melhor modelo
            run_best_model(best_model, data_neural, marca, tipo_previsao, results, reference_date)
            
            logger.info(f"Processamento concluído com sucesso para marca {marca}, tipo {tipo_previsao} e data {reference_date.strftime('%Y-%m-%d')}")
            
        finally:
            # Restaurar configurações originais
            DATA_ATUAL = original_data_atual
            DATA_TRAIN = original_data_train
            DATA_TEST = original_data_test
            DATA_INICIO_FUTR = original_data_inicio_futr
            DATA_FINAL_FUTR = original_data_final_futr
        
    except Exception as e:
        logger.error(f"Erro durante o processamento de marca {marca}, tipo {tipo_previsao} e data {reference_date.strftime('%Y-%m-%d')}: {e}")
        raise

def main():
    """Função principal que orquestra todo o fluxo."""
    try:
        logger.info("Iniciando execução do pipeline")

        # Salvar variáveis de configuração
        # Ajuste aqui para passar as listas corretas de variáveis futuras e históricas
        marca_para_salvar = MARCAS[0] if MARCAS else 'default'
        salvar_variaveis_csv(marca_para_salvar, FREQ, HORIZON, VARIAVEIS_FUTURAS, VARIAVEIS_HISTORICAS, DATA_INICIO_BASE)
        
        # Gerar datas de referência
        reference_dates = generate_reference_dates()
        logger.info(f"Executando para {len(reference_dates)} datas de referência:")
        for i, date in enumerate(reference_dates, 1):
            logger.info(f"  {i}. {date.strftime('%Y-%m-%d')} (último dia do mês anterior)")

        # Processa cada combinação de marca e tipo para cada data de referência
        for marca in MARCAS:
            for tipo_previsao in TIPOS_PREVISAO:
                for reference_date in reference_dates:
                    process_marca_tipo_with_date(marca, tipo_previsao, reference_date)
        
        logger.info("Pipeline executado com sucesso para todas as marcas, tipos e datas de referência")
        
    except Exception as e:
        logger.error(f"Erro durante a execução do pipeline: {e}")
        raise

if __name__ == "__main__":
    main()