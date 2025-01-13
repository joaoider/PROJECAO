# blackfriday_utils.py

import pandas as pd

def process_black_friday(df):
    blackfriday = df.copy()
    blackfriday.rename(columns={'value': 'black_friday'}, inplace=True)

    # Definir o range de dias antes e depois
    days_before = 1
    days_after = 1

    # Lista de datas específicas para a Black Friday, desde 2013 até 2025
    specific_dates_blackfriday = [
        '2013-11-29', '2014-11-28', '2015-11-27', '2016-11-25', '2017-11-24',
        '2018-11-23', '2019-11-29', '2020-11-27', '2021-11-26', '2022-11-25',
        '2023-11-24', '2024-11-29', '2025-11-28'
    ]
    specific_dates_blackfriday = pd.to_datetime(specific_dates_blackfriday)

    # Função para definir os valores no intervalo de datas específicas
    def set_values(df, specific_dates, days_before, days_after):
        for specific_date in specific_dates:
            start_range = specific_date - pd.Timedelta(days=days_before)
            end_range = specific_date + pd.Timedelta(days=days_after)
            df.loc[(df['ds'] >= start_range) & (df['ds'] <= end_range), 'black_friday'] = 1

    # Aplicar a função ao DataFrame
    set_values(blackfriday, specific_dates_blackfriday, days_before, days_after)

    return blackfriday