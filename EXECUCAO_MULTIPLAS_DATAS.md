# Execução para Múltiplas Datas de Referência

## Resumo da Nova Funcionalidade

O programa agora executa automaticamente para múltiplas datas de referência, desde **2024-01-01** até a **data atual**, onde cada execução usa dados até o último dia do mês anterior como referência.

## Como Funciona

### 1. **Geração de Datas de Referência**

O programa gera automaticamente uma lista de datas de referência:

- **Início**: 2024-01-01
- **Fim**: Data atual
- **Intervalo**: Mensal
- **Referência**: Último dia do mês anterior

### 2. **Exemplo de Datas de Referência**

Se executado em **Agosto de 2025**, as datas seriam:

| Mês de Referência | Data de Referência | Descrição |
|-------------------|-------------------|-----------|
| Janeiro 2024 | 2023-12-31 | Último dia de dezembro/2023 |
| Fevereiro 2024 | 2024-01-31 | Último dia de janeiro/2024 |
| Março 2024 | 2024-02-29 | Último dia de fevereiro/2024 |
| ... | ... | ... |
| Agosto 2025 | 2025-07-31 | Último dia de julho/2025 |

### 3. **Lógica de Execução**

Para cada data de referência:

1. **Período de Treinamento**: Dados históricos até 1 ano antes da data de referência
2. **Período de Teste**: Último ano até a data de referência
3. **Período de Previsões**: Data de referência até 1 ano à frente

### 4. **Exemplo Prático**

Para data de referência **2024-06-30**:

| Período | Início | Fim | Descrição |
|---------|--------|-----|-----------|
| **Treinamento** | 2020-01-01 | 2023-06-30 | Dados históricos |
| **Teste** | 2023-07-01 | 2024-06-30 | Último ano |
| **Previsões** | 2024-07-01 | 2025-06-30 | Próximo ano |

## Estrutura de Arquivos Gerados

```
data/forecasts/{MARCA}/{TIPO}/
├── 202312/                    # Execução para dezembro/2023
│   ├── previsoes_finais_LSTM.csv
│   └── previsoes_finais_LSTM.parquet
├── 202401/                    # Execução para janeiro/2024
│   ├── previsoes_finais_LSTM.csv
│   └── previsoes_finais_LSTM.parquet
├── 202402/                    # Execução para fevereiro/2024
│   ├── previsoes_finais_LSTM.csv
│   └── previsoes_finais_LSTM.parquet
└── ...                        # E assim por diante
```

## Vantagens da Abordagem

### 1. **Análise Histórica Completa**
- Permite analisar como o modelo teria performado em diferentes momentos
- Facilita a identificação de padrões sazonais
- Ajuda a validar a robustez do modelo

### 2. **Backtesting Automatizado**
- Testa o modelo em diferentes condições de mercado
- Valida a consistência das previsões ao longo do tempo
- Identifica períodos de melhor/pior performance

### 3. **Comparação Temporal**
- Permite comparar previsões feitas em diferentes momentos
- Facilita a análise de tendências e mudanças
- Ajuda na calibração de parâmetros

## Configurações

### **Datas de Referência**
```python
def generate_reference_dates():
    start_date = datetime(2024, 1, 1)  # Data inicial
    end_date = datetime.now()           # Data atual
```

### **Períodos Dinâmicos**
```python
# Para cada data de referência
DATA_ATUAL = reference_date
DATA_TRAIN = (reference_date - timedelta(days=365)).strftime('%Y-%m-%d')
DATA_TEST = (reference_date - timedelta(days=365)).strftime('%Y-%m-%d')
DATA_INICIO_FUTR = reference_date.strftime('%Y-%m-%d')
DATA_FINAL_FUTR = (reference_date + timedelta(days=365)).strftime('%Y-%m-%d')
```

## Logs Informativos

O programa agora exibe logs detalhados:

```
Executando para 20 datas de referência:
  1. 2023-12-31 (último dia do mês anterior)
  2. 2024-01-31 (último dia do mês anterior)
  3. 2024-02-29 (último dia do mês anterior)
  ...

Iniciando processamento para marca BB, tipo GERAL e data de referência 2024-06-30
Configurações atualizadas para data de referência 2024-06-30
Período de treinamento: até 2023-06-30
Período de teste: 2023-07-01 até 2024-06-30
Período de previsões: 2024-07-01 até 2025-06-30
```

## Compatibilidade

- ✅ **Mantém funcionalidade original** para execução única
- ✅ **Adiciona nova funcionalidade** para múltiplas datas
- ✅ **Logs detalhados** para acompanhamento
- ✅ **Organização automática** de arquivos por data
- ✅ **Configurações dinâmicas** para cada execução 