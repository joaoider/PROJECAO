import time
# Marcação de início de execução
start_time = time.time()

# MÓDULO PRINCIPAL
print('main_GRU.py iniciado')

# Importar módulos e dataframes necessários
from configuracoes.imports import *
from configuracoes.configuracoes_GRU import marca
from base import data_neural, futr_df 

print('Marca: ', marca)
print('###############################')

# Criar a pasta com a data do dia, se não existir
data_atual = datetime.now().strftime('%Y-%m-%d')
horario_atual = datetime.now().strftime('%H-%M-%S')
output_dir = f'outputs/{data_atual}'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Carregar o módulo do modelo GRU dinamicamente
modulo_modelo = importlib.import_module('models.model_GRU_final')

# Ajustar para chamar a função correta, no caso do GRU
funcao_treinar = getattr(modulo_modelo, 'treinar_GRU')  # Função específica para o GRU

# Parâmetros selecionados para a previsão
max_steps = 1
learning_rate = 0.001
batch_size = 32
encoder_hidden_size = 200
decoder_hidden_size = 200
encoder_n_layers = 2
decoder_layers = 2
context_size = 10
encoder_activation = 'tanh'
encoder_bias = True
encoder_dropout = 0.0
num_lr_decays = 3
early_stop_patience_steps = -1
val_check_steps = 100
scaler_type = 'robust'
random_seed = 1
num_workers_loader = 0
drop_last_loader = False
optimizer = None
lr_scheduler = None

# Nome para a coluna de previsão
col_name = (f'GRU_steps{max_steps}_lr{learning_rate}_batch{batch_size}_'
            f'encoder{encoder_hidden_size}_decoder{decoder_hidden_size}_'
            f'enc_layers{encoder_n_layers}_dec_layers{decoder_layers}_context{context_size}_'
            f'activation{encoder_activation}_bias{encoder_bias}_dropout{encoder_dropout}_'
            f'lr_decays{num_lr_decays}_early_stop{early_stop_patience_steps}_'
            f'val_check{val_check_steps}_scaler{scaler_type}_seed{random_seed}')

print(f'Parâmetros selecionados: max_steps={max_steps}, learning_rate={learning_rate}, '
      f'batch_size={batch_size}, encoder_hidden_size={encoder_hidden_size}, '
      f'decoder_hidden_size={decoder_hidden_size}, encoder_n_layers={encoder_n_layers}, '
      f'decoder_layers={decoder_layers}, context_size={context_size}, encoder_activation={encoder_activation}, '
      f'encoder_bias={encoder_bias}, encoder_dropout={encoder_dropout}, num_lr_decays={num_lr_decays}, '
      f'early_stop_patience_steps={early_stop_patience_steps}, val_check_steps={val_check_steps}, '
      f'scaler_type={scaler_type}, random_seed={random_seed}, num_workers_loader={num_workers_loader}, '
      f'drop_last_loader={drop_last_loader}, optimizer={optimizer}, lr_scheduler={lr_scheduler}')

# Treinar o modelo com os parâmetros selecionados
data_neural_hat = funcao_treinar(max_steps, learning_rate, batch_size, 
                                 encoder_hidden_size, decoder_hidden_size, 
                                 encoder_n_layers, decoder_layers, context_size, 
                                 encoder_activation, encoder_bias, encoder_dropout, 
                                 num_lr_decays, early_stop_patience_steps, 
                                 val_check_steps, scaler_type, random_seed, 
                                 num_workers_loader, drop_last_loader, 
                                 optimizer, lr_scheduler)

# Verificar se a previsão foi gerada corretamente
if data_neural_hat is not None:
    print("Previsão gerada com sucesso.")
    
    # Renomeia a coluna de previsões com o nome do modelo e parâmetros testados
    if 'GRU' in data_neural_hat.columns:
        data_neural_hat.rename(columns={'GRU': col_name}, inplace=True)
    else:
        print(f"Erro: A coluna 'GRU' não foi encontrada nas previsões.")

    # Salvar o resultado final em CSV
    csv_file_path = f'{output_dir}/forecast_GRU_final_{horario_atual}.csv'
    data_neural_hat.to_csv(csv_file_path, index=False)
    print(f"Previsão salva com sucesso: {csv_file_path}")

    # Plotar as previsões
    data_neural_hat.set_index('ds')[col_name].plot(linewidth=2)

    # Configurações de rótulos e título do gráfico
    plt.ylabel('VLF', fontsize=12)
    plt.xlabel('Date', fontsize=12)
    plt.title(f'Previsões GRU ({col_name})', fontsize=14)
    plt.grid()

    # Salvar o gráfico como imagem
    plot_file_path = f'{output_dir}/plot_image_GRU_final_{horario_atual}.png'
    plt.savefig(plot_file_path)
    print(f"Gráfico salvo com sucesso: {plot_file_path}")
else:
    print("Erro: Não foi possível gerar a previsão.")

# Exibir o tempo total de execução
end_time = time.time()
execution_time = end_time - start_time
print(f"Tempo de execução total: {execution_time:.2f} segundos")

print('main_GRU_final.py finalizado')