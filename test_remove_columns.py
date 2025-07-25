#!/usr/bin/env python3
"""
Script de teste para verificar a remoção das colunas.
"""
import sys
import os
sys.path.append('src')

import pandas as pd
from utils.special_dates import SpecialDates

def test_remove_columns():
    """Testa a remoção das colunas problemáticas."""
    print("=== TESTE REMOÇÃO DE COLUNAS ===")
    
    try:
        # Criar dados simulados
        print("1. Criando dados simulados...")
        dates = pd.date_range('2020-01-01', '2023-12-31', freq='D')
        data_neural = pd.DataFrame({
            'ds': dates,
            'unique_id': 'test',
            'y': [100] * len(dates)
        })
        
        # Criar SpecialDates
        print("\n2. Criando SpecialDates...")
        special_dates = SpecialDates()
        dates_df = special_dates.get_all_dates()
        
        # Fazer merge
        print("\n3. Fazendo merge...")
        merged_df = pd.merge(
            data_neural,
            dates_df,
            left_on='ds',
            right_on='data',
            how='left'
        )
        
        print(f"Antes da remoção: {merged_df.shape}")
        print(f"Colunas: {merged_df.columns.tolist()}")
        
        # Remover colunas problemáticas
        print("\n4. Removendo colunas problemáticas...")
        if 'data' in merged_df.columns:
            merged_df = merged_df.drop(columns=['data'])
        if 'tipo' in merged_df.columns:
            merged_df = merged_df.drop(columns=['tipo'])
        if 'evento' in merged_df.columns:
            merged_df = merged_df.drop(columns=['evento'])
        
        print(f"Após remoção: {merged_df.shape}")
        print(f"Colunas: {merged_df.columns.tolist()}")
        
        # Verificar se há valores nulos
        print(f"\n5. Verificando valores nulos:")
        null_counts = merged_df.isnull().sum()
        print(f"Valores nulos: {null_counts}")
        
        if null_counts.any():
            print("❌ AINDA HÁ VALORES NULOS!")
        else:
            print("✅ Nenhum valor nulo encontrado")
        
        # Verificar tipos de dados
        print(f"\n6. Tipos de dados:")
        print(merged_df.dtypes)
        
        return True
        
    except Exception as e:
        print(f"❌ ERRO: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_remove_columns()
    if success:
        print("\n✅ TESTE CONCLUÍDO COM SUCESSO")
    else:
        print("\n❌ TESTE FALHOU") 