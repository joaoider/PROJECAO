Programa para Previsão Temporal utilizando Neural Forecast

Variável prevista: VLF
Variáveis exógenas: 
    Futuras: futr_exog_list = ['dayofweek', 'monthofyear', 'dia_das_maes', 'dia_dos_pais', 'dia_dos_namorados', 'halloween', 'black_friday', 'natal', 'copa_do_mundo', 'eleicoes', 'dia_do_trabalhador', 'dia_de_finados', 'confraternizacao_universal', 'independencia_do_brasil', 'nossa_senhora_aparecida', 'proclamacao_da_republica', 'sexta_feira_santa', 'pascoa', 'carnaval']
    Históricas: hist_exog_list = ['QLF']
    Estática: static_exog_list = ['unique_id] #marca


Dados históricos
export_dd.csv = base histórica DD 
export_jj.csv = base histórica JJ 
export_ll.csv = base histórica LL

liquidacao_dd.csv = dados de liquidacao DD 
liquidacao_jj.csv = dados de liquidacao JJ 
liquidacao_ll.csv = dados de liquidacao LL

Módulos: 
imports.py = Carregando todas bibliotecas necessárias
configuracoes.py = parametros basicos para rodar modelos
from datas = feriados/eventos adicionados
unindo_datas.py = organizando dataframe com todos feriados/eventos 
base.py = carregando base histórica de dados unindo com unindo_datas e criando base para previsão futura
model.py = modelos utilizados e parâmetros de cada um
main.py = ajuste dos resultados dos modelos, plot de gráficos e salvando arquivos

Imagens
plot_image.png = gráfico com dados históricos e futuros de cada modelo

Dados futuros
plot_df.csv = Arquivo com todos os dados gerados pelo modelo
forecast.csv = Arquivo com dados do modelo agrupados por mês 

Modelos: F/H/S
    LSTM - RNN
    GRU - RNN
    NHITS - MLP
    BiTCN - CNN
    NBEATSx - MLP