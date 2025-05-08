import pandas as pd

def process_independencia_do_brasil(df):
    independencia_do_brasil = df.copy()
    independencia_do_brasil.rename(columns={'value': 'independencia_do_brasil'}, inplace=True)

    # Intervalo de dias antes e depois é 0 para ambos, conforme especificado
    days_before = 0
    days_after = 0

    # Lista de datas específicas para a Independência do Brasil conforme fornecido
    specific_dates_independencia_do_brasil = [
        '2013-09-07', '2014-09-07', '2015-09-07', '2016-09-07', '2017-09-07',
        '2018-09-07', '2019-09-07', '2020-09-07', '2021-09-07', '2022-09-07',
        '2023-09-07', '2024-09-07', '2025-09-07', '2026-09-07'
    ]
    specific_dates_independencia_do_brasil = pd.to_datetime(specific_dates_independencia_do_brasil)

    # Função para definir os valores no intervalo de datas específicas
    def set_values(df, specific_dates, days_before, days_after):
        for specific_date in specific_dates:
            start_range = specific_date - pd.Timedelta(days=days_before)
            end_range = specific_date + pd.Timedelta(days=days_after)
            df.loc[(df['ds'] >= start_range) & (df['ds'] <= end_range), 'independencia_do_brasil'] = 1

    # Aplicar a função ao DataFrame
    set_values(independencia_do_brasil, specific_dates_independencia_do_brasil, days_before, days_after)

    return independencia_do_brasil