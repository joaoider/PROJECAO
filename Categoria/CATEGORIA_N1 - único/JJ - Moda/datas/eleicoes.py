# eleicoes_utils.py

import pandas as pd

def process_eleicoes(df):
    eleicoes = df.copy()
    eleicoes.rename(columns={'value': 'eleicoes'}, inplace=True)

    # Intervalo de dias antes e depois é 0 para ambos, conforme especificado
    days_before = 0
    days_after = 0

    # Lista de datas específicas para as Eleições conforme fornecido
    specific_dates_eleicoes = [
        '2018-10-07', '2018-10-28', '2022-10-02', '2022-10-30', '2024-10-06', '2024-10-27'
    ]
    specific_dates_eleicoes = pd.to_datetime(specific_dates_eleicoes)

    # Função para definir os valores no intervalo de datas específicas
    def set_values(df, specific_dates, days_before, days_after):
        for specific_date in specific_dates:
            start_range = specific_date - pd.Timedelta(days=days_before)
            end_range = specific_date + pd.Timedelta(days=days_after)
            df.loc[(df['ds'] >= start_range) & (df['ds'] <= end_range), 'eleicoes'] = 1

    # Aplicar a função ao DataFrame
    set_values(eleicoes, specific_dates_eleicoes, days_before, days_after)

    return eleicoes