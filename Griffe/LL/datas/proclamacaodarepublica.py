import pandas as pd

def process_proclamacao_da_republica(df):
    proclamacao_da_republica = df.copy()
    proclamacao_da_republica.rename(columns={'value': 'proclamacao_da_republica'}, inplace=True)

    # Intervalo de dias antes e depois é 0 para ambos, conforme especificado
    days_before = 0
    days_after = 0

    # Lista de datas específicas para a Proclamação da República conforme fornecido
    specific_dates_proclamacao_da_republica = [
        '2013-11-15', '2014-11-15', '2015-11-15', '2016-11-15', '2017-11-15',
        '2018-11-15', '2019-11-15', '2020-11-15', '2021-11-15', '2022-11-15',
        '2023-11-15', '2024-11-15', '2025-11-15'
    ]
    specific_dates_proclamacao_da_republica = pd.to_datetime(specific_dates_proclamacao_da_republica)

    # Função para definir os valores no intervalo de datas específicas
    def set_values(df, specific_dates, days_before, days_after):
        for specific_date in specific_dates:
            start_range = specific_date - pd.Timedelta(days=days_before)
            end_range = specific_date + pd.Timedelta(days=days_after)
            df.loc[(df['ds'] >= start_range) & (df['ds'] <= end_range), 'proclamacao_da_republica'] = 1

    # Aplicar a função ao DataFrame
    set_values(proclamacao_da_republica, specific_dates_proclamacao_da_republica, days_before, days_after)

    return proclamacao_da_republica