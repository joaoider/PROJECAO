"""
Modelo NBEATSx para previsão de vendas.
"""
import pandas as pd
import numpy as np
from neuralforecast import NeuralForecast
from neuralforecast.models import NBEATSx
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)

class NBEATSxModel:
    """Classe para modelo NBEATSx."""
    
    def __init__(self, **kwargs):
        """
        Inicializa o modelo NBEATSx.
        
        Args:
            **kwargs: Parâmetros do modelo
        """
        self.params = kwargs
        self.model = None
        self.nf = None
        
    def fit(self, data: pd.DataFrame):
        """
        Treina o modelo NBEATSx.
        
        Args:
            data: DataFrame com os dados de treinamento
        """
        logger.info(f"Treinando modelo NBEATSx com parâmetros: {self.params}")
        
        # Criar modelo NBEATSx
        self.model = NBEATSx(
            h=365,  # Horizonte de previsão
            input_size=-1,
            **self.params
        )
        
        # Instanciar NeuralForecast
        self.nf = NeuralForecast(models=[self.model], freq='D')
        
        # Treinar modelo
        self.nf.fit(df=data)
        
        logger.info("Modelo NBEATSx treinado com sucesso")
    
    def predict(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Faz previsões com o modelo NBEATSx.
        
        Args:
            data: DataFrame com dados para previsão
            
        Returns:
            DataFrame com previsões
        """
        logger.info("Fazendo previsões com modelo NBEATSx")
        
        if self.nf is None:
            raise ValueError("Modelo não foi treinado. Chame fit() primeiro.")
        
        # Fazer previsões
        predictions = self.nf.predict(df=data)
        
        logger.info("Previsões NBEATSx geradas com sucesso")
        return predictions
    
    def save_model(self, filepath: str):
        """
        Salva os parâmetros do modelo.
        
        Args:
            filepath: Caminho para salvar os parâmetros
        """
        import pandas as pd
        
        # Criar DataFrame com parâmetros
        params_df = pd.DataFrame([self.params])
        params_df.to_csv(filepath, index=False)
        
        logger.info(f"Parâmetros do modelo NBEATSx salvos em {filepath}")