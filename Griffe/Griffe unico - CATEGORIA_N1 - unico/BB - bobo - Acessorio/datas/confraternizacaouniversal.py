# confraternizacao_universal_utils.py

import pandas as pd

def process_confraternizacao_universal(df):
    confraternizacao_universal = df.copy()
    confraternizacao_universal.rename(columns={'value': 'confraternizacao_universal'}, inplace=True)

    # Definir o range de dias antes e depois
    days_before = 1
    days_after = 0

    # Lista de datas específicas para a Confraternização Universal conforme fornecido
    specific_dates_confraternizacao_universal = [
        '2013-01-01', '2014-01-01', '2015-01-01', '2016-01-01', '2017-01-01',
        '2018-01-01', '2019-01-01', '2020-01-01', '2021-01-01', '2022-01-01',
        '2023-01-01', '2024-01-01', '2025-01-01', '2026-01-01'
    ]
    specific_dates_confraternizacao_universal = pd.to_datetime(specific_dates_confraternizacao_universal)

    # Função para definir os valores no intervalo de datas específicas
    def set_values(df, specific_dates, days_before, days_after):
        for specific_date in specific_dates:
            start_range = specific_date - pd.Timedelta(days=days_before)
            end_range = specific_date + pd.Timedelta(days=days_after)
            df.loc[(df['ds'] >= start_range) & (df['ds'] <= end_range), 'confraternizacao_universal'] = 1

    # Aplicar a função ao DataFrame
    set_values(confraternizacao_universal, specific_dates_confraternizacao_universal, days_before, days_after)

    return confraternizacao_universal