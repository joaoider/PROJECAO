#!/usr/bin/env python3
"""
Script de teste para verificar o formato da data.
"""
from datetime import datetime

def test_date_format():
    """Testa o formato da data atual."""
    print("=== TESTE FORMATO DE DATA ===")
    
    # Data atual (ano e mês de hoje)
    data_atual = datetime.now().strftime('%Y%m')
    
    print(f"Data atual (YYYYMM): {data_atual}")
    
    # Simular nomes de arquivo
    marca = "BB"
    tipo_previsao = "GERAL"
    
    nome_final = f"{marca}_{tipo_previsao}_{data_atual}.parquet"
    print(f"Nome do arquivo: {nome_final}")
    
    # Exemplo de diretório temporário
    temp_blob_path = f"/mnt/analytics/planejamento/datascience/forecast_marca/temp_{marca}_{tipo_previsao}_{data_atual}"
    print(f"Diretório temporário: {temp_blob_path}")
    
    return True

if __name__ == "__main__":
    success = test_date_format()
    if success:
        print("\n✅ TESTE CONCLUÍDO COM SUCESSO")
    else:
        print("\n❌ TESTE FALHOU") 