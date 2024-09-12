# MÓDULO BASE

from imports import *
from unindo_datas import datas
from configuracoes import marca, horizon, freq
from query_base import data, path, data_inicio_base

# depois retirar esse comando pois puxarei direto a base em pandas.
#data = pd.read_csv(path)

data = data.drop(columns=['MARCA_SIGLA'])
#data.rename(columns={'MARCA_SIGLA': 'unique_id'}, inplace=True)
data = data.drop(columns=['GRIFFE'])
#data.rename(columns={'GRIFFE': 'unique_id'}, inplace=True)
data = data.drop(columns=['CODIGO_FILIAL'])
data = data.drop(columns=['CANAL_ORIGEM'])
data = data.drop(columns=['CIDADE'])
data = data.drop(columns=['UF'])
data = data.drop(columns=['STATUS_PRODUTO'])
data = data.drop(columns=['TIPO_VENDA'])
data = data.drop(columns=['LINHA'])
data = data.drop(columns=['GRUPO'])

data['DATA'] = pd.to_datetime(data['DATA'])
data = data.loc[data['DATA'] >= data_inicio_base]

# Definir a coluna 'DATA_DTTIME' como índice
#data.set_index('DATA', inplace=True)
data['VLF'] = data['VLF'].astype(float)
data['QLF'] = data['QLF'].astype(float)

# Agrupando por data e somando as colunas VLF e QLF
data = data.groupby('DATA').agg({'VLF': 'sum', 'QLF': 'sum'}).reset_index()
# Ordenando o DataFrame por data em ordem crescente
data = data.sort_values(by='DATA').reset_index(drop=True)

data['unique_id'] = marca
data['unique_id'] = data['unique_id'].astype(object)

# Pegando o último valor do índice DATA_DTTIME
ultimo_valor = data.index[-1]

# Gerando os próximos 365 dias a partir do último valor
proximos_365_dias = pd.date_range(start=ultimo_valor, periods=horizon, freq=freq)[1:]

# Criando um novo dataframe com esses 365 valores
data_previsao = pd.DataFrame(proximos_365_dias, columns=['DATA_VENDA'])

# Resetando o índice
data_previsao.reset_index(drop=True, inplace=True)


#print(data_previsao)

data_neural = data.copy().reset_index()
data_neural.rename(columns={'DATA': 'ds', 'VLF': 'y'}, inplace=True)
#data_neural = data_neural.drop(columns=['Média_Móvel_30'])
#data_neural['unique_id'] = 'JJ'
#data_neural['unique_id'] = data_neural['unique_id'].astype(object)
data_neural = data_neural[['ds', 'unique_id', 'y', 'QLF']] #, 'CANAL_ORIGEM', 'LINHA', 'GRUPO', 'TIPO_VENDA', 'STATUS_PRODUTO', 'CIDADE', 'UF', 'GRIFFE']]
#data_neural

data_neural = pd.merge(data_neural, datas, on=['ds'])

# Calcular a data limite
data_inicio = datetime.now()
data_limite = datetime.now() + timedelta(days=horizon)

# Formatar as datas no formato 'yyyy-mm-dd'
data_inicio = data_inicio.strftime('%Y-%m-%d')
print('data_inicio', data_inicio)
data_limite = data_limite.strftime('%Y-%m-%d')
print('data_limite', data_limite)

#data_inicio, data_limite

# Filtrar o DataFrame para manter apenas as datas a partir da data limite
futr_df = datas[(datas['ds'] >= data_inicio) & (datas['ds'] <= data_limite)]

futr_df['unique_id'] = marca
futr_df['unique_id'] = futr_df['unique_id'].astype(object)

#print('futr_df')
#print(futr_df)