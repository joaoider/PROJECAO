print('unindo_datas.py iniciado')

import pandas as pd

from DD_configuracoes import variaveis_futuras, start_date, end_date

from datas.diadasmaes import process_dia_das_maes
from datas.diadospais import process_dia_dos_pais
from datas.diadosnamorados import process_dia_dos_namorados
from datas.halloween import process_halloween
from datas.blackfriday import process_black_friday
from datas.natal import process_natal
from datas.copadomundo import process_copa_do_mundo
from datas.eleicoes import process_eleicoes
from datas.diadotrabalhador import process_dia_do_trabalhador
from datas.diadefinados import process_dia_de_finados
from datas.confraternizacaouniversal import process_confraternizacao_universal
from datas.independenciadobrasil import process_independencia_do_brasil
from datas.nossasenhoraaparecida import process_nossa_senhora_aparecida
from datas.proclamacaodarepublica import process_proclamacao_da_republica
from datas.sextafeirasanta import process_sexta_feira_santa
from datas.pascoa import process_pascoa
from datas.carnaval import process_carnaval
from datas.diadasemana import process_dia_da_semana
from datas.mesdoano import process_mes_do_ano
from datas.covid import process_covid
from DD_liquidacao import process_liquidacao, liqui_datas


# Criar DataFrame com todos os dias no intervalo especificado
date_range = pd.date_range(start=start_date, end=end_date)
df = pd.DataFrame(date_range, columns=['ds'])
# Inicializar a coluna 'value' com 0
df['value'] = 0


# Chamar as funções para processar os dados de cada evento
diadasemana = process_dia_da_semana(df)
mesdoano = process_mes_do_ano(df)
diadasmaes = process_dia_das_maes(df)
diadospais = process_dia_dos_pais(df)
diadosnamorados = process_dia_dos_namorados(df)
halloween = process_halloween(df)
blackfriday = process_black_friday(df)
natal = process_natal(df)
copa_do_mundo = process_copa_do_mundo(df)
eleicoes = process_eleicoes(df)
dia_do_trabalhador = process_dia_do_trabalhador(df)
dia_de_finados = process_dia_de_finados(df)
confraternizacao_universal = process_confraternizacao_universal(df)
independencia_do_brasil = process_independencia_do_brasil(df)
nossa_senhora_aparecida = process_nossa_senhora_aparecida(df)
proclamacao_da_republica = process_proclamacao_da_republica(df)
sexta_feira_santa = process_sexta_feira_santa(df)
pascoa = process_pascoa(df)
carnaval = process_carnaval(df)
covid = process_covid(df)
liquidacao = process_liquidacao(df, liqui_datas)  # liqui_datas deve ser definido com as datas de liquidação

datas = pd.merge(diadasemana, mesdoano, left_on='ds', right_on='ds')
datas = pd.merge(datas, diadasmaes, left_on='ds', right_on='ds')
datas = pd.merge(datas, diadospais, left_on='ds', right_on='ds')
datas = pd.merge(datas, diadosnamorados, left_on='ds', right_on='ds')
datas = pd.merge(datas, halloween, left_on='ds', right_on='ds')
datas = pd.merge(datas, blackfriday, left_on='ds', right_on='ds')
datas = pd.merge(datas, natal, left_on='ds', right_on='ds')
datas = pd.merge(datas, copa_do_mundo, left_on='ds', right_on='ds')
datas = pd.merge(datas, eleicoes, left_on='ds', right_on='ds')
datas = pd.merge(datas, dia_do_trabalhador, left_on='ds', right_on='ds')
datas = pd.merge(datas, dia_de_finados, left_on='ds', right_on='ds')
datas = pd.merge(datas, confraternizacao_universal, left_on='ds', right_on='ds')
datas = pd.merge(datas, independencia_do_brasil, left_on='ds', right_on='ds')
datas = pd.merge(datas, nossa_senhora_aparecida, left_on='ds', right_on='ds')
datas = pd.merge(datas, proclamacao_da_republica, left_on='ds', right_on='ds')
datas = pd.merge(datas, sexta_feira_santa, left_on='ds', right_on='ds')
datas = pd.merge(datas, pascoa, left_on='ds', right_on='ds')
datas = pd.merge(datas, carnaval, left_on='ds', right_on='ds')
datas = pd.merge(datas, covid, left_on='ds', right_on='ds')
datas = pd.merge(datas, liquidacao, left_on='ds', right_on='ds')


#datas['MARCA_SIGLA'] = 'JJ'
datas['ds'] = pd.to_datetime(datas['ds'])
#datas['unique_id'] = 'JJ'
#datas['unique_id'] = datas['unique_id'].astype(object)
datas_dv = ['ds'] + variaveis_futuras
datas = datas[datas_dv]
#datas

#print(datas.head())

#print(datas.tail())

print('unindo_datas.py finalizado')