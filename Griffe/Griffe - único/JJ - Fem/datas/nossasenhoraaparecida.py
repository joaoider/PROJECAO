import pandas as pd

def process_nossa_senhora_aparecida(df):
    nossa_senhora_aparecida = df.copy()
    nossa_senhora_aparecida.rename(columns={'value': 'nossa_senhora_aparecida'}, inplace=True)

    # Intervalo de dias antes e depois é 0 para ambos, conforme especificado
    days_before = 0
    days_after = 0

    # Lista de datas específicas para Nossa Senhora Aparecida conforme fornecido
    specific_dates_nossa_senhora_aparecida = [
        '2013-10-12', '2014-10-12', '2015-10-12', '2016-10-12', '2017-10-12',
        '2018-10-12', '2019-10-12', '2020-10-12', '2021-10-12', '2022-10-12',
        '2023-10-12', '2024-10-12', '2025-10-12', '2026-10-12'
    ]
    specific_dates_nossa_senhora_aparecida = pd.to_datetime(specific_dates_nossa_senhora_aparecida)

    # Função para definir os valores no intervalo de datas específicas
    def set_values(df, specific_dates, days_before, days_after):
        for specific_date in specific_dates:
            start_range = specific_date - pd.Timedelta(days=days_before)
            end_range = specific_date + pd.Timedelta(days=days_after)
            df.loc[(df['ds'] >= start_range) & (df['ds'] <= end_range), 'nossa_senhora_aparecida'] = 1

    # Aplicar a função ao DataFrame
    set_values(nossa_senhora_aparecida, specific_dates_nossa_senhora_aparecida, days_before, days_after)

    return nossa_senhora_aparecida