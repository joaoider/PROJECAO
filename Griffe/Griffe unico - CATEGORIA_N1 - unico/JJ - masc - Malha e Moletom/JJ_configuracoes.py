print('configuracoes.py iniciado')

freq = 'D' # frequencia dos dados Diário
horizon = 365 # dias futuros para previsao
variaveis_futuras = ['dayofweek', 'monthofyear', 'dia_das_maes', 'dia_dos_pais', 'dia_dos_namorados', 'halloween', 'black_friday', 'natal', 'copa_do_mundo', 'eleicoes', 'dia_do_trabalhador', 'dia_de_finados', 'confraternizacao_universal', 'independencia_do_brasil', 'nossa_senhora_aparecida', 'proclamacao_da_republica', 'sexta_feira_santa', 'pascoa', 'carnaval', 'covid', 'liquidacao']
variaveis_historicas = ['QLF', 'ROL', 'CPV']
# marcas

marca = 'JJ'

data_inicio_base = '2013-01-01'
data_final_base = '2024-12-31'

data_train = '2023-12-31'
data_test = '2024-01-01'

data_inicio_futr_test = '2024-01-01'
data_final_futr_test = '2024-12-31'

data_inicio_futr = '2025-01-01'
data_final_futr = '2025-12-31'

start_date = '2013-01-01'
end_date = '2025-12-31'




print('configuracoes.py finalizado')