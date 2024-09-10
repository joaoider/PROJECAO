freq = 'D' #frequencia dos dados Diário
horizon = 365 #dias futuros para previsao

marca = 'LL' #JJ

if marca == 'DD':
    path = 'export_dd.csv'
    data_inicio_base = '2018-01-01'
    path_liqui = 'liquidacao_dd.csv'

if marca == 'JJ':
    path = 'export_jj.csv'
    data_inicio_base = '2013-01-01'
    path_liqui = 'liquidacao_jj.csv'

if marca == 'LL':
    path = 'export_ll.csv'
    data_inicio_base = '2013-01-01'
    path_liqui = 'liquidacao_ll.csv'