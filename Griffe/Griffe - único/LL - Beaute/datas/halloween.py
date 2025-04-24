# halloween_utils.py

import pandas as pd

def process_halloween(df):
    halloween = df.copy()
    halloween.rename(columns={'value': 'halloween'}, inplace=True)

    # Definir o range de dias antes e depois
    days_before = 1
    days_after = 1

    # Lista de datas específicas para o Halloween, desde 2013 até 2025
    specific_dates_halloween = [
        '2013-10-31', '2014-10-31', '2015-10-31', '2016-10-31', '2017-10-31',
        '2018-10-31', '2019-10-31', '2020-10-31', '2021-10-31', '2022-10-31',
        '2023-10-31', '2024-10-31', '2025-10-31'
    ]
    specific_dates_halloween = pd.to_datetime(specific_dates_halloween)

    # Função para definir os valores no intervalo de datas específicas
    def set_values(df, specific_dates, days_before, days_after):
        for specific_date in specific_dates:
            start_range = specific_date - pd.Timedelta(days=days_before)
            end_range = specific_date + pd.Timedelta(days=days_after)
            df.loc[(df['ds'] >= start_range) & (df['ds'] <= end_range), 'halloween'] = 1

    # Aplicar a função ao DataFrame
    set_values(halloween, specific_dates_halloween, days_before, days_after)

    return halloween