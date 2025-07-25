"""
Módulo de processamento de dados.
"""
import pandas as pd
import logging
from typing import Optional, List, Dict, Any
from pathlib import Path

logger = logging.getLogger(__name__)

class DataProcessor:
    """Classe base para processamento de dados."""
    
    def __init__(self, marca: str, data_inicio: str, data_fim: str):
        """
        Inicializa o processador de dados.
        
        Args:
            marca: Nome da marca
            data_inicio: Data de início do período
            data_fim: Data de fim do período
        """
        self.marca = marca
        self.data_inicio = pd.to_datetime(data_inicio)
        self.data_fim = pd.to_datetime(data_fim)
        
    def process_data(self, data: pd.DataFrame, unique_id: Optional[str] = None) -> pd.DataFrame:
        """
        Processa os dados brutos.
        
        Args:
            data: DataFrame com os dados brutos
            unique_id: ID único para agrupamento (opcional)
            
        Returns:
            DataFrame processado
        """
        logger.info(f"Iniciando processamento de dados para {self.marca}")
        
        # Colunas a serem removidas
        drop_cols = [
            'MARCA_SIGLA', 'GRIFFE', 'CODIGO_FILIAL', 'CANAL_ORIGEM',
            'CIDADE', 'UF', 'STATUS_PRODUTO', 'TIPO_VENDA', 'LINHA',
            'GRUPO', 'MEDIA_VLF', 'MEDIA_QLF', 'MEDIA_ROL', 'MEDIA_CPV'
        ]
        
        # Remove colunas desnecessárias
        data = data.drop(columns=[col for col in drop_cols if col in data.columns])
        
        # Converte tipos de dados
        data['DATA'] = pd.to_datetime(data['DATA'])
        data['VLF'] = data['VLF'].astype(float)
        data['QLF'] = data['QLF'].astype(float)
        data['ROL'] = data['ROL'].astype(float)
        data['CPV'] = data['CPV'].astype(float)
        
        # Filtra por período
        data = data.loc[data['DATA'] >= self.data_inicio]
        
        # Adiciona unique_id
        if unique_id is not None:
            data['unique_id'] = unique_id
        else:
            data['unique_id'] = self.marca
        data['unique_id'] = data['unique_id'].astype(object)
        
        # Agrupa dados sempre incluindo unique_id
        group_cols = ['DATA', 'unique_id']
        data = data.groupby(group_cols).agg({
            'VLF': 'sum',
            'QLF': 'sum',
            'ROL': 'sum',
            'CPV': 'sum'
        }).reset_index()
        
        # Ordena dados
        data = data.sort_values(by='DATA').reset_index(drop=True)
        
        # Prepara dados para modelo neural
        data_neural = data.copy()
        data_neural.rename(columns={'DATA': 'ds', 'VLF': 'y'}, inplace=True)
        
        # Verifica se todas as colunas necessárias existem
        required_columns = ['ds', 'unique_id', 'y', 'QLF', 'ROL', 'CPV']
        available_columns = data_neural.columns.tolist()
        logger.info(f"Colunas disponíveis: {available_columns}")
        logger.info(f"Colunas necessárias: {required_columns}")
        
        # Verifica se todas as colunas estão presentes
        missing_columns = [col for col in required_columns if col not in available_columns]
        if missing_columns:
            logger.error(f"Colunas faltando: {missing_columns}")
            raise ValueError(f"Colunas necessárias não encontradas: {missing_columns}")
        
        data_neural = data_neural[required_columns]
        
        logger.info(f"Processamento de dados concluído para {self.marca}")
        logger.info(f"Shape final: {data_neural.shape}")
        logger.info(f"Colunas finais: {data_neural.columns.tolist()}")
        return data_neural
    
    def verify_missing_dates(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Verifica e completa datas faltantes.
        
        Args:
            data: DataFrame com os dados
            
        Returns:
            DataFrame com datas completadas
        """
        logger.info("Verificando datas faltantes")
        
        # Gera intervalo completo de datas
        date_range = pd.date_range(
            start=data['ds'].min(),
            end=data['ds'].max(),
            freq='D'
        )
        
        # Para cada unique_id
        dfs_completed = []
        for unique_id in data['unique_id'].unique():
            df_id = data[data['unique_id'] == unique_id]
            dates_present = pd.to_datetime(df_id['ds'])
            missing_dates = date_range.difference(dates_present)
            
            if len(missing_dates) > 0:
                logger.info(f"Encontradas {len(missing_dates)} datas faltantes para {unique_id}")
                
                # Cria DataFrame com datas faltantes
                df_missing = pd.DataFrame({
                    'ds': missing_dates,
                    'unique_id': unique_id,
                    'y': 0,
                    'QLF': 0,
                    'ROL': 0,
                    'CPV': 0
                })
                
                dfs_completed.append(pd.concat([df_id, df_missing]))
            else:
                dfs_completed.append(df_id)
        
        # Combina todos os DataFrames
        result = pd.concat(dfs_completed, ignore_index=True)
        result = result.sort_values(['unique_id', 'ds']).reset_index(drop=True)
        
        logger.info("Verificação de datas faltantes concluída")
        return result
    
    def save_processed_data(self, data: pd.DataFrame, output_dir: Path) -> None:
        """
        Salva os dados processados.
        
        Args:
            data: DataFrame com os dados processados
            output_dir: Diretório de saída
        """
        output_file = output_dir / f'processed_data_{self.marca}.csv'
        data.to_csv(output_file, index=False)
        logger.info(f"Dados processados salvos em {output_file}") 