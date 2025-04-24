# diadospais_utils.py

import pandas as pd

def process_dia_dos_pais(df):
    diadospais = df.copy()
    diadospais.rename(columns={'value': 'dia_dos_pais'}, inplace=True)

    # Definir o range de dias antes e depois
    days_before = 7
    days_after = 1

    # Lista de datas específicas
    specific_dates = [
        '2013-08-11', '2014-08-10', '2015-08-09', '2016-08-14', '2017-08-13',
        '2018-08-12', '2019-08-11', '2020-08-09', '2021-08-08', '2022-08-14',
        '2023-08-13', '2024-08-11', '2025-08-10'
    ]
    specific_dates = pd.to_datetime(specific_dates)

    # Função para definir os valores no intervalo de datas específicas
    def set_values(df, specific_dates, days_before, days_after):
        for specific_date in specific_dates:
            start_range = specific_date - pd.Timedelta(days=days_before)
            end_range = specific_date + pd.Timedelta(days=days_after)
            df.loc[(df['ds'] >= start_range) & (df['ds'] <= end_range), 'dia_dos_pais'] = 1

    # Aplicar a função ao DataFrame
    set_values(diadospais, specific_dates, days_before, days_after)

    return diadospais