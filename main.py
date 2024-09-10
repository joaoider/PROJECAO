import time
from imports import *
from base import data_neural
from model import data_neural_hat

# Começar a contagem do tempo
start_time = time.time()

plot_df = data_neural.copy().reset_index()
#plot_df = data_neural[data_neural['unique_id']=='JJ'].reset_index(drop=True)
#plot_df['unique_id'] = plot_df['unique_id'].astype(object)
#plot_df = data_neural.reset_index(drop=True)

data_neural_hat = data_neural_hat.reset_index(drop=False)
#data_neural_hat = data_neural_hat[data_neural_hat['unique_id']=='JJ']
#data_neural_hat['unique_id'] = data_neural_hat['unique_id'].astype(object)

#print(data_neural_hat)

plot_df = pd.concat([plot_df, data_neural_hat]).set_index('ds') # Concatenate the train and forecast dataframes

# Supondo que a coluna 'ds' esteja como string, primeiro convertemos para datetime
data_neural_hat['ds'] = pd.to_datetime(data_neural_hat['ds'])
# Criar uma nova coluna 'year_month' que contém o ano e o mês
data_neural_hat['year_month'] = data_neural_hat['ds'].dt.to_period('M')
# Agrupar por 'year_month' e somar os valores da coluna 'LSTM'
data_neural_hat2 = data_neural_hat.groupby('year_month')[['LSTM']].sum().reset_index()
#data_neural_hat2 = data_neural_hat.groupby('year_month')[['LSTM', 'GRU', 'NHITS', 'BiTCN', 'NBEATSx']].sum().reset_index()
# Se você quiser salvar o resultado em um arquivo CSV
data_neural_hat2.to_csv('forecast.csv', index=True)

#print(plot_df)
# Salvar o DataFrame plot_df como CSV
plot_df.to_csv('plot_df.csv', index=True)

plot_df[['y', 'LSTM']].plot(linewidth=2)
#plot_df[['y', 'LSTM', 'GRU', 'NHITS', 'BiTCN', 'NBEATSx']].plot(linewidth=2)
plt.ylabel('VLF', fontsize=12)
plt.xlabel('Date', fontsize=12)
plt.grid()
#Salvar o gráfico como uma imagem
plt.savefig('plot_image.png')
#plt.show()

# Exibir o tempo total de execução
end_time = time.time()
execution_time = end_time - start_time
print(f"Tempo de execução: {execution_time:.2f} segundos")