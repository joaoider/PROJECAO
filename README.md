# 🚀 Projeto de Previsão de Vendas - Sistema Neural

Este projeto implementa um **sistema avançado de previsão de vendas** utilizando modelos de deep learning com avaliação completa e seleção automática do melhor modelo.

## 🕐 **Períodos Dinâmicos**

O sistema agora utiliza **períodos dinâmicos** baseados na data atual:

- **📚 Treinamento**: Dados históricos até 1 ano atrás da data atual
- **🧪 Teste**: Último ano de dados (para calcular MAPE, RMSE, etc.)
- **🔮 Previsões**: Próximo ano (salvo no Parquet final)

**Resultado**: Arquivo Parquet com 2 anos de dados (1 ano de teste + 1 ano de previsões)

## 🎯 **Funcionalidades Principais**

- ✅ **Grid Search Completo**: Testa todas as combinações de parâmetros
- ✅ **Múltiplos Modelos**: LSTM, GRU, NHITS, NBEATSx
- ✅ **Múltiplas Métricas**: MAPE, RMSE, MAE, MSE
- ✅ **Score Composto**: Seleção inteligente baseada em todas as métricas
- ✅ **Eventos Especiais**: 15+ eventos brasileiros (Black Friday, Carnaval, etc.)
- ✅ **Features Temporais**: Dia da semana, mês do ano
- ✅ **Relatórios Detalhados**: Ranking completo e comparações

## 📁 **Estrutura do Projeto**

```
projecao/
├── src/                    # 🧠 Código fonte principal
│   ├── main.py            # 🚀 Ponto de entrada principal
│   ├── models/            # 🤖 Implementações dos modelos
│   │   ├── base_model.py
│   │   ├── model_LSTM.py
│   │   ├── model_GRU.py
│   │   ├── model_NHITS.py
│   │   └── model_NBEATSx.py
│   ├── utils/             # 🔧 Utilitários e funções auxiliares
│   │   ├── data_processing.py
│   │   ├── metrics.py
│   │   ├── queries.py
│   │   ├── special_dates.py
│   │   └── save_config_vars.py
│   └── config/            # ⚙️ Configurações do projeto
│       └── settings.py
├── data/                  # 📊 Dados do projeto
│   ├── raw/              # 📥 Dados brutos
│   ├── processed/        # 🔄 Dados processados
│   └── forecasts/        # 📤 Previsões geradas
├── GUIA_CONFIGURACAO.md  # 📖 Guia detalhado de configuração
├── requirements.txt      # 📦 Dependências do projeto
└── README.md            # 📋 Este arquivo
```

## 🛠️ **Requisitos**

- Python 3.8+
- Dependências listadas em `requirements.txt`

## 📦 **Instalação**

1. **Clone o repositório:**
```bash
git clone [URL_DO_REPOSITORIO]
cd projecao
```

2. **Crie um ambiente virtual:**
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

3. **Instale as dependências:**
```bash
pip install -r requirements.txt
```

## ⚙️ **Configuração**

### **1. Configuração Rápida**
Edite `src/config/settings.py` para configurar:

```python
# 🔧 MARCAS: Selecione quais marcas processar
MARCAS = ['BB']  # ['BB', 'LL', 'DD', 'JJ']

# 🔧 TIPOS_PREVISAO: Selecione tipos de previsão
TIPOS_PREVISAO = ['GERAL']  # ['GERAL', 'GRIFFE', 'GRIFFE_N1']

# 🔧 MODELOS_A_EXECUTAR: Selecione quais modelos treinar
MODELOS_A_EXECUTAR = ['LSTM']  # ['LSTM', 'GRU', 'NHITS', 'NBEATSx']

# 🔧 METRICS: Selecione quais métricas calcular
METRICS = ['MAPE', 'RMSE', 'MAE', 'MSE']

# 🔧 VARIAVEIS_FUTURAS: Selecione variáveis futuras
VARIAVEIS_FUTURAS = ['black_friday', 'dayofweek']

# 🔧 VARIAVEIS_HISTORICAS: Selecione variáveis históricas
VARIAVEIS_HISTORICAS = ['QLF']
```

### **2. Configuração Detalhada**
Consulte o `GUIA_CONFIGURACAO.md` para configurações avançadas.

## 🚀 **Uso**

### **Execução Completa**
```bash
python src/main.py
```

### **O que acontece:**
1. 📥 **Carrega dados** do Databricks
2. 🔄 **Processa dados** com features temporais e eventos
3. 🤖 **Treina todos os modelos** com grid search
4. 📊 **Avalia com todas as métricas** configuradas
5. 🏆 **Seleciona o melhor modelo** baseado em score composto
6. 📤 **Gera previsões** com o modelo vencedor
7. 📋 **Salva relatórios** detalhados

## 🤖 **Modelos Implementados**

| Modelo | Descrição | Configurável |
|--------|-----------|--------------|
| **LSTM** | Long Short-Term Memory | ✅ |
| **GRU** | Gated Recurrent Unit | ✅ |
| **NHITS** | Neural Hierarchical Interpolation | ✅ |
| **NBEATSx** | Neural Basis Expansion | ✅ |

## 📊 **Métricas de Avaliação**

| Métrica | Descrição | Peso |
|---------|-----------|------|
| **MAPE** | Mean Absolute Percentage Error | 40% |
| **RMSE** | Root Mean Square Error | 30% |
| **MAE** | Mean Absolute Error | 20% |
| **MSE** | Mean Square Error | 10% |

## 📅 **Eventos Especiais Suportados**

- 🛍️ **Black Friday** (Novembro)
- 🎭 **Carnaval** (Fevereiro)
- 🎄 **Natal** (Dezembro)
- 🎃 **Halloween** (Outubro)
- 🏛️ **Eleições** (Outubro)
- 🇧🇷 **Independência do Brasil** (Setembro)
- ⛪ **Nossa Senhora Aparecida** (Outubro)
- ✝️ **Páscoa** (Data móvel)
- 🏛️ **Proclamação da República** (Novembro)
- ✝️ **Sexta-Feira Santa** (Data móvel)
- 🎊 **Confraternização Universal** (Janeiro)
- ⚽ **Copa do Mundo** (Julho)
- 🦠 **COVID** (2020-2022)
- 👩 **Dia das Mães** (Maio)
- ⚰️ **Dia de Finados** (Novembro)
- 💕 **Dia dos Namorados** (Junho)
- 👨 **Dia dos Pais** (Agosto)
- 👷 **Dia do Trabalhador** (Maio)

## 📁 **Saídas Geradas**

```
data/forecasts/{MARCA}/{TIPO}/
├── relatorio_comparacao_modelos.csv     # 📊 Ranking completo
├── melhor_modelo_parametros_{MODEL}.csv # ⚙️ Parâmetros do vencedor
├── previsoes_finais_{MODEL}.csv        # 📈 Previsões CSV
└── previsoes_finais_{MODEL}.parquet    # 📦 Previsões Parquet
```

## 🔧 **Configurações Avançadas**

### **Grid Search de Hiperparâmetros**
```python
MODEL_PARAM_GRID = {
    'LSTM': {
        'learning_rate': [0.001, 0.01],
        'batch_size': [32, 64],
        'encoder_hidden_size': [100, 200]
    }
}
```

### **Datas Dinâmicas (Baseadas na Data Atual)**
```python
# Período de treinamento: até 1 ano atrás da data atual
DATA_TRAIN = (DATA_ATUAL - timedelta(days=365)).strftime('%Y-%m-%d')

# Período de teste: último ano (desde 1 ano atrás até hoje)
DATA_TEST = (DATA_ATUAL - timedelta(days=365)).strftime('%Y-%m-%d')

# Período de previsões futuras: próximo ano (desde hoje até 1 ano à frente)
DATA_INICIO_FUTR = DATA_ATUAL.strftime('%Y-%m-%d')
DATA_FINAL_FUTR = (DATA_ATUAL + timedelta(days=365)).strftime('%Y-%m-%d')
```

**Exemplo**: Se executado em 15/01/2025:
- **Treinamento**: 2020-01-01 até 2024-01-15
- **Teste**: 2024-01-15 até 2025-01-15  
- **Previsões**: 2025-01-15 até 2026-01-15

## 📈 **Exemplo de Resultado**

```
🎯 MELHOR MODELO SELECIONADO:
   Modelo: GRU_001
   Score Composto: 0.1251
   Métricas: {'MAPE': 4.8, 'RMSE': 9.8, 'MAE': 7.9, 'MSE': 96.04}

🏆 TOP 3 MODELOS:
   1. GRU_001: Score=0.1251
   2. LSTM_001: Score=0.1158
   3. NHITS_001: Score=0.0939
```

## 🤝 **Contribuição**

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/nova-feature`)
3. Commit suas mudanças (`git commit -m 'Adiciona nova feature'`)
4. Push para a branch (`git push origin feature/nova-feature`)
5. Abra um Pull Request

## 📖 **Documentação Adicional**

- 📋 **GUIA_CONFIGURACAO.md**: Configurações detalhadas
- 📊 **Relatórios**: Gerados automaticamente em `data/forecasts/`

## 📄 **Licença**

Este projeto está licenciado sob a licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes. 