# diadosnamorados_utils.py

import pandas as pd

def process_dia_dos_namorados(df):
    diadosnamorados = df.copy()
    diadosnamorados.rename(columns={'value': 'dia_dos_namorados'}, inplace=True)

    # Definir o range de dias antes e depois
    days_before = 7
    days_after = 1

    # Lista de datas específicas para o Dia dos Namorados
    specific_dates_namorados = [
        '2013-06-12', '2014-06-12', '2015-06-12', '2016-06-12', '2017-06-12',
        '2018-06-12', '2019-06-12', '2020-06-12', '2021-06-12', '2022-06-12',
        '2023-06-12', '2024-06-12', '2025-06-12', '2026-06-12'
    ]
    specific_dates_namorados = pd.to_datetime(specific_dates_namorados)

    # Função para definir os valores no intervalo de datas específicas
    def set_values(df, specific_dates, days_before, days_after):
        for specific_date in specific_dates:
            start_range = specific_date - pd.Timedelta(days=days_before)
            end_range = specific_date + pd.Timedelta(days=days_after)
            df.loc[(df['ds'] >= start_range) & (df['ds'] <= end_range), 'dia_dos_namorados'] = 1

    # Aplicar a função ao DataFrame
    set_values(diadosnamorados, specific_dates_namorados, days_before, days_after)

    return diadosnamorados