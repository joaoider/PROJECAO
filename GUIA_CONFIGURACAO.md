# 📋 Guia de Configuração - settings.py

## 🎯 Como Configurar o Projeto

O arquivo `src/config/settings.py` permite que você selecione exatamente o que deseja executar. Aqui está como configurar cada seção:

## 🔧 1. MARCAS

**O que é:** Selecione quais marcas processar.

**Opções disponíveis:** `['BB', 'LL', 'DD', 'JJ']` (substitua pelos nomes reais das suas marcas)

**Exemplos:**
```python
# Processar apenas a marca BB
MARCAS = ['BB']

# Processar múltiplas marcas
MARCAS = ['BB', 'LL', 'DD']

# Processar todas as marcas
MARCAS = ['BB', 'LL', 'DD', 'JJ']
```

## 🔧 2. TIPOS_PREVISAO

**O que é:** Selecione tipos de previsão.

**Opções disponíveis:** `['GERAL', 'GRIFFE', 'GRIFFE_N1']`

**Exemplos:**
```python
# Processar apenas previsão geral
TIPOS_PREVISAO = ['GERAL']

# Processar múltiplos tipos
TIPOS_PREVISAO = ['GERAL', 'GRIFFE']

# Processar todos os tipos
TIPOS_PREVISAO = ['GERAL', 'GRIFFE', 'GRIFFE_N1']
```

## 🔧 3. MODELOS_A_EXECUTAR

**O que é:** Selecione quais modelos de machine learning treinar.

**Opções disponíveis:** `['LSTM', 'GRU', 'NHITS', 'NBEATSx']`

**Exemplos:**
```python
# Treinar apenas LSTM
MODELOS_A_EXECUTAR = ['LSTM']

# Treinar LSTM e GRU
MODELOS_A_EXECUTAR = ['LSTM', 'GRU']

# Treinar todos os modelos
MODELOS_A_EXECUTAR = ['LSTM', 'GRU', 'NHITS', 'NBEATSx']
```

## 🔧 4. METRICS

**O que é:** Selecione quais métricas calcular para avaliar os modelos.

**Opções disponíveis:** `['MAPE', 'RMSE', 'MAE']`

**Exemplos:**
```python
# Calcular apenas MAPE
METRICS = ['MAPE']

# Calcular MAPE e RMSE
METRICS = ['MAPE', 'RMSE']

# Calcular todas as métricas
METRICS = ['MAPE', 'RMSE', 'MAE']
```

## 🔧 5. VARIAVEIS_FUTURAS

**O que é:** Selecione eventos especiais que afetam as vendas futuras.

**Opções disponíveis:**
- `'black_friday'` - Black Friday
- `'carnaval'` - Carnaval
- `'natal'` - Natal
- `'halloween'` - Halloween
- `'dia_do_trabalhador'` - Dia do Trabalhador
- `'eleicoes'` - Eleições
- `'independencia_do_brasil'` - Independência do Brasil
- `'nossa_senhora_aparecida'` - Nossa Senhora Aparecida
- `'pascoa'` - Páscoa
- `'proclamacao_da_republica'` - Proclamação da República
- `'sexta_feira_santa'` - Sexta-Feira Santa
- `'confraternizacao_universal'` - Confraternização Universal
- `'copa_do_mundo'` - Copa do Mundo
- `'covid'` - COVID-19
- `'dia_das_maes'` - Dia das Mães
- `'dia_de_finados'` - Dia de Finados
- `'dia_dos_namorados'` - Dia dos Namorados
- `'dia_dos_pais'` - Dia dos Pais

**Exemplos:**
```python
# Nenhum evento especial
VARIAVEIS_FUTURAS = []

# Apenas Black Friday e Natal
VARIAVEIS_FUTURAS = ['black_friday', 'natal']

# Múltiplos eventos
VARIAVEIS_FUTURAS = ['black_friday', 'carnaval', 'natal', 'halloween']

# Todos os eventos importantes
VARIAVEIS_FUTURAS = ['black_friday', 'carnaval', 'natal', 'halloween', 
                     'dia_do_trabalhador', 'eleicoes', 'independencia_do_brasil',
                     'nossa_senhora_aparecida', 'pascoa', 'proclamacao_da_republica',
                     'sexta_feira_santa', 'confraternizacao_universal', 'copa_do_mundo',
                     'covid', 'dia_das_maes', 'dia_de_finados', 'dia_dos_namorados',
                     'dia_dos_pais']
```

## 🔧 6. VARIAVEIS_HISTORICAS

**O que é:** Selecione características temporais dos dados históricos.

**Opções disponíveis:**
- `'dayofweek'` - Dia da semana (0=Segunda, 6=Domingo)
- `'monthofyear'` - Mês do ano (1=Janeiro, 12=Dezembro)

**Exemplos:**
```python
# Nenhuma característica temporal
VARIAVEIS_HISTORICAS = []

# Apenas dia da semana
VARIAVEIS_HISTORICAS = ['dayofweek']

# Dia da semana e mês
VARIAVEIS_HISTORICAS = ['dayofweek', 'monthofyear']
```

## 🚀 Exemplos de Configuração

### Configuração Mínima (Teste Rápido)
```python
MARCAS = ['BB']
TIPOS_PREVISAO = ['GERAL']
MODELOS_A_EXECUTAR = ['LSTM']
METRICS = ['MAPE']
VARIAVEIS_FUTURAS = []
VARIAVEIS_HISTORICAS = ['dayofweek']
```

### Configuração Média (Teste Completo)
```python
MARCAS = ['BB', 'LL']
TIPOS_PREVISAO = ['GERAL', 'GRIFFE']
MODELOS_A_EXECUTAR = ['LSTM', 'GRU']
METRICS = ['MAPE', 'RMSE']
VARIAVEIS_FUTURAS = ['black_friday', 'natal']
VARIAVEIS_HISTORICAS = ['dayofweek', 'monthofyear']
```

### Configuração Completa (Produção)
```python
MARCAS = ['BB', 'LL', 'DD', 'JJ']
TIPOS_PREVISAO = ['GERAL', 'GRIFFE', 'GRIFFE_N1']
MODELOS_A_EXECUTAR = ['LSTM', 'GRU', 'NHITS', 'NBEATSx']
METRICS = ['MAPE', 'RMSE', 'MAE']
VARIAVEIS_FUTURAS = ['black_friday', 'carnaval', 'natal', 'halloween', 
                     'dia_do_trabalhador', 'eleicoes', 'independencia_do_brasil',
                     'nossa_senhora_aparecida', 'pascoa', 'proclamacao_da_republica',
                     'sexta_feira_santa', 'confraternizacao_universal', 'copa_do_mundo',
                     'covid', 'dia_das_maes', 'dia_de_finados', 'dia_dos_namorados',
                     'dia_dos_pais']
VARIAVEIS_HISTORICAS = ['dayofweek', 'monthofyear']
```

## ⚡ Dicas de Performance

1. **Para testes rápidos:** Use configuração mínima
2. **Para desenvolvimento:** Use configuração média
3. **Para produção:** Use configuração completa
4. **Para economizar tempo:** Comece com poucos modelos e adicione gradualmente
5. **Para economizar memória:** Processe uma marca por vez

## 🔍 Como Verificar se a Configuração Está Correta

1. Abra o arquivo `src/config/settings.py`
2. Verifique se as listas estão no formato correto: `['item1', 'item2']`
3. Certifique-se de que não há vírgulas extras no final das listas
4. Execute um teste simples para verificar se tudo funciona

## 📊 Impacto das Configurações

| Configuração | Impacto no Tempo | Impacto na Memória | Impacto na Precisão |
|--------------|------------------|-------------------|---------------------|
| Mais marcas | ⬆️ Aumenta | ⬆️ Aumenta | ⬆️ Melhora |
| Mais tipos | ⬆️ Aumenta | ⬆️ Aumenta | ⬆️ Melhora |
| Mais modelos | ⬆️ Aumenta | ⬆️ Aumenta | ⬆️ Melhora |
| Mais métricas | ➡️ Mantém | ➡️ Mantém | ⬆️ Melhora |
| Mais variáveis | ⬆️ Aumenta | ⬆️ Aumenta | ⬆️ Melhora | 