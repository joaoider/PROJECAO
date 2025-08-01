"""
Modelo LSTM para previsão de vendas.
"""
import pandas as pd
import numpy as np
from neuralforecast import NeuralForecast
from neuralforecast.models import LSTM
from typing import Dict, Any
import logging
from datetime import datetime, timedelta
import pandas as pd

logger = logging.getLogger(__name__)

class LSTMModel:
    """Classe para modelo LSTM."""
    
    def __init__(self, **kwargs):
        """
        Inicializa o modelo LSTM.
        
        Args:
            **kwargs: Parâmetros do modelo
        """
        self.params = kwargs
        self.model = None
        self.nf = None
        
    def fit(self, data: pd.DataFrame):
        """
        Treina o modelo LSTM.
        
        Args:
            data: DataFrame com os dados de treinamento
        """
        logger.info(f"Treinando modelo LSTM com parâmetros: {self.params}")
        
        # Criar modelo LSTM
        self.model = LSTM(
            h=365,  # Horizonte de previsão
            input_size=-1,
            **self.params
        )
        
        # Instanciar NeuralForecast
        self.nf = NeuralForecast(models=[self.model], freq='D')
        
        # Treinar modelo
        self.nf.fit(df=data)
        
        logger.info("Modelo LSTM treinado com sucesso")
    
    def predict(self, data: pd.DataFrame, start_date: str = None, end_date: str = None) -> pd.DataFrame:
        """
        Faz previsões com o modelo LSTM.
        
        Args:
            data: DataFrame com dados para previsão
            start_date: Data de início para previsões (opcional)
            end_date: Data de fim para previsões (opcional)
            
        Returns:
            DataFrame com previsões
        """
        logger.info("Fazendo previsões com modelo LSTM")
        
        if self.nf is None:
            raise ValueError("Modelo não foi treinado. Chame fit() primeiro.")
        
        # Usar datas fornecidas ou configurações globais
        if start_date is None or end_date is None:
            from config.settings import DATA_INICIO_FUTR, DATA_FINAL_FUTR
            start_date = DATA_INICIO_FUTR
            end_date = DATA_FINAL_FUTR
        
        # Criar range de datas futuras
        start_dt = pd.to_datetime(start_date)
        end_dt = pd.to_datetime(end_date)
        
        future_dates = pd.date_range(
            start=start_dt,
            end=end_dt,
            freq='D'
        )
        
        # Obter todos os unique_ids dos dados
        unique_ids = data['unique_id'].unique()
        
        # Criar futr_df com o mesmo formato que o NeuralForecast espera
        futr_df = pd.DataFrame([
            {'ds': date, 'unique_id': uid}
            for date in future_dates
            for uid in unique_ids
        ])
        
        # Verificar se há combinações faltantes
        try:
            missing_combinations = self.nf.get_missing_future(futr_df)
            if len(missing_combinations) > 0:
                logger.warning(f"Combinações faltantes encontradas: {len(missing_combinations)}")
                # Adicionar as combinações faltantes
                futr_df = pd.concat([futr_df, missing_combinations], ignore_index=True)
                futr_df = futr_df.drop_duplicates(subset=['ds', 'unique_id'])
        except Exception as e:
            logger.warning(f"Erro ao verificar combinações faltantes: {e}")
        
        logger.info(f"Gerando previsões para {len(futr_df)} períodos futuros")
        logger.info(f"Período: {futr_df['ds'].min()} até {futr_df['ds'].max()}")
        logger.info(f"Unique IDs: {unique_ids}")
        
        # Fazer previsões usando futr_df
        predictions = self.nf.predict(futr_df=futr_df)
        
        logger.info("Previsões LSTM geradas com sucesso")
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
        
        logger.info(f"Parâmetros do modelo LSTM salvos em {filepath}")