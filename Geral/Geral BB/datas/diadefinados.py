# diadefinados_utils.py

import pandas as pd

def process_dia_de_finados(df):
    dia_de_finados = df.copy()
    dia_de_finados.rename(columns={'value': 'dia_de_finados'}, inplace=True)

    # Intervalo de dias antes e depois é 0 para ambos, conforme especificado
    days_before = 0
    days_after = 0

    # Lista de datas específicas para o Dia de Finados conforme fornecido
    specific_dates_dia_de_finados = [
        '2013-11-02', '2014-11-02', '2015-11-02', '2016-11-02', '2017-11-02',
        '2018-11-02', '2019-11-02', '2020-11-02', '2021-11-02', '2022-11-02',
        '2023-11-02', '2024-11-02', '2025-11-02', '2026-11-02'
    ]
    specific_dates_dia_de_finados = pd.to_datetime(specific_dates_dia_de_finados)

    # Função para definir os valores no intervalo de datas específicas
    def set_values(df, specific_dates, days_before, days_after):
        for specific_date in specific_dates:
            start_range = specific_date - pd.Timedelta(days=days_before)
            end_range = specific_date + pd.Timedelta(days=days_after)
            df.loc[(df['ds'] >= start_range) & (df['ds'] <= end_range), 'dia_de_finados'] = 1

    # Aplicar a função ao DataFrame
    set_values(dia_de_finados, specific_dates_dia_de_finados, days_before, days_after)

    return dia_de_finados