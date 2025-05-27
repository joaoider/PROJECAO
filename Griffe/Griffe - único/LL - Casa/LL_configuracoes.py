print('configuracoes.py iniciado')

marca = 'LL'
modelo = 'GRU'
griffe = 'Le Lis Casa'
output_dir = "outputs"

from datetime import datetime
from dateutil.relativedelta import relativedelta

def gerar_datas_dinamicas(mes_corrente_str):
    # Converter string para datetime
    mes_corrente = datetime.strptime(mes_corrente_str, '%Y-%m')
    
    # Definir o ponto base (para 2024-12 → offset = 0)
    base_mes = datetime.strptime('2024-12', '%Y-%m')
    offset = (mes_corrente.year - base_mes.year) * 12 + (mes_corrente.month - base_mes.month)
    
    # Gerar datas com o deslocamento de meses
    data_inicio_base = datetime(2013, 1, 1)
    data_final_base = datetime(2024, 12, 31) + relativedelta(months=offset)

    data_train = datetime(2023, 12, 31) + relativedelta(months=offset)
    data_test = datetime(2024, 1, 1) + relativedelta(months=offset)

    data_inicio_futr_test = datetime(2024, 1, 1) + relativedelta(months=offset)
    data_final_futr_test = datetime(2024, 12, 31) + relativedelta(months=offset)

    data_inicio_futr = datetime(2025, 1, 1) + relativedelta(months=offset)
    data_final_futr = datetime(2025, 12, 31) + relativedelta(months=offset)

    start_date = data_inicio_base
    end_date = data_final_futr

    # Retornar como dicionário de strings
    return {
        "data_inicio_base": data_inicio_base.strftime('%Y-%m-%d'),
        "data_final_base": data_final_base.strftime('%Y-%m-%d'),
        "data_train": data_train.strftime('%Y-%m-%d'),
        "data_test": data_test.strftime('%Y-%m-%d'),
        "data_inicio_futr_test": data_inicio_futr_test.strftime('%Y-%m-%d'),
        "data_final_futr_test": data_final_futr_test.strftime('%Y-%m-%d'),
        "data_inicio_futr": data_inicio_futr.strftime('%Y-%m-%d'),
        "data_final_futr": data_final_futr.strftime('%Y-%m-%d'),
        "start_date": start_date.strftime('%Y-%m-%d'),
        "end_date": end_date.strftime('%Y-%m-%d'),
    }

freq = 'D' # frequencia dos dados Diário
horizon = 365 # dias futuros para previsao
variaveis_futuras = ['dayofweek', 'monthofyear', 'dia_das_maes', 'dia_dos_pais', 'dia_dos_namorados', 'halloween', 'black_friday', 'natal', 'copa_do_mundo', 'eleicoes', 'dia_do_trabalhador', 'dia_de_finados', 'confraternizacao_universal', 'independencia_do_brasil', 'nossa_senhora_aparecida', 'proclamacao_da_republica', 'sexta_feira_santa', 'pascoa', 'carnaval', 'covid', 'liquidacao']
variaveis_historicas = ['QLF', 'ROL', 'CPV']

# Exemplo de uso:
mes_corrente = '2024-12'
datas = gerar_datas_dinamicas(mes_corrente)
# Desempacotar o dicionário em variáveis
data_inicio_base = datas['data_inicio_base']
data_final_base = datas['data_final_base']
data_train = datas['data_train']
data_test = datas['data_test']
data_inicio_futr_test = datas['data_inicio_futr_test']
data_final_futr_test = datas['data_final_futr_test']
data_inicio_futr = datas['data_inicio_futr']
data_final_futr = datas['data_final_futr']
start_date = datas['start_date']
end_date = datas['end_date']

for k, v in datas.items():
    print(f"{k} = '{v}'")

print('configuracoes.py finalizado')