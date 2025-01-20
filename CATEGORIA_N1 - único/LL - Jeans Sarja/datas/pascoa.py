import pandas as pd

def process_pascoa(df):
    pascoa = df.copy()
    pascoa.rename(columns={'value': 'pascoa'}, inplace=True)

    # Intervalo de dias antes e depois é 0 para ambos, conforme especificado
    days_before = 0
    days_after = 0

    # Lista de datas específicas para a Páscoa conforme fornecido
    specific_dates_pascoa = [
        '2013-03-31', '2014-04-20', '2015-04-05', '2016-03-27', '2017-04-16',
        '2018-04-01', '2019-04-21', '2020-04-12', '2021-04-04', '2022-04-17',
        '2023-04-09', '2024-03-31', '2025-04-20'
    ]
    specific_dates_pascoa = pd.to_datetime(specific_dates_pascoa)

    # Função para definir os valores no intervalo de datas específicas
    def set_values(df, specific_dates, days_before, days_after):
        for specific_date in specific_dates:
            start_range = specific_date - pd.Timedelta(days=days_before)
            end_range = specific_date + pd.Timedelta(days=days_after)
            df.loc[(df['ds'] >= start_range) & (df['ds'] <= end_range), 'pascoa'] = 1

    # Aplicar a função ao DataFrame
    set_values(pascoa, specific_dates_pascoa, days_before, days_after)

    return pascoa