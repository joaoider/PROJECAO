import pandas as pd

def process_covid(df):
    covid = df.copy()
    covid.rename(columns={'value': 'covid'}, inplace=True)

    # Definir o range de dias antes e depois
    days_before = 60
    days_after = 240

    # Lista de datas específicas para o COVID conforme fornecido
    specific_dates_covid = [
        '2020-03-01'
    ]
    specific_dates_covid = pd.to_datetime(specific_dates_covid)

    # Função para definir os valores no intervalo de datas específicas
    def set_values(df, specific_dates, days_before, days_after):
        for specific_date in specific_dates:
            start_range = specific_date - pd.Timedelta(days=days_before)
            end_range = specific_date + pd.Timedelta(days=days_after)
            df.loc[(df['ds'] >= start_range) & (df['ds'] <= end_range), 'covid'] = 1

    # Aplicar a função ao DataFrame
    set_values(covid, specific_dates_covid, days_before, days_after)

    return covid