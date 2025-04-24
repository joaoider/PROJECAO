import pandas as pd

def process_sexta_feira_santa(df):
    sexta_feira_santa = df.copy()
    sexta_feira_santa.rename(columns={'value': 'sexta_feira_santa'}, inplace=True)

    # Intervalo de dias antes e depois é 0 para ambos, conforme especificado
    days_before = 0
    days_after = 0

    # Lista de datas específicas para a Sexta-Feira Santa conforme fornecido
    specific_dates_sexta_feira_santa = [
        '2013-03-29', '2014-04-18', '2015-04-03', '2016-03-25', '2017-04-14',
        '2018-03-30', '2019-04-19', '2020-04-10', '2021-04-02', '2022-04-15',
        '2023-04-07', '2024-03-29', '2025-04-18'
    ]
    specific_dates_sexta_feira_santa = pd.to_datetime(specific_dates_sexta_feira_santa)

    # Função para definir os valores no intervalo de datas específicas
    def set_values(df, specific_dates, days_before, days_after):
        for specific_date in specific_dates:
            start_range = specific_date - pd.Timedelta(days=days_before)
            end_range = specific_date + pd.Timedelta(days=days_after)
            df.loc[(df['ds'] >= start_range) & (df['ds'] <= end_range), 'sexta_feira_santa'] = 1

    # Aplicar a função ao DataFrame
    set_values(sexta_feira_santa, specific_dates_sexta_feira_santa, days_before, days_after)

    return sexta_feira_santa