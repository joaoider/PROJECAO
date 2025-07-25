#!/usr/bin/env python3
"""
Script de teste para verificar a estrutura das previsões.
"""
import sys
import os
sys.path.append('src')

import pandas as pd
import numpy as np

def test_predictions_structure():
    """Testa a detecção da coluna de previsão."""
    print("=== TESTE ESTRUTURA DE PREVISÕES ===")
    
    try:
        # Simular diferentes estruturas de previsões
        test_cases = [
            {
                'name': 'LSTM',
                'columns': ['ds', 'unique_id', 'LSTM']
            },
            {
                'name': 'GRU', 
                'columns': ['ds', 'unique_id', 'GRU']
            },
            {
                'name': 'NHITS',
                'columns': ['ds', 'unique_id', 'NHITS']
            },
            {
                'name': 'NBEATSx',
                'columns': ['ds', 'unique_id', 'NBEATSx']
            }
        ]
        
        for test_case in test_cases:
            print(f"\n--- Testando {test_case['name']} ---")
            print(f"Colunas: {test_case['columns']}")
            
            # Simular DataFrame de previsões
            predictions = pd.DataFrame({
                'ds': pd.date_range('2020-01-01', periods=10),
                'unique_id': ['test'] * 10,
                test_case['name']: np.random.randn(10)
            })
            
            # Detectar coluna de previsão
            y_pred_col = None
            for col in predictions.columns:
                if col != 'ds' and col != 'unique_id' and not col.startswith('y'):
                    y_pred_col = col
                    break
            
            if y_pred_col is None:
                print("❌ Nenhuma coluna de previsão encontrada")
            else:
                print(f"✅ Coluna de previsão encontrada: {y_pred_col}")
                print(f"   Valores: {predictions[y_pred_col].head()}")
        
        return True
        
    except Exception as e:
        print(f"❌ ERRO: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_predictions_structure()
    if success:
        print("\n✅ TESTE CONCLUÍDO COM SUCESSO")
    else:
        print("\n❌ TESTE FALHOU") 