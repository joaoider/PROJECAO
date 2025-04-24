# diadasmaes_utils.py

import pandas as pd

def process_dia_das_maes(df):
    diadasmaes = df.copy()
    diadasmaes.rename(columns={'value': 'dia_das_maes'}, inplace=True)

    # Definir o range de dias antes e depois
    days_before = 7
    days_after = 1

    # Lista de datas específicas
    specific_dates = [
        '2013-05-12', '2014-05-11', '2015-05-10', '2016-05-08', '2017-05-14',
        '2018-05-13', '2019-05-12', '2020-05-10', '2021-05-09', '2022-05-08',
        '2023-05-14', '2024-05-12', '2025-05-11'
    ]
    specific_dates = pd.to_datetime(specific_dates)

    # Função para definir os valores no intervalo de datas específicas
    def set_values(df, specific_dates, days_before, days_after):
        for specific_date in specific_dates:
            start_range = specific_date - pd.Timedelta(days=days_before)
            end_range = specific_date + pd.Timedelta(days=days_after)
            df.loc[(df['ds'] >= start_range) & (df['ds'] <= end_range), 'dia_das_maes'] = 1

    # Aplicar a função ao DataFrame
    set_values(diadasmaes, specific_dates, days_before, days_after)

    return diadasmaes