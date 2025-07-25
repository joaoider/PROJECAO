#!/usr/bin/env python3
"""
Script de teste para verificar a correção do merge.
"""
import sys
import os
sys.path.append('src')

import pandas as pd
from utils.special_dates import SpecialDates

def test_fix_merge():
    """Testa a correção do merge."""
    print("=== TESTE CORREÇÃO MERGE ===")
    
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
        
        # Fazer merge com correção
        print("\n3. Fazendo merge com correção...")
        merged_df = pd.merge(
            data_neural,
            dates_df,
            left_on='ds',
            right_on='data',
            how='left'
        )
        
        # Aplicar correção
        print("\n4. Aplicando correção...")
        merged_df['tipo'] = merged_df['tipo'].fillna('sem_evento')
        merged_df['evento'] = merged_df['evento'].fillna('Sem Evento')
        
        # Remover coluna 'data' duplicada se existir
        if 'data' in merged_df.columns:
            merged_df = merged_df.drop(columns=['data'])
        
        print(f"Merge corrigido: {merged_df.shape}")
        print(f"Colunas: {merged_df.columns.tolist()}")
        
        # Verificar valores nulos após correção
        print(f"\n5. Verificando valores nulos após correção:")
        null_counts = merged_df.isnull().sum()
        print(f"Valores nulos: {null_counts}")
        
        if null_counts.any():
            print("❌ AINDA HÁ VALORES NULOS!")
            null_columns = null_counts[null_counts > 0].index.tolist()
            print(f"Colunas com nulos: {null_columns}")
        else:
            print("✅ Nenhum valor nulo encontrado após correção")
        
        # Verificar valores únicos nas colunas
        print(f"\n6. Valores únicos em 'tipo': {merged_df['tipo'].unique()}")
        print(f"Valores únicos em 'evento': {merged_df['evento'].unique()}")
        
        return True
        
    except Exception as e:
        print(f"❌ ERRO: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_fix_merge()
    if success:
        print("\n✅ TESTE CONCLUÍDO COM SUCESSO")
    else:
        print("\n❌ TESTE FALHOU") 