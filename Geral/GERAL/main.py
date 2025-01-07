import time
# Marcação de início de execução
start_time = time.time()

from configuracoes_modelos.imports import *
from configuracoes import marca, freq, horizon, variaveis_futuras, variaveis_historicas, data_inicio_base
from funcoes import salvar_variaveis_csv, excluir_arquivos_antigos, executar_script, encontrar_melhor_modelo, rodar_modelo_vencedor


if __name__ == "__main__":
    # Salvar as variáveis em CSV
    salvar_variaveis_csv(marca, freq, horizon, variaveis_futuras, variaveis_historicas)
    
    # Executar main_LSTM.py
    print("Executando LSTM...")
    executar_script('main_LSTM.py')

    # Executar main_NHITS.py
    print("Executando NHITS...")
    executar_script('main_NHITS.py')

    # Executar main_GRU.py
    print("Executando NBEATSx...")
    executar_script('main_NBEATSx.py')

    # Executar main_GRU.py
    print("Executando GRU...")
    executar_script('main_GRU.py')

    print('Procurando melhor modelo...')
    encontrar_melhor_modelo()

    # Chamar a função para rodar o modelo vencedor
    print('Executando melhor modelo...')
    rodar_modelo_vencedor()

# Exibir o tempo total de execução
end_time = time.time()
execution_time = end_time - start_time
# Exibir o tempo total de execução em minutos
execution_time_minutes = execution_time / 60
print(f"Tempo de execução total: {execution_time_minutes:.2f} minutos")