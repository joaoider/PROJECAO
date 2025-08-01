"""
Modelo NHITS para previsão de vendas.
"""
import pandas as pd
import numpy as np
from neuralforecast import NeuralForecast
from neuralforecast.models import NHITS
from typing import Dict, Any
import logging
from datetime import datetime, timedelta
import pandas as pd

logger = logging.getLogger(__name__)

class NHITSModel:
    """Classe para modelo NHITS."""
    
    def __init__(self, **kwargs):
        """
        Inicializa o modelo NHITS.
        
        Args:
            **kwargs: Parâmetros do modelo
        """
        self.params = kwargs
        self.model = None
        self.nf = None
        
    def fit(self, data: pd.DataFrame):
        """
        Treina o modelo NHITS.
        
        Args:
            data: DataFrame com os dados de treinamento
        """
        logger.info(f"Treinando modelo NHITS com parâmetros: {self.params}")
        
        # Criar modelo NHITS
        self.model = NHITS(
            h=365,  # Horizonte de previsão
            input_size=-1,
            **self.params
        )
        
        # Instanciar NeuralForecast
        self.nf = NeuralForecast(models=[self.model], freq='D')
        
        # Treinar modelo
        self.nf.fit(df=data)
        
        logger.info("Modelo NHITS treinado com sucesso")
    
    def predict(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Faz previsões com o modelo NHITS.
        
        Args:
            data: DataFrame com dados para previsão
            
        Returns:
            DataFrame com previsões
        """
        logger.info("Fazendo previsões com modelo NHITS")
        
        if self.nf is None:
            raise ValueError("Modelo não foi treinado. Chame fit() primeiro.")
        
        # Criar dataframe futuro para previsões
        data_atual = datetime.now()
        data_fim = data_atual + timedelta(days=365)
        
        # Criar range de datas futuras
        future_dates = pd.date_range(
            start=data_atual,
            end=data_fim,
            freq='D'
        )
        
        # Criar futr_df com as datas futuras
        futr_df = pd.DataFrame({
            'ds': future_dates,
            'unique_id': data['unique_id'].iloc[0] if len(data) > 0 else 'default'
        })
        
        logger.info(f"Gerando previsões de {data_atual.strftime('%Y-%m-%d')} até {data_fim.strftime('%Y-%m-%d')}")
        
        # Fazer previsões usando futr_df
        predictions = self.nf.predict(futr_df=futr_df)
        
        logger.info("Previsões NHITS geradas com sucesso")
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
        
        logger.info(f"Parâmetros do modelo NHITS salvos em {filepath}")