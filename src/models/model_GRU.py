"""
Modelo GRU para previsão de vendas.
"""
import pandas as pd
import numpy as np
from neuralforecast import NeuralForecast
from neuralforecast.models import GRU
from typing import Dict, Any
import logging
from datetime import datetime, timedelta
import pandas as pd

logger = logging.getLogger(__name__)

class GRUModel:
    """Classe para modelo GRU."""
    
    def __init__(self, **kwargs):
        """
        Inicializa o modelo GRU.
        
        Args:
            **kwargs: Parâmetros do modelo
        """
        self.params = kwargs
        self.model = None
        self.nf = None
        
    def fit(self, data: pd.DataFrame):
        """
        Treina o modelo GRU.
        
        Args:
            data: DataFrame com os dados de treinamento
        """
        logger.info(f"Treinando modelo GRU com parâmetros: {self.params}")
        
        # Criar modelo GRU
        self.model = GRU(
            h=365,  # Horizonte de previsão
            input_size=-1,
            **self.params
        )
        
        # Instanciar NeuralForecast
        self.nf = NeuralForecast(models=[self.model], freq='D')
        
        # Treinar modelo
        self.nf.fit(df=data)
        
        logger.info("Modelo GRU treinado com sucesso")
    
    def predict(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Faz previsões com o modelo GRU.
        
        Args:
            data: DataFrame com dados para previsão
            
        Returns:
            DataFrame com previsões
        """
        logger.info("Fazendo previsões com modelo GRU")
        
        if self.nf is None:
            raise ValueError("Modelo não foi treinado. Chame fit() primeiro.")
        
        # Obter datas de referência das configurações globais
        from config.settings import DATA_ATUAL, DATA_INICIO_FUTR, DATA_FINAL_FUTR
        
        # Criar range de datas futuras baseado nas configurações
        start_date = pd.to_datetime(DATA_INICIO_FUTR)
        end_date = pd.to_datetime(DATA_FINAL_FUTR)
        
        future_dates = pd.date_range(
            start=start_date,
            end=end_date,
            freq='D'
        )
        
        # Obter todos os unique_ids dos dados
        unique_ids = data['unique_id'].unique()
        
        # Criar todas as combinações de unique_id e datas futuras
        futr_df = pd.DataFrame([
            {'ds': date, 'unique_id': uid}
            for date in future_dates
            for uid in unique_ids
        ])
        
        logger.info(f"Gerando previsões para {len(futr_df)} períodos futuros")
        logger.info(f"Período: {futr_df['ds'].min()} até {futr_df['ds'].max()}")
        
        # Fazer previsões usando futr_df
        predictions = self.nf.predict(futr_df=futr_df)
        
        logger.info("Previsões GRU geradas com sucesso")
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
        
        logger.info(f"Parâmetros do modelo GRU salvos em {filepath}")