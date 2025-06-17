"""
Testes para o módulo de processamento de dados.
"""
import pytest
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from src.utils.data_processing import DataProcessor

@pytest.fixture
def sample_data():
    """Fixture com dados de exemplo."""
    dates = pd.date_range(start='2024-01-01', end='2024-01-10', freq='D')
    data = {
        'DATA': dates,
        'VLF': np.random.uniform(1000, 2000, len(dates)),
        'QLF': np.random.uniform(100, 200, len(dates)),
        'ROL': np.random.uniform(5000, 6000, len(dates)),
        'CPV': np.random.uniform(800, 1000, len(dates)),
        'MARCA_SIGLA': ['TEST'] * len(dates),
        'GRIFFE': ['TEST'] * len(dates)
    }
    return pd.DataFrame(data)

@pytest.fixture
def processor():
    """Fixture com processador de dados."""
    return DataProcessor(
        marca='TEST',
        data_inicio='2024-01-01',
        data_fim='2024-01-10'
    )

def test_process_data(processor, sample_data):
    """Testa o processamento básico de dados."""
    result = processor.process_data(sample_data)
    
    # Verifica se as colunas corretas foram mantidas
    expected_columns = ['ds', 'unique_id', 'y', 'QLF', 'ROL', 'CPV']
    assert all(col in result.columns for col in expected_columns)
    
    # Verifica se os tipos de dados estão corretos
    assert result['ds'].dtype == 'datetime64[ns]'
    assert result['y'].dtype == 'float64'
    assert result['unique_id'].dtype == 'object'
    
    # Verifica se os dados foram agrupados corretamente
    assert len(result) == len(sample_data)

def test_verify_missing_dates(processor, sample_data):
    """Testa a verificação de datas faltantes."""
    # Processa os dados primeiro
    processed_data = processor.process_data(sample_data)
    
    # Remove algumas datas para criar lacunas
    dates_to_remove = processed_data['ds'].iloc[2:4]
    data_with_gaps = processed_data[~processed_data['ds'].isin(dates_to_remove)]
    
    # Verifica datas faltantes
    result = processor.verify_missing_dates(data_with_gaps)
    
    # Verifica se todas as datas foram preenchidas
    expected_dates = pd.date_range(
        start=processed_data['ds'].min(),
        end=processed_data['ds'].max(),
        freq='D'
    )
    assert all(date in result['ds'].values for date in expected_dates)
    
    # Verifica se os valores para datas faltantes são zero
    missing_dates = result[result['ds'].isin(dates_to_remove)]
    assert all(missing_dates[['y', 'QLF', 'ROL', 'CPV']].values == 0)

def test_save_processed_data(processor, sample_data, tmp_path):
    """Testa o salvamento de dados processados."""
    # Processa os dados
    processed_data = processor.process_data(sample_data)
    
    # Salva os dados
    output_dir = tmp_path / "output"
    output_dir.mkdir()
    processor.save_processed_data(processed_data, output_dir)
    
    # Verifica se o arquivo foi criado
    output_file = output_dir / f'processed_data_{processor.marca}.csv'
    assert output_file.exists()
    
    # Verifica se os dados salvos podem ser lidos
    loaded_data = pd.read_csv(output_file)
    assert len(loaded_data) == len(processed_data)
    assert all(col in loaded_data.columns for col in processed_data.columns) 