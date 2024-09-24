# MÓDULO BASE
print('base.py iniciado')

from imports import *
from unindo_datas import datas
from configuracoes import marca, horizon, freq
from querys.query_base import dataframes  # Agora importa o dicionário com os DataFrames

# Garantir que a variável marca seja uma lista
if isinstance(marca, str):
    marca = [marca]  # Se for string, transformar em lista

# Dicionário para armazenar os DataFrames finais
data_neural_dfs = {}
futr_df_dfs = {}

# Iterar sobre as marcas
for m in marca:
    # Pegar o DataFrame correspondente da marca no dicionário
    data = dataframes.get(f'data_{m}')

    if data is not None:
        # Processar o DataFrame como no código original
        data = data.drop(columns=['MARCA_SIGLA', 'GRIFFE', 'CODIGO_FILIAL', 'CANAL_ORIGEM', 'CIDADE', 'UF', 'STATUS_PRODUTO', 'TIPO_VENDA', 'LINHA', 'GRUPO'])

        data['DATA'] = pd.to_datetime(data['DATA'])
        data = data.loc[data['DATA'] >= data_inicio_base]

        data['VLF'] = data['VLF'].astype(float)
        data['QLF'] = data['QLF'].astype(float)

        # Agrupando por data e somando as colunas VLF e QLF
        data = data.groupby('DATA').agg({'VLF': 'sum', 'QLF': 'sum'}).reset_index()
        data = data.sort_values(by='DATA').reset_index(drop=True)

        data['unique_id'] = m  # Usar a marca atual
        data['unique_id'] = data['unique_id'].astype(object)

        # Gerar os próximos 365 dias
        ultimo_valor = data.index[-1]
        proximos_365_dias = pd.date_range(start=ultimo_valor, periods=horizon, freq=freq)[1:]

        data_previsao = pd.DataFrame(proximos_365_dias, columns=['DATA_VENDA'])
        data_previsao.reset_index(drop=True, inplace=True)

        # Criar o DataFrame `data_neural_marca`
        data_neural = data.copy().reset_index()
        data_neural.rename(columns={'DATA': 'ds', 'VLF': 'y'}, inplace=True)
        data_neural = data_neural[['ds', 'unique_id', 'y', 'QLF']]
        data_neural = pd.merge(data_neural, datas, on=['ds'])

        # Calcular a data limite
        data_inicio = datetime.now()
        data_limite = datetime.now() + timedelta(days=horizon)

        data_inicio = data_inicio.strftime('%Y-%m-%d')
        data_limite = data_limite.strftime('%Y-%m-%d')

        # Filtrar o DataFrame para as datas futuras
        futr_df = datas[(datas['ds'] >= data_inicio) & (datas['ds'] <= data_limite)]
        futr_df['unique_id'] = m  # Usar a marca atual
        futr_df['unique_id'] = futr_df['unique_id'].astype(object)

        # Armazenar os DataFrames no dicionário
        data_neural_dfs[f'data_neural_{m}'] = data_neural
        futr_df_dfs[f'futr_df_{m}'] = futr_df

        # Exibir as primeiras linhas dos DataFrames criados
        print(f"\nDataFrame data_neural_{m}:")
        print(data_neural.head(1))
        print(f"\nDataFrame futr_df_{m}:")
        print(futr_df.head(1))

# Agora você tem os DataFrames `data_neural_marca` e `futr_df_marca` armazenados nos dicionários `data_neural_dfs` e `futr_df_dfs`.

print('base.py finalizado')