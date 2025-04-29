# diadotrabalhador_utils.py

import pandas as pd

def process_dia_do_trabalhador(df):
    dia_do_trabalhador = df.copy()
    dia_do_trabalhador.rename(columns={'value': 'dia_do_trabalhador'}, inplace=True)

    # Intervalo de dias antes e depois é 0 para ambos, conforme especificado
    days_before = 0
    days_after = 0

    # Lista de datas específicas para o Dia do Trabalhador conforme fornecido
    specific_dates_dia_do_trabalhador = [
        '2013-05-01', '2014-05-01', '2015-05-01', '2016-05-01', '2017-05-01',
        '2018-05-01', '2019-05-01', '2020-05-01', '2021-05-01', '2022-05-01',
        '2023-05-01', '2024-05-01', '2025-05-01'
    ]
    specific_dates_dia_do_trabalhador = pd.to_datetime(specific_dates_dia_do_trabalhador)

    # Função para definir os valores no intervalo de datas específicas
    def set_values(df, specific_dates, days_before, days_after):
        for specific_date in specific_dates:
            start_range = specific_date - pd.Timedelta(days=days_before)
            end_range = specific_date + pd.Timedelta(days=days_after)
            df.loc[(df['ds'] >= start_range) & (df['ds'] <= end_range), 'dia_do_trabalhador'] = 1

    # Aplicar a função ao DataFrame
    set_values(dia_do_trabalhador, specific_dates_dia_do_trabalhador, days_before, days_after)

    return dia_do_trabalhador