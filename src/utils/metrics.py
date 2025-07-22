"""
Módulo de métricas para avaliação de modelos.
"""
import numpy as np
import pandas as pd
from typing import Dict, Union, List
import logging

logger = logging.getLogger(__name__)

def calculate_mape(y_true: Union[np.ndarray, pd.Series], 
                  y_pred: Union[np.ndarray, pd.Series]) -> float:
    """
    Calcula o Mean Absolute Percentage Error (MAPE).
    
    Args:
        y_true: Valores reais
        y_pred: Valores previstos
        
    Returns:
        Valor do MAPE
    """
    return np.mean(np.abs((y_true - y_pred) / y_true)) * 100

def calculate_rmse(y_true: Union[np.ndarray, pd.Series], 
                  y_pred: Union[np.ndarray, pd.Series]) -> float:
    """
    Calcula o Root Mean Square Error (RMSE).
    
    Args:
        y_true: Valores reais
        y_pred: Valores previstos
        
    Returns:
        Valor do RMSE
    """
    return np.sqrt(np.mean((y_true - y_pred) ** 2))

def calculate_mae(y_true: Union[np.ndarray, pd.Series], 
                 y_pred: Union[np.ndarray, pd.Series]) -> float:
    """
    Calcula o Mean Absolute Error (MAE).
    
    Args:
        y_true: Valores reais
        y_pred: Valores previstos
        
    Returns:
        Valor do MAE
    """
    return np.mean(np.abs(y_true - y_pred))

def calculate_mse(y_true: Union[np.ndarray, pd.Series], 
                 y_pred: Union[np.ndarray, pd.Series]) -> float:
    """
    Calcula o Mean Square Error (MSE).
    
    Args:
        y_true: Valores reais
        y_pred: Valores previstos
        
    Returns:
        Valor do MSE
    """
    return np.mean((y_true - y_pred) ** 2)

def calculate_metrics(y_true: Union[np.ndarray, pd.Series], 
                     y_pred: Union[np.ndarray, pd.Series]) -> Dict[str, float]:
    """
    Calcula todas as métricas disponíveis.
    
    Args:
        y_true: Valores reais
        y_pred: Valores previstos
        
    Returns:
        Dicionário com todas as métricas
    """
    metrics = {
        'MAPE': calculate_mape(y_true, y_pred),
        'RMSE': calculate_rmse(y_true, y_pred),
        'MAE': calculate_mae(y_true, y_pred),
        'MSE': calculate_mse(y_true, y_pred)
    }
    
    logger.info(f"Métricas calculadas: {metrics}")
    return metrics

def save_metrics(metrics: Dict[str, float], 
                model_name: str, 
                marca: str,
                output_dir: str) -> None:
    """
    Salva as métricas em um arquivo CSV.
    
    Args:
        metrics: Dicionário com as métricas
        model_name: Nome do modelo
        marca: Nome da marca
        output_dir: Diretório de saída
    """
    df = pd.DataFrame([metrics])
    output_file = f"{output_dir}/forecast_with_metrics_{model_name}_{marca}.csv"
    df.to_csv(output_file, index=False)
    logger.info(f"Métricas salvas em {output_file}")

def compare_models(metrics_list: List[Dict[str, float]], 
                  model_names: List[str]) -> pd.DataFrame:
    """
    Compara as métricas de diferentes modelos.
    
    Args:
        metrics_list: Lista de dicionários com métricas
        model_names: Lista de nomes dos modelos
        
    Returns:
        DataFrame com a comparação
    """
    comparison = pd.DataFrame(metrics_list, index=model_names)
    logger.info("Comparação de modelos:\n" + str(comparison))
    return comparison 