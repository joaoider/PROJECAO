# MÓDULO PRINCIPAL

print('main.py iniciado')

import importlib
from imports import *
from base import data_neural
from configuracoes import marca, modelo

print('marca: ', marca)
print('modelos utilizados: ', modelo)
print('###############################')

# Dicionário que mapeia o nome do modelo para o módulo correspondente
modelos_disponiveis = {
    'LSTM': 'models.model_LSTM',
    'NHITS': 'models.model_NHITS',
    'BiTCN': 'models.model_BiTCN',
    'GRU': 'models.model_GRU',
    'NBEATSx': 'models.model_NBEATSx'
}

# Inicializa a variável para armazenar o dataframe final
data_neural_hat_final = None

# Itera pelos modelos definidos na variável 'modelo'
for modelo_escolhido in modelo:
    if modelo_escolhido in modelos_disponiveis:
        # Carrega o módulo dinamicamente
        modulo_modelo = importlib.import_module(modelos_disponiveis[modelo_escolhido])
        
        # Acessa o dataframe específico dentro do módulo carregado
        data_neural_hat = getattr(modulo_modelo, 'data_neural_hat')
        
        # Renomeia a coluna de previsões com o nome do modelo escolhido
        #data_neural_hat.rename(columns={'previsao': modelo_escolhido}, inplace=True)  # Supondo que a coluna de previsões se chame 'previsao'
        
        # Se for o primeiro dataframe, ele se torna o dataframe final
        if data_neural_hat_final is None:
            data_neural_hat_final = data_neural_hat
        else:
            # Faz o merge dos dataframes com base nas colunas 'unique_id' e 'ds'
            data_neural_hat_final = data_neural_hat_final.merge(data_neural_hat, on=['unique_id', 'ds'], how='inner')
    else:
        print(f"O modelo '{modelo_escolhido}' não está disponível.")

# Ao final, o dataframe data_neural_hat_final terá as colunas 'unique_id', 'ds' e as previsões de cada modelo

print('dataframe modelo')
print(data_neural_hat_final.head())

#print(data_neural_hat.head(1))

# Começar a contagem do tempo
start_time = time.time()

plot_df = data_neural.copy().reset_index()
#plot_df = data_neural[data_neural['unique_id']=='JJ'].reset_index(drop=True)
#plot_df['unique_id'] = plot_df['unique_id'].astype(object)
#plot_df = data_neural.reset_index(drop=True)

data_neural_hat_final = data_neural_hat_final.reset_index(drop=False)
#data_neural_hat = data_neural_hat[data_neural_hat['unique_id']=='JJ']
#data_neural_hat['unique_id'] = data_neural_hat['unique_id'].astype(object)

#print(data_neural_hat)

plot_df = pd.concat([plot_df, data_neural_hat_final]).set_index('ds') # Concatenate the train and forecast dataframes

# Supondo que a coluna 'ds' esteja como string, primeiro convertemos para datetime
data_neural_hat_final['ds'] = pd.to_datetime(data_neural_hat_final['ds'])
# Criar uma nova coluna 'year_month' que contém o ano e o mês
data_neural_hat_final['year_month'] = data_neural_hat_final['ds'].dt.to_period('M')
# Agrupar por 'year_month' e somar os valores da coluna 'LSTM'
# Faz o groupby usando a variável modelo
data_neural_hat2 = data_neural_hat_final.groupby('year_month')[modelo].sum().reset_index()
#data_neural_hat2 = data_neural_hat.groupby('year_month')[['LSTM', 'GRU', 'NHITS', 'BiTCN', 'NBEATSx']].sum().reset_index()
# Se você quiser salvar o resultado em um arquivo CSV
data_neural_hat2.to_csv('outputs/forecast.csv', index=True)

#print(plot_df)
# Salvar o DataFrame plot_df como CSV
plot_df.to_csv('outputs/plot_df.csv', index=True)

# Adiciona 'y' à lista de colunas que você quer plotar
colunas_para_plotar = ['y'] + modelo
plot_df[colunas_para_plotar].plot(linewidth=2)
#plot_df[['y', 'LSTM', 'GRU', 'NHITS', 'BiTCN', 'NBEATSx']].plot(linewidth=2)
plt.ylabel('VLF', fontsize=12)
plt.xlabel('Date', fontsize=12)
plt.grid()
#Salvar o gráfico como uma imagem
plt.savefig('outputs/plot_image.png')
#plt.show()

# Exibir o tempo total de execução
end_time = time.time()
execution_time = end_time - start_time
print(f"Tempo de execução: {execution_time:.2f} segundos")

print('main.py finalizado')