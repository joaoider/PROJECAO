# copadomundo_utils.py

import pandas as pd

def process_copa_do_mundo(df):
    copa_do_mundo = df.copy()
    copa_do_mundo.rename(columns={'value': 'copa_do_mundo'}, inplace=True)

    # Intervalo de dias antes e depois é 0 para ambos, conforme especificado
    days_before = 0
    days_after = 0

    # Lista de datas específicas para a Copa do Mundo conforme fornecido
    specific_dates_copa_do_mundo = [
        '2014-06-12', '2014-06-17', '2014-06-23', '2014-06-28', '2014-07-04', 
        '2014-07-08', '2014-07-12', '2018-06-14', '2018-06-17', '2018-06-22', 
        '2018-07-02', '2018-07-06', '2022-11-20', '2022-11-24', '2022-11-28', 
        '2022-12-02', '2022-12-05', '2022-12-09', '2026-07-11'
    ]
    specific_dates_copa_do_mundo = pd.to_datetime(specific_dates_copa_do_mundo)

    # Função para definir os valores no intervalo de datas específicas
    def set_values(df, specific_dates, days_before, days_after):
        for specific_date in specific_dates:
            start_range = specific_date - pd.Timedelta(days=days_before)
            end_range = specific_date + pd.Timedelta(days=days_after)
            df.loc[(df['ds'] >= start_range) & (df['ds'] <= end_range), 'copa_do_mundo'] = 1

    # Aplicar a função ao DataFrame
    set_values(copa_do_mundo, specific_dates_copa_do_mundo, days_before, days_after)

    return copa_do_mundo