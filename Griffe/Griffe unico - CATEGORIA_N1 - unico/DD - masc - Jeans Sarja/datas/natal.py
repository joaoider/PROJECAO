# natal_utils.py

import pandas as pd

def process_natal(df):
    natal = df.copy()
    natal.rename(columns={'value': 'natal'}, inplace=True)

    # Definir o range de dias antes e depois
    days_before = 7
    days_after = 0

    # Lista de datas específicas para o Natal, desde 2013 até 2025
    specific_dates_natal = [
        '2013-12-25', '2014-12-25', '2015-12-25', '2016-12-25', '2017-12-25',
        '2018-12-25', '2019-12-25', '2020-12-25', '2021-12-25', '2022-12-25',
        '2023-12-25', '2024-12-25', '2025-12-25', '2026-12-25'
    ]
    specific_dates_natal = pd.to_datetime(specific_dates_natal)

    # Função para definir os valores no intervalo de datas específicas
    def set_values(df, specific_dates, days_before, days_after):
        for specific_date in specific_dates:
            start_range = specific_date - pd.Timedelta(days=days_before)
            end_range = specific_date + pd.Timedelta(days=days_after)
            df.loc[(df['ds'] >= start_range) & (df['ds'] <= end_range), 'natal'] = 1

    # Aplicar a função ao DataFrame
    set_values(natal, specific_dates_natal, days_before, days_after)

    return natal