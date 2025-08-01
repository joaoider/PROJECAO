"""
Script de teste para verificar como os modelos geram previsões
"""
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def create_test_data():
    """Cria dados de teste para simular o problema"""
    
    # Criar dados históricos de exemplo
    start_date = datetime(2020, 1, 1)
    end_date = datetime(2025, 7, 31)
    
    dates = pd.date_range(start=start_date, end=end_date, freq='D')
    
    # Criar dados simulados
    data = pd.DataFrame({
        'ds': dates,
        'unique_id': 'BB',
        'y': np.random.randint(100000, 500000, len(dates))
    })
    
    return data

def test_model_prediction_simulation():
    """Simula como os modelos estão gerando previsões"""
    
    print("=" * 80)
    print("TESTE DE SIMULAÇÃO DE PREVISÕES DOS MODELOS")
    print("=" * 80)
    
    # Criar dados de teste
    data = create_test_data()
    print(f"Dados criados: {len(data)} registros")
    print(f"Período: {data['ds'].min()} até {data['ds'].max()}")
    
    # Simular diferentes datas de referência
    reference_dates = [
        datetime(2023, 12, 31),
        datetime(2024, 1, 31),
        datetime(2025, 7, 31)
    ]
    
    for reference_date in reference_dates:
        print(f"\n{'='*60}")
        print(f"Data de Referência: {reference_date.strftime('%Y-%m-%d')}")
        print(f"{'='*60}")
        
        # Simular as configurações do código
        DATA_ATUAL = reference_date
        DATA_TRAIN = (reference_date - timedelta(days=365)).strftime('%Y-%m-%d')
        DATA_TEST = (reference_date - timedelta(days=365)).strftime('%Y-%m-%d')
        DATA_INICIO_FUTR = reference_date.strftime('%Y-%m-%d')
        DATA_FINAL_FUTR = (reference_date + timedelta(days=365)).strftime('%Y-%m-%d')
        
        print(f"Configurações:")
        print(f"  DATA_ATUAL: {DATA_ATUAL.strftime('%Y-%m-%d')}")
        print(f"  DATA_TRAIN: {DATA_TRAIN}")
        print(f"  DATA_TEST: {DATA_TEST}")
        print(f"  DATA_INICIO_FUTR: {DATA_INICIO_FUTR}")
        print(f"  DATA_FINAL_FUTR: {DATA_FINAL_FUTR}")
        
        # Simular o processamento de dados até a data de referência
        data_processed = data[data['ds'] <= reference_date].copy()
        print(f"\nDados processados até {reference_date.strftime('%Y-%m-%d')}: {len(data_processed)} registros")
        
        # Simular a criação de dados futuros para previsão
        future_start = pd.to_datetime(DATA_INICIO_FUTR)
        future_end = pd.to_datetime(DATA_FINAL_FUTR)
        
        future_dates = pd.date_range(start=future_start, end=future_end, freq='D')
        unique_ids = data_processed['unique_id'].unique()
        
        future_data = pd.DataFrame([
            {'ds': date, 'unique_id': uid}
            for date in future_dates
            for uid in unique_ids
        ])
        
        print(f"\nDados futuros criados:")
        print(f"  Início: {future_start.strftime('%Y-%m-%d')}")
        print(f"  Fim: {future_end.strftime('%Y-%m-%d')}")
        print(f"  Total de registros futuros: {len(future_data)}")
        print(f"  Primeiras 5 datas: {[d.strftime('%Y-%m-%d') for d in future_dates[:5]]}")
        print(f"  Últimas 5 datas: {[d.strftime('%Y-%m-%d') for d in future_dates[-5:]]}")
        
        # Simular previsões (valores aleatórios para teste)
        np.random.seed(42)  # Para reprodutibilidade
        predictions = future_data.copy()
        predictions['y_pred'] = np.random.randint(300000, 400000, len(predictions))
        
        print(f"\nPrevisões simuladas:")
        print(f"  Total de previsões: {len(predictions)}")
        print(f"  Primeiras 5 previsões:")
        for i in range(5):
            print(f"    {predictions.iloc[i]['ds'].strftime('%Y-%m-%d')}: {predictions.iloc[i]['y_pred']:.0f}")
        
        # Simular dados de teste
        test_start = pd.to_datetime(DATA_TEST)
        test_end = DATA_ATUAL
        
        test_dates = pd.date_range(start=test_start, end=test_end, freq='D')
        test_data = pd.DataFrame([
            {'ds': date, 'unique_id': uid}
            for date in test_dates
            for uid in unique_ids
        ])
        
        test_predictions = test_data.copy()
        test_predictions['y_pred'] = np.random.randint(300000, 400000, len(test_predictions))
        
        print(f"\nDados de teste:")
        print(f"  Início: {test_start.strftime('%Y-%m-%d')}")
        print(f"  Fim: {test_end.strftime('%Y-%m-%d')}")
        print(f"  Total de registros de teste: {len(test_predictions)}")
        
        # Simular junção de dados de teste + previsões futuras
        serie_completa = pd.concat([test_predictions, predictions], ignore_index=True)
        serie_completa = serie_completa.sort_values('ds').reset_index(drop=True)
        
        print(f"\nSérie completa (teste + futuro):")
        print(f"  Total de registros: {len(serie_completa)}")
        print(f"  Período: {serie_completa['ds'].min().strftime('%Y-%m-%d')} até {serie_completa['ds'].max().strftime('%Y-%m-%d')}")
        print(f"  Primeiras 5 datas: {[d.strftime('%Y-%m-%d') for d in serie_completa['ds'].head()]}")
        print(f"  Últimas 5 datas: {[d.strftime('%Y-%m-%d') for d in serie_completa['ds'].tail()]}")

if __name__ == "__main__":
    test_model_prediction_simulation() 