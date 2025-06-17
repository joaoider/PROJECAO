# Projeto de Previsão de Vendas

Este projeto implementa um sistema de previsão de vendas utilizando diferentes modelos de machine learning e deep learning.

## Estrutura do Projeto

```
projecao/
├── src/                    # Código fonte principal
│   ├── models/            # Implementações dos modelos
│   │   ├── __init__.py
│   │   ├── base_model.py
│   │   ├── lstm_model.py
│   │   ├── gru_model.py
│   │   ├── nhits_model.py
│   │   └── nbeatsx_model.py
│   ├── utils/             # Utilitários e funções auxiliares
│   │   ├── __init__.py
│   │   ├── data_processing.py
│   │   └── metrics.py
│   ├── config/            # Configurações do projeto
│   │   ├── __init__.py
│   │   └── settings.py
│   └── main.py            # Ponto de entrada principal
├── data/                  # Dados do projeto
│   ├── raw/              # Dados brutos
│   ├── processed/        # Dados processados
│   └── forecasts/        # Previsões geradas
├── notebooks/            # Jupyter notebooks para análise
├── tests/                # Testes unitários
├── docs/                 # Documentação
├── requirements.txt      # Dependências do projeto
└── README.md            # Este arquivo
```

## Requisitos

- Python 3.8+
- Dependências listadas em `requirements.txt`

## Instalação

1. Clone o repositório:
```bash
git clone [URL_DO_REPOSITORIO]
cd [NOME_DO_DIRETORIO]
```

2. Crie um ambiente virtual:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

## Uso

1. Configure as variáveis de ambiente em um arquivo `.env`:
```
MARCA=default
DATA_INICIO=2020-01-01
DATA_FIM=2024-12-31
```

2. Execute o pipeline completo:
```bash
python src/main.py
```

## Modelos Implementados

- LSTM
- GRU
- NHITS
- NBEATSx

## Testes

Execute os testes unitários:
```bash
pytest tests/
```

## Contribuição

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/nova-feature`)
3. Commit suas mudanças (`git commit -m 'Adiciona nova feature'`)
4. Push para a branch (`git push origin feature/nova-feature`)
5. Abra um Pull Request

## Licença

Este projeto está licenciado sob a licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes. 