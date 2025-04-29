# MÓDULO BASE
print('base_categoria.py iniciado')

from configuracoes_modelos.imports import *
from unindo_datas import datas
from JJ_configuracoes import marca, horizon, freq, data_inicio_base, data_final_base, data_train, data_test, data_inicio_futr_test, data_final_futr_test, data_inicio_futr, data_final_futr
from funcoes import verificar_e_completar_datas_faltantes
from querys.JJ_query_databricks import data

print(data.head())
#path = 'bases/base_LL.csv'
#data = pd.read_csv(path)

# Processar o DataFrame como no código original
data = data.drop(columns=['MARCA_SIGLA', 'GRIFFE', 'CODIGO_FILIAL', 'CANAL_ORIGEM', 'CIDADE', 'UF', 'STATUS_PRODUTO', 'TIPO_VENDA', 'LINHA', 'GRUPO', 'MEDIA_VLF', 'MEDIA_QLF', 'MEDIA_ROL', 'MEDIA_CPV'])

data['DATA'] = pd.to_datetime(data['DATA'])
data = data.loc[data['DATA'] >= data_inicio_base]

data['VLF'] = data['VLF'].astype(float)
data['QLF'] = data['QLF'].astype(float)
data['ROL'] = data['ROL'].astype(float)
data['CPV'] = data['CPV'].astype(float)
data['CATEGORIA_N1'] = data['CATEGORIA_N1'].astype(object)

data.rename(columns={'CATEGORIA_N1': 'unique_id'}, inplace=True)

## Agrupando por data e somando as colunas VLF e QLF
# Agrupando por DATA e unique_id e somando as colunas VLF, QLF, ROL e CPV
data = data.groupby(['DATA', 'unique_id']).agg({
    'VLF': 'sum',
    'QLF': 'sum',
    'ROL': 'sum',
    'CPV': 'sum'
}).reset_index()
#data = data.groupby('DATA').agg({'VLF': 'sum', 'QLF': 'sum', 'ROL': 'sum', 'CPV': 'sum'}).reset_index()
data = data.sort_values(by='DATA').reset_index(drop=True)

#data['unique_id'] = marca  # Usar a marca atual
#data['unique_id'] = data['unique_id'].astype(object)

# Gerar os próximos 365 dias
#ultimo_valor = data.index[-1]
#proximos_365_dias = pd.date_range(start=ultimo_valor, periods=horizon, freq=freq)[1:]
#data_previsao = pd.DataFrame(proximos_365_dias, columns=['DATA_VENDA'])
#data_previsao.reset_index(drop=True, inplace=True)

# Criar o DataFrame data_neural_marca
data_neural = data.copy().reset_index()
data_neural.rename(columns={'DATA': 'ds', 'VLF': 'y'}, inplace=True)
data_neural = data_neural[['ds', 'unique_id', 'y', 'QLF', 'ROL', 'CPV']]



# Plot the graph
plt.plot(data_neural['ds'], data_neural['y'])
plt.xlabel('DATA')
plt.ylabel('VLF')
plt.title('VLF by DATA')
plt.savefig(f'outputs/base_{marca}_categoria_moda.png')


############################################################################# Criando Static_df
# Extraindo os valores únicos da coluna 'unique_id'
unique_ids = data_neural['unique_id'].unique()
print(unique_ids)
# Criando um DataFrame de zeros para o número de mercados
num_markets = len(unique_ids)  # Defina quantos mercados você quer
print(num_markets)
# Criar a matriz identidade com NumPy
identity_matrix = np.eye(num_markets, dtype=int)
# Criar o DataFrame com a matriz identidade
static_df = pd.DataFrame(identity_matrix, index=unique_ids, columns=[f'market_{i}' for i in range(num_markets)])
print(static_df)
# Adicionar a coluna 'unique_id' como índice
static_df.index.name = 'unique_id'
print(static_df)
"""
static_df = pd.DataFrame(0, index=range(len(unique_ids)), columns=['unique_id'] + [f'market_{i}' for i in range(num_markets)])
# Preenchendo a coluna 'unique_id' com os valores únicos
static_df['unique_id'] = unique_ids
"""
#print(static_df)





##################################################### Verificando datas faltantes
# Verificar datas faltantes
data_neural = verificar_e_completar_datas_faltantes(data_neural)




################################### Fazendo merge da base com datas feriados liquidações etc
data_neural = pd.merge(data_neural, datas, on=['ds'])



############################################ Criando base para previsão futura
# Fixando tudo para referencia de fim de setembro 2024!
data_neural = data_neural[data_neural['ds'] <= '2024-12-31'] # a base só está indo até essa data, é só pra confirmar
#print(len(data_neural))

futr_df = datas[(datas['ds'] >= '2025-01-01') & (datas['ds'] <= '2025-12-31')]
#print(data_neural.head())
#print(futr_df.head())
#print('len(futr_df) antes do merge:', len(futr_df))
# Criar um DataFrame com todas as combinações de 'ds' e 'unique_id'
futr_df = futr_df.assign(key=1).merge(pd.DataFrame({'unique_id': unique_ids, 'key': 1}), on='key').drop('key', axis=1)
futr_df = futr_df.sort_values(by=['unique_id', 'ds']).reset_index(drop=True)
#print('len(futr_df) depois do merge:', len(futr_df))
#print(futr_df)



######################################### Criando base para previsão de treino e teste
data_neural_train = data_neural[data_neural['ds'] <= '2023-12-31']
#print(data_neural_train.head())
data_neural_test = data_neural[(data_neural['ds'] >= '2024-01-01') & (data_neural['ds'] < '2024-12-31')]
#print(data_neural_test.head())
print('len(data_neural_test) antes do merge:', len(data_neural_test))
# Criar um DataFrame com todas as combinações de 'ds' e 'unique_id'
#data_neural_test = data_neural_test.assign(key=1).merge(pd.DataFrame({'unique_id': unique_ids, 'key': 1}), on='key').drop('key', axis=1)
data_neural_test = data_neural_test.sort_values(by=['unique_id', 'ds']).reset_index(drop=True)
print('len(data_neural_test) depois do merge:', len(data_neural_test))



#futr_df['unique_id'] = marca  # Usar a marca atual
#futr_df['unique_id'] = futr_df['unique_id'].astype(object)
#futr_df_test = datas[(datas['ds'] >= '2023-10-01') & (datas['ds'] < '2024-09-30')]
#futr_df_test['unique_id'] = marca  # Usar a marca atual
#futr_df_test['unique_id'] = futr_df_test['unique_id'].astype(object)



"""
# Calcular a data limite
data_inicio = datetime.now()
data_limite = datetime.now() + timedelta(days=horizon)

data_inicio = data_inicio.strftime('%Y-%m-%d')
data_limite = data_limite.strftime('%Y-%m-%d')

data_inicio_back = datetime.now() - timedelta(days=horizon+1)
data_limite_back = datetime.now()
data_inicio_back = data_inicio_back.strftime('%Y-%m-%d')
data_limite_back = data_limite_back.strftime('%Y-%m-%d')

# Para fazer validação vou limitar a base de dados até 1 ano atrás, essa será a base de treino
data_neural_train = data_neural[data_neural['ds'] < data_inicio_back]

data_neural_test = data_neural[(data_neural['ds'] >= data_inicio_back) & (data_neural['ds'] < data_inicio)]

#ajuste
data_inicio_ajuste = datetime.now() - timedelta(days=1)
data_inicio_ajuste = data_inicio_ajuste.strftime('%Y-%m-%d')
## Filtrar o DataFrame para as datas futuras
futr_df = datas[(datas['ds'] >= data_inicio_ajuste) & (datas['ds'] < data_limite)]
futr_df['unique_id'] = marca  # Usar a marca atual
futr_df['unique_id'] = futr_df['unique_id'].astype(object)

# Filtrar o DataFrame para as datas futuras
# base de teste
futr_df_test = datas[(datas['ds'] >= data_inicio_back) & (datas['ds'] < data_inicio)]
futr_df_test['unique_id'] = marca  # Usar a marca atual
futr_df_test['unique_id'] = futr_df_test['unique_id'].astype(object)
"""



#print('data geral', data_neural['ds'].max())
#print('futr geral', futr_df['ds'].min(), futr_df['ds'].max())

#print('data train', data_neural_train['ds'].max())
#print('futr geral test', data_neural_test['ds'].min(), data_neural_test['ds'].max())

print('base_categoria.py finalizado')