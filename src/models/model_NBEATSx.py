"""
Modelo NBEATSx para previsão de vendas.
"""
import pandas as pd
import numpy as np
from neuralforecast import NeuralForecast
from neuralforecast.models import NBEATSx
from typing import Dict, Any
import logging
from datetime import datetime, timedelta
import pandas as pd

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
        
        # Usar o método make_future_dataframe para obter o formato correto
        # e depois ajustar as datas conforme necessário
        base_futr_df = self.nf.make_future_dataframe(df=data)
        
        # Obter datas de referência das configurações globais
        from config.settings import DATA_INICIO_FUTR, DATA_FINAL_FUTR
        
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
        
        # Fazer previsões usando futr_df
        predictions = self.nf.predict(futr_df=futr_df)
        
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