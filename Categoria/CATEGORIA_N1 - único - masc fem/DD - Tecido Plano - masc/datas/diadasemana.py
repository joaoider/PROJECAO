def process_dia_da_semana(df):
    diadasemana = df.copy()
    diadasemana['value'] = diadasemana['ds'].dt.day_name()
    diadasemana.rename(columns={'value': 'dia_da_semana'}, inplace=True)

    # Mapeamento dos dias da semana para números
    day_mapping = {
        'Monday': 0,
        'Tuesday': 1,
        'Wednesday': 2,
        'Thursday': 3,
        'Friday': 4,
        'Saturday': 5,
        'Sunday': 6
    }

    # Criar a nova coluna 'dayofweek' utilizando um loop for
    diadasemana['dayofweek'] = diadasemana['dia_da_semana'].map(day_mapping)

    # Remover a coluna 'dia_da_semana'
    diadasemana = diadasemana.drop(columns=['dia_da_semana'])

    return diadasemana