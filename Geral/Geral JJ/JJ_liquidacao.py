import pandas as pd
#path_liqui = 'bases/base_liqui_LL.csv'
#data_liqui = pd.read_csv(path_liqui)

from querys.JJ_query_databricks import data_liqui


print('data_liqui', data_liqui)

data_liqui['DATA_INICIO_LIQUIDACAO'] = pd.to_datetime(data_liqui['DATA_INICIO_LIQUIDACAO'])

# Ordenar o DataFrame pela coluna 'date_column'
data_liqui = data_liqui.sort_values(by='DATA_INICIO_LIQUIDACAO')

# Resetar o índice após a ordenação
data_liqui = data_liqui.reset_index(drop=True)

liqui_datas = data_liqui['DATA_INICIO_LIQUIDACAO'].tolist()
liqui_datas

def process_liquidacao(df, liqui_datas):
    liquidacao = df.copy()
    liquidacao.rename(columns={'value': 'liquidacao'}, inplace=True)

    # Definir o range de dias antes e depois
    days_before = 15
    days_after = 1

    # Função para definir os valores no intervalo de datas específicas
    def set_values(df, specific_dates, days_before, days_after):
        for specific_date in specific_dates:
            start_range = specific_date - pd.Timedelta(days=days_before)
            end_range = specific_date + pd.Timedelta(days=days_after)
            df.loc[(df['ds'] >= start_range) & (df['ds'] <= end_range), 'liquidacao'] = 1

    # Aplicar a função ao DataFrame
    set_values(liquidacao, liqui_datas, days_before, days_after)

    return liquidacao