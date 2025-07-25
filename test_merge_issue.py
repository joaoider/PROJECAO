#!/usr/bin/env python3
"""
Script de teste para verificar o problema do merge.
"""
import sys
import os
sys.path.append('src')

import pandas as pd
from utils.special_dates import SpecialDates

def test_merge_issue():
    """Testa o problema do merge."""
    print("=== TESTE MERGE ISSUE ===")
    
    try:
        # Criar dados simulados como no main.py
        print("1. Criando dados simulados...")
        dates = pd.date_range('2020-01-01', '2023-12-31', freq='D')
        data_neural = pd.DataFrame({
            'ds': dates,
            'unique_id': 'test',
            'y': [100] * len(dates)
        })
        print(f"DataFrame criado: {data_neural.shape}")
        print(f"Colunas: {data_neural.columns.tolist()}")
        print(f"Tipos: {data_neural.dtypes}")
        
        # Criar SpecialDates
        print("\n2. Criando SpecialDates...")
        special_dates = SpecialDates()
        dates_df = special_dates.get_all_dates()
        print(f"Dates DataFrame: {dates_df.shape}")
        print(f"Colunas: {dates_df.columns.tolist()}")
        print(f"Tipos: {dates_df.dtypes}")
        
        # Verificar valores nulos antes do merge
        print(f"\n3. Verificando valores nulos antes do merge:")
        print(f"data_neural nulos: {data_neural.isnull().sum()}")
        print(f"dates_df nulos: {dates_df.isnull().sum()}")
        
        # Fazer o merge
        print("\n4. Fazendo merge...")
        merged_df = pd.merge(
            data_neural,
            dates_df,
            left_on='ds',
            right_on='data',
            how='left'
        )
        print(f"Merge concluído: {merged_df.shape}")
        print(f"Colunas após merge: {merged_df.columns.tolist()}")
        
        # Verificar valores nulos após o merge
        print(f"\n5. Verificando valores nulos após o merge:")
        null_counts = merged_df.isnull().sum()
        print(f"Valores nulos: {null_counts}")
        
        if null_counts.any():
            print("❌ VALORES NULOS ENCONTRADOS APÓS MERGE!")
            null_columns = null_counts[null_counts > 0].index.tolist()
            print(f"Colunas com nulos: {null_columns}")
            
            # Mostrar algumas linhas com nulos
            for col in null_columns:
                null_rows = merged_df[merged_df[col].isnull()]
                print(f"\nLinhas com nulos em '{col}': {len(null_rows)}")
                if len(null_rows) > 0:
                    print(null_rows.head())
        else:
            print("✅ Nenhum valor nulo encontrado após merge")
        
        return True
        
    except Exception as e:
        print(f"❌ ERRO: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_merge_issue()
    if success:
        print("\n✅ TESTE CONCLUÍDO COM SUCESSO")
    else:
        print("\n❌ TESTE FALHOU") 