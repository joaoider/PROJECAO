"""
Script de teste para verificar as configurações de data
"""
import pandas as pd
from datetime import datetime, timedelta
import calendar

def test_date_configurations():
    """Testa as configurações de data para diferentes datas de referência"""
    
    # Simular as datas de referência
    reference_dates = [
        datetime(2023, 12, 31),  # 202312
        datetime(2024, 1, 31),   # 202401
        datetime(2024, 2, 29),   # 202402
        datetime(2024, 3, 31),   # 202403
        datetime(2024, 4, 30),   # 202404
        datetime(2024, 5, 31),   # 202405
        datetime(2024, 6, 30),   # 202406
        datetime(2024, 7, 31),   # 202407
        datetime(2024, 8, 31),   # 202408
        datetime(2024, 9, 30),   # 202409
        datetime(2024, 10, 31),  # 202410
        datetime(2024, 11, 30),  # 202411
        datetime(2024, 12, 31),  # 202412
        datetime(2025, 1, 31),   # 202501
        datetime(2025, 2, 28),   # 202502
        datetime(2025, 3, 31),   # 202503
        datetime(2025, 4, 30),   # 202504
        datetime(2025, 5, 31),   # 202505
        datetime(2025, 6, 30),   # 202506
        datetime(2025, 7, 31),   # 202507
        datetime(2025, 8, 31),   # 202508
    ]
    
    print("=" * 80)
    print("TESTE DE CONFIGURAÇÕES DE DATA")
    print("=" * 80)
    
    for i, reference_date in enumerate(reference_dates, 1):
        print(f"\n{i}. Data de Referência: {reference_date.strftime('%Y-%m-%d')}")
        print("-" * 50)
        
        # Simular as configurações que o código faz
        DATA_ATUAL = reference_date
        DATA_TRAIN = (reference_date - timedelta(days=365)).strftime('%Y-%m-%d')
        DATA_TEST = (reference_date - timedelta(days=365)).strftime('%Y-%m-%d')
        DATA_INICIO_FUTR = reference_date.strftime('%Y-%m-%d')
        DATA_FINAL_FUTR = (reference_date + timedelta(days=365)).strftime('%Y-%m-%d')
        
        print(f"   DATA_ATUAL: {DATA_ATUAL.strftime('%Y-%m-%d')}")
        print(f"   DATA_TRAIN: {DATA_TRAIN}")
        print(f"   DATA_TEST: {DATA_TEST}")
        print(f"   DATA_INICIO_FUTR: {DATA_INICIO_FUTR}")
        print(f"   DATA_FINAL_FUTR: {DATA_FINAL_FUTR}")
        
        # Calcular períodos
        train_start = datetime(2020, 1, 1)
        train_end = pd.to_datetime(DATA_TRAIN)
        test_start = pd.to_datetime(DATA_TEST)
        test_end = DATA_ATUAL
        future_start = pd.to_datetime(DATA_INICIO_FUTR)
        future_end = pd.to_datetime(DATA_FINAL_FUTR)
        
        print(f"\n   Períodos:")
        print(f"   - Treinamento: {train_start.strftime('%Y-%m-%d')} até {train_end.strftime('%Y-%m-%d')}")
        print(f"   - Teste: {test_start.strftime('%Y-%m-%d')} até {test_end.strftime('%Y-%m-%d')}")
        print(f"   - Futuro: {future_start.strftime('%Y-%m-%d')} até {future_end.strftime('%Y-%m-%d')}")
        
        # Verificar se as datas fazem sentido
        if test_start >= test_end:
            print("   ❌ ERRO: Período de teste inválido!")
        else:
            print("   ✅ Período de teste válido")
            
        if future_start >= future_end:
            print("   ❌ ERRO: Período futuro inválido!")
        else:
            print("   ✅ Período futuro válido")
            
        if test_end != future_start:
            print("   ❌ ERRO: Teste e futuro não se conectam!")
        else:
            print("   ✅ Teste e futuro se conectam corretamente")

def test_future_dates_generation():
    """Testa a geração de datas futuras"""
    
    print("\n" + "=" * 80)
    print("TESTE DE GERAÇÃO DE DATAS FUTURAS")
    print("=" * 80)
    
    # Testar com algumas datas de referência
    test_reference_dates = [
        datetime(2023, 12, 31),
        datetime(2024, 1, 31),
        datetime(2025, 7, 31)
    ]
    
    for reference_date in test_reference_dates:
        print(f"\nData de Referência: {reference_date.strftime('%Y-%m-%d')}")
        print("-" * 40)
        
        # Simular a geração de datas futuras como no código
        future_start = reference_date
        future_end = reference_date + timedelta(days=365)
        
        future_dates = pd.date_range(start=future_start, end=future_end, freq='D')
        
        print(f"   Início futuro: {future_start.strftime('%Y-%m-%d')}")
        print(f"   Fim futuro: {future_end.strftime('%Y-%m-%d')}")
        print(f"   Total de dias futuros: {len(future_dates)}")
        print(f"   Primeiras 5 datas: {[d.strftime('%Y-%m-%d') for d in future_dates[:5]]}")
        print(f"   Últimas 5 datas: {[d.strftime('%Y-%m-%d') for d in future_dates[-5:]]}")

if __name__ == "__main__":
    test_date_configurations()
    test_future_dates_generation() 