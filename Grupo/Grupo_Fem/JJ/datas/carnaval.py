import pandas as pd

def process_carnaval(df):
    carnaval = df.copy()
    carnaval.rename(columns={'value': 'carnaval'}, inplace=True)

    # Definir o range de dias antes e depois
    days_before = 3
    days_after = 2

    # Lista de datas específicas para o Carnaval conforme fornecido
    specific_dates_carnaval = [
        '2013-02-11', '2014-03-03', '2015-02-16', '2016-02-08', '2017-02-27',
        '2018-02-12', '2019-03-04', '2020-02-24', '2021-02-15', '2022-02-28',
        '2023-02-20', '2024-02-12', '2025-03-04'
    ]
    specific_dates_carnaval = pd.to_datetime(specific_dates_carnaval)

    # Função para definir os valores no intervalo de datas específicas
    def set_values(df, specific_dates, days_before, days_after):
        for specific_date in specific_dates:
            start_range = specific_date - pd.Timedelta(days=days_before)
            end_range = specific_date + pd.Timedelta(days=days_after)
            df.loc[(df['ds'] >= start_range) & (df['ds'] <= end_range), 'carnaval'] = 1

    # Aplicar a função ao DataFrame
    set_values(carnaval, specific_dates_carnaval, days_before, days_after)

    return carnaval