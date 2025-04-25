# MÓDULO BASE
print('base.py iniciado')

from configuracoes_modelos.imports import *
from unindo_datas import datas
from JJ_configuracoes import marca, horizon, freq, data_inicio_base, data_final_base, data_train, data_test, data_inicio_futr_test, data_final_futr_test, data_inicio_futr, data_final_futr
from funcoes import verificar_e_completar_datas_faltantes_sem_unique_id
from querys.JJ_query_databricks import data

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

## Agrupando por data e somando as colunas VLF e QLF
data = data.groupby('DATA').agg({'VLF': 'sum', 'QLF': 'sum', 'ROL': 'sum', 'CPV': 'sum'}).reset_index()
data = data.sort_values(by='DATA').reset_index(drop=True)

data['unique_id'] = marca  # Usar a marca atual
data['unique_id'] = data['unique_id'].astype(object)

# Gerar os próximos 365 dias
#ultimo_valor = data.index[-1]
#proximos_365_dias = pd.date_range(start=ultimo_valor, periods=horizon, freq=freq)[1:]

#data_previsao = pd.DataFrame(proximos_365_dias, columns=['DATA_VENDA'])
#data_previsao.reset_index(drop=True, inplace=True)

# Criar o DataFrame data_neural_marca
data_neural = data.copy().reset_index()
data_neural.rename(columns={'DATA': 'ds', 'VLF': 'y'}, inplace=True)
data_neural = data_neural[['ds', 'unique_id', 'y', 'QLF', 'ROL', 'CPV']]

print('infos')
print(len(data_neural))
print(data_neural['ds'].min(), data_neural['ds'].max())

##################################################### Verificando datas faltantes
# Verificar datas faltantes
#data_neural = verificar_e_completar_datas_faltantes_sem_unique_id(data_neural)

data_neural['ds'] = pd.to_datetime(data_neural['ds'])
data_neural['y'] = data_neural['y'].astype(float)
data_neural['QLF'] = data_neural['QLF'].astype(float)
data_neural['ROL'] = data_neural['ROL'].astype(float)
data_neural['CPV'] = data_neural['CPV'].astype(float)
data_neural['unique_id'] = data_neural['unique_id'].astype(object)


########################################## Fazendo merge
data_neural = pd.merge(data_neural, datas, on=['ds'])


# Plot the graph
plt.plot(data_neural['ds'], data_neural['y'])
plt.xlabel('DATA')
plt.ylabel('VLF')
plt.title('VLF by DATA')
plt.savefig(f'outputs/base_{marca}.png')


# Fixando tudo para referencia de fim de setembro 2024!
data_neural = data_neural[data_neural['ds'] <= data_final_base]
#data_neural_filtered = data_neural[data_neural['ds'] <= '2024-09-30']
data_neural_train = data_neural[data_neural['ds'] <= data_train]
data_neural_test = data_neural[(data_neural['ds'] >= data_test) & (data_neural['ds'] <= data_final_base)]

#data_neural = data_neural[data_neural['ds'] <= '2024-09-30']
#data_neural_train = data_neural[data_neural['ds'] <= '2023-09-30']
print('data_neural_train')
print(data_neural_train.head())
#data_neural_test = data_neural[(data_neural['ds'] >= '2023-10-01') & (data_neural['ds'] <= '2024-09-30')]
print('data_neural_test')
print(data_neural_test.head())
print('columns', data_neural_test.columns)
#print(data_neural_test['QLF'])


futr_df = datas[(datas['ds'] >= data_inicio_futr) & (datas['ds'] <= data_final_futr)]
futr_df['unique_id'] = marca  # Usar a marca atual
futr_df['unique_id'] = futr_df['unique_id'].astype(object)
futr_df_test = datas[(datas['ds'] >= data_inicio_futr_test) & (datas['ds'] < data_final_futr_test)]
futr_df_test['unique_id'] = marca  # Usar a marca atual
futr_df_test['unique_id'] = futr_df_test['unique_id'].astype(object)


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
#print('futr geral test', futr_df_test['ds'].min(), futr_df_test['ds'].max())

print('base.py finalizado')