#!/usr/bin/env python3
"""
Script de teste para verificar o problema com special_dates.
"""
import sys
import os
sys.path.append('src')

import pandas as pd
from utils.special_dates import SpecialDates

def test_special_dates():
    """Testa a funcionalidade de SpecialDates."""
    print("=== TESTE SPECIAL_DATES ===")
    
    try:
        # Criar instância
        special_dates = SpecialDates()
        print("✅ SpecialDates criado com sucesso")
        
        # Testar get_all_dates
        print("\n--- Testando get_all_dates ---")
        dates_df = special_dates.get_all_dates()
        print(f"DataFrame criado: {dates_df.shape}")
        print(f"Colunas: {dates_df.columns.tolist()}")
        print(f"Tipos de dados: {dates_df.dtypes}")
        
        # Verificar valores nulos
        print(f"\nValores nulos: {dates_df.isnull().sum()}")
        
        if dates_df.isnull().any().any():
            print("❌ VALORES NULOS ENCONTRADOS!")
            print(dates_df[dates_df.isnull().any(axis=1)])
        else:
            print("✅ Nenhum valor nulo encontrado")
        
        # Mostrar primeiras linhas
        print(f"\nPrimeiras 5 linhas:")
        print(dates_df.head())
        
        # Testar alguns eventos específicos
        print("\n--- Testando eventos específicos ---")
        events_to_test = ['black_friday', 'carnaval', 'covid']
        
        for event in events_to_test:
            try:
                dates = special_dates.get_dates_for_event(event)
                print(f"{event}: {len(dates)} datas")
            except Exception as e:
                print(f"❌ Erro em {event}: {e}")
        
        return True
        
    except Exception as e:
        print(f"❌ ERRO: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_special_dates()
    if success:
        print("\n✅ TESTE CONCLUÍDO COM SUCESSO")
    else:
        print("\n❌ TESTE FALHOU") 