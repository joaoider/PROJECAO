"""
Teste para verificar quando as configurações são importadas
"""
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def test_import_timing():
    """Testa quando as configurações são importadas"""
    
    print("=" * 80)
    print("TESTE DE TIMING DE IMPORTAÇÃO DAS CONFIGURAÇÕES")
    print("=" * 80)
    
    # Simular as configurações globais
    global DATA_INICIO_FUTR, DATA_FINAL_FUTR
    
    # Testar diferentes datas de referência
    reference_dates = [
        datetime(2023, 12, 31),
        datetime(2024, 1, 31),
        datetime(2025, 7, 31)
    ]
    
    for i, reference_date in enumerate(reference_dates, 1):
        print(f"\n{i}. Data de Referência: {reference_date.strftime('%Y-%m-%d')}")
        print("-" * 60)
        
        # Simular a atualização das configurações globais
        DATA_INICIO_FUTR = reference_date.strftime('%Y-%m-%d')
        DATA_FINAL_FUTR = (reference_date + timedelta(days=365)).strftime('%Y-%m-%d')
        
        print(f"   Configurações globais atualizadas:")
        print(f"   DATA_INICIO_FUTR: {DATA_INICIO_FUTR}")
        print(f"   DATA_FINAL_FUTR: {DATA_FINAL_FUTR}")
        
        # Simular o que acontece quando o modelo importa as configurações
        def simulate_model_predict():
            """Simula o que o modelo faz quando chama predict"""
            # Esta linha simula o que acontece no modelo
            # from config.settings import DATA_INICIO_FUTR, DATA_FINAL_FUTR
            
            # Em vez de importar, usar as variáveis globais
            global DATA_INICIO_FUTR, DATA_FINAL_FUTR
            
            print(f"   Modelo importou configurações:")
            print(f"   DATA_INICIO_FUTR: {DATA_INICIO_FUTR}")
            print(f"   DATA_FINAL_FUTR: {DATA_FINAL_FUTR}")
            
            # Simular criação de datas futuras
            start_date = pd.to_datetime(DATA_INICIO_FUTR)
            end_date = pd.to_datetime(DATA_FINAL_FUTR)
            
            future_dates = pd.date_range(start=start_date, end=end_date, freq='D')
            
            print(f"   Datas futuras geradas:")
            print(f"   Início: {start_date.strftime('%Y-%m-%d')}")
            print(f"   Fim: {end_date.strftime('%Y-%m-%d')}")
            print(f"   Total de dias: {len(future_dates)}")
            print(f"   Primeiras 3 datas: {[d.strftime('%Y-%m-%d') for d in future_dates[:3]]}")
            print(f"   Últimas 3 datas: {[d.strftime('%Y-%m-%d') for d in future_dates[-3:]]}")
        
        # Simular a chamada do modelo
        simulate_model_predict()

def test_config_import():
    """Testa a importação real das configurações"""
    
    print("\n" + "=" * 80)
    print("TESTE DE IMPORTAÇÃO REAL DAS CONFIGURAÇÕES")
    print("=" * 80)
    
    try:
        # Tentar importar do diretório src
        import sys
        sys.path.append('src')
        from config.settings import DATA_INICIO_FUTR, DATA_FINAL_FUTR
        print(f"Configurações importadas:")
        print(f"   DATA_INICIO_FUTR: {DATA_INICIO_FUTR}")
        print(f"   DATA_FINAL_FUTR: {DATA_FINAL_FUTR}")
        
        # Verificar se as datas fazem sentido
        start_date = pd.to_datetime(DATA_INICIO_FUTR)
        end_date = pd.to_datetime(DATA_FINAL_FUTR)
        
        print(f"\nAnálise das datas:")
        print(f"   Início: {start_date.strftime('%Y-%m-%d')}")
        print(f"   Fim: {end_date.strftime('%Y-%m-%d')}")
        print(f"   Diferença em dias: {(end_date - start_date).days}")
        
        if start_date >= end_date:
            print("   ❌ ERRO: Data de início >= Data de fim!")
        else:
            print("   ✅ Datas válidas")
            
    except Exception as e:
        print(f"Erro ao importar configurações: {e}")

if __name__ == "__main__":
    test_import_timing()
    test_config_import() 