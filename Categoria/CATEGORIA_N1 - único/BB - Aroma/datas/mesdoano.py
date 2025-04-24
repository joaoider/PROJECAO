def process_mes_do_ano(df):
    mesdoano = df.copy()
    mesdoano['value'] = mesdoano['ds'].dt.month_name()
    mesdoano.rename(columns={'value': 'mes_do_ano'}, inplace=True)

    # Mapeamento dos meses para números
    month_mapping = {
        'January': 1,
        'February': 2,
        'March': 3,
        'April': 4,
        'May': 5,
        'June': 6,
        'July': 7,
        'August': 8,
        'September': 9,
        'October': 10,
        'November': 11,
        'December': 12
    }

    # Criar a nova coluna 'monthofyear' utilizando o mapeamento
    mesdoano['monthofyear'] = mesdoano['mes_do_ano'].map(month_mapping)

    # Remover a coluna 'mes_do_ano'
    mesdoano = mesdoano.drop(columns=['mes_do_ano'])

    return mesdoano