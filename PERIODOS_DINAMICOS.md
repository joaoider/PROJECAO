# Períodos Dinâmicos - Documentação das Mudanças

## Resumo das Modificações

O programa foi modificado para usar **períodos dinâmicos** baseados na data atual, em vez de datas fixas. Isso garante que o modelo sempre use dados atualizados e relevantes.

## Como Funciona Agora

### 1. **Data Atual**
- O programa usa `datetime.now()` como referência para todos os cálculos
- Todas as datas são calculadas dinamicamente a partir desta data

### 2. **Período de Treinamento**
- **Início**: `2020-01-01` (fixo)
- **Fim**: `DATA_ATUAL - 365 dias` (1 ano atrás da data atual)
- **Objetivo**: Treinar o modelo com dados históricos até 1 ano atrás

### 3. **Período de Teste**
- **Início**: `DATA_ATUAL - 365 dias` (1 ano atrás)
- **Fim**: `DATA_ATUAL` (hoje)
- **Objetivo**: Calcular métricas (MAPE, RMSE, etc.) usando o último ano de dados

### 4. **Período de Previsões Futuras**
- **Início**: `DATA_ATUAL` (hoje)
- **Fim**: `DATA_ATUAL + 365 dias` (1 ano à frente)
- **Objetivo**: Gerar previsões para o próximo ano

## Exemplo Prático

Se o programa for executado em **15 de Janeiro de 2025**:

| Período | Início | Fim | Duração |
|---------|--------|-----|---------|
| **Treinamento** | 2020-01-01 | 2024-01-15 | ~4 anos |
| **Teste** | 2024-01-15 | 2025-01-15 | 1 ano |
| **Previsões** | 2025-01-15 | 2026-01-15 | 1 ano |

## Arquivo Parquet Final

O arquivo Parquet final conterá:
- **1 ano de dados de teste** (valores reais vs previstos)
- **1 ano de previsões futuras** (valores previstos)

**Total**: 2 anos de dados (1 ano de teste + 1 ano de previsões)

## Vantagens da Abordagem Dinâmica

1. **Sempre Atualizado**: O modelo sempre usa dados recentes
2. **Período de Teste Consistente**: Sempre 1 ano para validação
3. **Previsões Relevantes**: Sempre 1 ano à frente
4. **Flexibilidade**: Não precisa alterar datas manualmente
5. **Comparabilidade**: Períodos consistentes entre execuções

## Configurações no Código

As configurações estão em `src/config/settings.py`:

```python
# Data atual para cálculos dinâmicos
DATA_ATUAL = datetime.now()

# Período de treinamento: até 1 ano atrás da data atual
DATA_TRAIN = (DATA_ATUAL - timedelta(days=365)).strftime('%Y-%m-%d')

# Período de teste: último ano (desde 1 ano atrás até hoje)
DATA_TEST = (DATA_ATUAL - timedelta(days=365)).strftime('%Y-%m-%d')

# Período de previsões futuras: próximo ano (desde hoje até 1 ano à frente)
DATA_INICIO_FUTR = DATA_ATUAL.strftime('%Y-%m-%d')
DATA_FINAL_FUTR = (DATA_ATUAL + timedelta(days=365)).strftime('%Y-%m-%d')
```

## Logs Informativos

O programa agora exibe logs detalhados sobre os períodos:

```
Período de treinamento: até 2024-01-15
Período de teste: 2024-01-15 até 2025-01-15
Período de previsões futuras: 2025-01-15 até 2026-01-15
```

## Compatibilidade

- ✅ Mantém compatibilidade com código existente
- ✅ Não quebra funcionalidades anteriores
- ✅ Logs detalhados para debug
- ✅ Configuração centralizada 