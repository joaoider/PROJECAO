# MÓDULO PRINCIPAL

from imports import *
from unindo_datas import datas
from configuracoes import path, marca, horizon, freq, data_inicio_base

data = pd.read_csv(path)

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

# Definindo os dados
#static_dict = {
#    'unique_id': ['Dudalina Masc', 'Dudalina Fem'],
#    'market_0': [1, 0],
#    'market_1': [0, 1]
#}
#static_df = pd.DataFrame(static_dict)

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

#print(data)
#exit()
#print(static_df)

#data['CODIGO_FILIAL'] = data['CODIGO_FILIAL'].astype(object)
#Retirado por enquanto porque deve ter algum erro. São quase 200 lojas.
#data = data.drop(columns=['CODIGO_FILIAL'])


#data['CANAL_ORIGEM'] = data['CANAL_ORIGEM'].astype(object)
#data['LINHA'] = data['LINHA'].astype(object)
#data['GRUPO'] = data['GRUPO'].astype(object)
#data['TIPO_VENDA'] = data['TIPO_VENDA'].astype(object)
#data['STATUS_PRODUTO'] = data['STATUS_PRODUTO'].astype(object)
#data['CIDADE'] = data['CIDADE'].astype(object)
#data['UF'] = data['UF'].astype(object)
#data['GRIFFE'] = data['GRIFFE'].astype(object)
# Calcular a média móvel de 3 dias (ajuste conforme necessário)
#data['Média_Móvel_30'] = data['VLF'].rolling(window=30).mean()


# Renomeando a coluna 'old_column_name' para 'new_column_name'
#data.rename(columns={'GRIFFE': 'unique_id'}, inplace=True)

#print(data.head())

"""
# Ajustar o valor de 'agg.path.chunksize' e 'path.simplify_threshold'
mpl.rcParams['agg.path.chunksize'] = 10000  # Aumenta o limite de segmentos por chunk
mpl.rcParams['path.simplify_threshold'] = 1.0  # Ajusta o limiar de simplificação
# Plotar o dataframe e a média móvel
plt.figure(figsize=(10, 6))
plt.plot(data.index, data['VLF'], label='Valor de Venda')
plt.plot(data.index, data['Média_Móvel_30'], label='Média Móvel 30', color="firebrick")
plt.xlabel('Data')
plt.ylabel('Valor de Venda')
plt.title('Valor de Venda por Data')
plt.grid(True)
plt.xticks(rotation=45)
plt.legend()
plt.tight_layout()

# Salvar o gráfico como uma imagem
plt.savefig('history.png')

# Mostrar o gráfico (opcional)
# plt.show()
"""

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

#data_neural.rename(columns={'DATA': 'ds', 'VLF': 'y'}, inplace=True)
#data_neural = data_neural.drop(columns=['date'])
#print('data_neural')
#print(data_neural.head())

#data_neural = data_neural.drop(columns=['MARCA_SIGLA'])
#data_neural['unique_id'] = 'JJ'
#data_neural['unique_id'] = data_neural['unique_id'].astype(object)

#data_neural = data_neural.drop(columns=['CANAL_ORIGEM', 'LINHA', 'GRUPO', 'TIPO_VENDA', 'STATUS_PRODUTO', 'CIDADE', 'UF', 'GRIFFE'])
#print('data neural')
#print(data_neural)
"""
# Criar a lista com o prefixo "CANAL_ORIGEM_" antes de cada nome
canal_origem_nomes = ["CANAL_ORIGEM_" + str(nome) for nome in data_neural['CANAL_ORIGEM']]
canal_origem_linha = ["LINHA" + str(nome) for nome in data_neural['LINHA']]
canal_origem_grupo = ["GRUPO" + str(nome) for nome in data_neural['GRUPO']]
canal_origem_tipo_venda = ["TIPO_VENDA" + str(nome) for nome in data_neural['TIPO_VENDA']]
canal_origem_status_produto = ["STATUS_PRODUTO" + str(nome) for nome in data_neural['STATUS_PRODUTO']]
canal_origem_cidade = ["CIDADE" + str(nome) for nome in data_neural['CIDADE']]
canal_origem_uf = ["UF" + str(nome) for nome in data_neural['UF']]
canal_origem_griffe = ["GRIFFE" + str(nome) for nome in data_neural['GRIFFE']]

# As colunas de interesse
cols_to_transform = ['CANAL_ORIGEM', 'LINHA', 'GRUPO', 'TIPO_VENDA',
                     'STATUS_PRODUTO', 'CIDADE', 'UF', 'GRIFFE']
# Aplicar One-Hot Encoding nas colunas especificadas
data_neural = pd.get_dummies(data_neural, columns = cols_to_transform)

# Garantir que as colunas criadas com os nomes gerados sejam convertidas para inteiros
data_neural[canal_origem_nomes] = data_neural[canal_origem_nomes].astype(int)
data_neural[canal_origem_linha] = data_neural[canal_origem_linha].astype(int)
data_neural[canal_origem_grupo] = data_neural[canal_origem_grupo].astype(int)
data_neural[canal_origem_tipo_venda] = data_neural[canal_origem_tipo_venda].astype(int)
data_neural[canal_origem_status_produto] = data_neural[canal_origem_status_produto].astype(int)
data_neural[canal_origem_cidade] = data_neural[canal_origem_cidade].astype(int)
data_neural[canal_origem_uf] = data_neural[canal_origem_uf].astype(int)
data_neural[canal_origem_griffe] = data_neural[canal_origem_griffe].astype(int)

#print(data_neural.columns)
#print(data_neural)
"""

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