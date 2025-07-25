#!/usr/bin/env python3
"""
Script de teste para verificar a estrutura de pastas.
"""
from datetime import datetime
from pathlib import Path

def test_folder_structure():
    """Testa a estrutura de pastas com data."""
    print("=== TESTE ESTRUTURA DE PASTAS ===")
    
    # Simular configurações
    FORECASTS_DIR = Path("data/forecasts")
    marca = "BB"
    tipo_previsao = "GERAL"
    
    # Data atual
    data_atual = datetime.now().strftime('%Y%m')
    
    # Criar caminho da pasta
    pasta_data = FORECASTS_DIR / marca / tipo_previsao / data_atual
    
    print(f"Pasta base: {FORECASTS_DIR}")
    print(f"Marca: {marca}")
    print(f"Tipo previsão: {tipo_previsao}")
    print(f"Data atual: {data_atual}")
    print(f"Pasta completa: {pasta_data}")
    
    # Simular arquivos que serão criados
    arquivos = [
        f'previsoes_finais_LSTM_0.001_32_200_200_2_2_True_0.0_-1_-1_100_1.csv',
        f'previsoes_finais_LSTM_0.001_32_200_200_2_2_True_0.0_-1_-1_100_1.parquet',
        'relatorio_comparacao_modelos.csv',
        'melhor_modelo_parametros_LSTM_0.001_32_200_200_2_2_True_0.0_-1_-1_100_1.csv'
    ]
    
    print(f"\nArquivos que serão criados em {pasta_data}:")
    for arquivo in arquivos:
        print(f"  📄 {arquivo}")
    
    # Estrutura completa
    print(f"\nEstrutura completa:")
    print(f"data/forecasts/")
    print(f"└── {marca}/")
    print(f"    └── {tipo_previsao}/")
    print(f"        └── {data_atual}/")
    for arquivo in arquivos:
        print(f"            └── {arquivo}")
    
    return True

if __name__ == "__main__":
    success = test_folder_structure()
    if success:
        print("\n✅ TESTE CONCLUÍDO COM SUCESSO")
    else:
        print("\n❌ TESTE FALHOU") 