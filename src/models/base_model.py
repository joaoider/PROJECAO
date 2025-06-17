"""
Classe base para modelos de previsão.
"""
from abc import ABC, abstractmethod
import pandas as pd
import numpy as np
from typing import Dict, Any, Optional
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

class BaseModel(ABC):
    """Classe base abstrata para modelos de previsão."""
    
    def __init__(self, config: Dict[str, Any]):
        """
        Inicializa o modelo base.
        
        Args:
            config: Dicionário com configurações do modelo
        """
        self.config = config
        self.model = None
        self.is_fitted = False
        
    @abstractmethod
    def fit(self, data: pd.DataFrame) -> None:
        """
        Treina o modelo.
        
        Args:
            data: DataFrame com dados de treinamento
        """
        pass
    
    @abstractmethod
    def predict(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Faz previsões com o modelo.
        
        Args:
            data: DataFrame com dados para previsão
            
        Returns:
            DataFrame com previsões
        """
        pass
    
    def save_model(self, path: Path) -> None:
        """
        Salva o modelo treinado.
        
        Args:
            path: Caminho para salvar o modelo
        """
        if not self.is_fitted:
            raise ValueError("Modelo não foi treinado ainda")
        
        try:
            self._save_model_impl(path)
            logger.info(f"Modelo salvo em {path}")
        except Exception as e:
            logger.error(f"Erro ao salvar modelo: {e}")
            raise
    
    @abstractmethod
    def _save_model_impl(self, path: Path) -> None:
        """
        Implementação específica para salvar o modelo.
        
        Args:
            path: Caminho para salvar o modelo
        """
        pass
    
    def load_model(self, path: Path) -> None:
        """
        Carrega um modelo salvo.
        
        Args:
            path: Caminho do modelo salvo
        """
        try:
            self._load_model_impl(path)
            self.is_fitted = True
            logger.info(f"Modelo carregado de {path}")
        except Exception as e:
            logger.error(f"Erro ao carregar modelo: {e}")
            raise
    
    @abstractmethod
    def _load_model_impl(self, path: Path) -> None:
        """
        Implementação específica para carregar o modelo.
        
        Args:
            path: Caminho do modelo salvo
        """
        pass
    
    def evaluate(self, y_true: pd.Series, y_pred: pd.Series) -> Dict[str, float]:
        """
        Avalia o modelo usando métricas comuns.
        
        Args:
            y_true: Valores reais
            y_pred: Valores previstos
            
        Returns:
            Dicionário com métricas de avaliação
        """
        metrics = {}
        
        # MAPE
        mape = np.mean(np.abs((y_true - y_pred) / y_true)) * 100
        metrics['MAPE'] = mape
        
        # RMSE
        rmse = np.sqrt(np.mean((y_true - y_pred) ** 2))
        metrics['RMSE'] = rmse
        
        # MAE
        mae = np.mean(np.abs(y_true - y_pred))
        metrics['MAE'] = mae
        
        logger.info(f"Métricas de avaliação: {metrics}")
        return metrics 