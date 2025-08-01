"""
Módulo responsável por executar queries no Databricks e retornar os dados necessários.
"""
import os
from pyspark.sql import SparkSession
from typing import Dict, List, Union
import pandas as pd
from config.settings import MARCAS, DATA_INICIO_BASE

# Inicializar a sessão Spark de forma condicional
if "DATABRICKS_RUNTIME_VERSION" in os.environ:
    spark = SparkSession.getActiveSession()
    if spark is None:
        spark = SparkSession.builder.getOrCreate()
else:
    # Configuração local
    spark = SparkSession.builder.master("local[*]").appName("MyApp").getOrCreate()

class DataQueries:
    """Classe responsável por executar queries no Databricks."""
    
    def __init__(self):
        """Inicializa a classe com as configurações de griffe."""
        # Configuração para previsão geral (todas as griffes da marca)
        self.griffe_config_geral = {
            'BB':  { 'griffe': ['Bobô', 'Bobo Casa'], 'data_inicio': '2013-01-01' },
            'DD':  { 'griffe': ['Dudalina Masc', 'Dudalina Fem'], 'data_inicio': '2018-01-01' },
            'JJ':  { 'griffe': ['John John Fem', 'John John Masc'], 'data_inicio': '2013-01-01' },
            'LL':  { 'griffe': ['Le Lis Blanc Deux', 'Le Lis Casa', 'Le Lis Noir', 'Le Lis Beaute'], 'data_inicio': '2013-01-01' },
        }

        # Configuração para previsão por griffe específica
        self.griffe_config_unico = {
            'BB':  [ {'griffe': ['Bobô'], 'data_inicio': '2013-01-01'} ],
            'DD':  [ {'griffe': ['Dudalina Fem'], 'data_inicio': '2018-01-01'},
                    {'griffe': ['Dudalina Masc'], 'data_inicio': '2018-01-01'} ],
            'JJ':  [ {'griffe': ['John John Fem'], 'data_inicio': '2013-01-01'},
                    {'griffe': ['John John Masc'], 'data_inicio': '2013-01-01'} ],
            'LL':  [ {'griffe': ['Le Lis Blanc Deux'], 'data_inicio': '2013-01-01'} ],
        }

        # Configuração para previsão por griffe e linha
        self.griffe_linha_config = {
            'BB': {
                'Bobô': [
                    'Acessorio', 'Alfaiataria', 'Aroma', 'Casual',
                    'Casual/Ville/Tricot/Moda', 'Couro', 'Jeans e Sarja', 'Jeans/Sarja',
                    'Malha', 'Malha e Moletom', 'Moda', 'Outros', 'Seda'
                ]
            },
            'DD': {
                'Dudalina Fem': ['Alfaiataria', 'Jeans e Sarja', 'Malha', 'Outros', 'Tecido Plano'],
                'Dudalina Masc': ['Alfaiataria', 'Jeans e Sarja', 'Malha', 'Outros', 'Tecido Plano']
            },
            'JJ': {
                'John John Fem': ['Alfaiataria', 'Jeans e Sarja', 'Malha', 'Outros', 'Tecido Plano'],
                'John John Masc': ['Alfaiataria', 'Jeans e Sarja', 'Malha', 'Outros', 'Tecido Plano']
            },
            'LL': {
                'Le Lis Blanc Deux': ['Alfaiataria', 'Jeans e Sarja', 'Malha', 'Outros', 'Tecido Plano']
            }
        }

    def get_sales_data(self, marca: str, griffe_list: List[str], data_inicio: str, data_fim: str = None) -> pd.DataFrame:
        """
        Obtém dados de vendas para uma marca e lista de griffes específicas.
        
        Args:
            marca: Sigla da marca
            griffe_list: Lista de griffes para filtrar
            data_inicio: Data inicial para filtrar os dados
            data_fim: Data final para filtrar os dados (opcional)
            
        Returns:
            DataFrame com os dados de vendas
        """
        griffe_condition = ', '.join(f"'{griffe}'" for griffe in griffe_list)
        
        # Construir a condição de data
        data_condition = f"DATA >= '{data_inicio}'"
        if data_fim:
            data_condition += f" AND DATA <= '{data_fim}'"
        
        query = f"""
        SELECT A.DATA, D.MARCA_SIGLA, split_part(A.ID_LOJA_VENDA, ':',2) as CODIGO_FILIAL, 
               A.CANAL_ORIGEM, A.LINHA, A.GRUPO, A.CATEGORIA_N1, A.TIPO_VENDA, A.STATUS_PRODUTO, 
               B.CIDADE, B.UF, C.GRIFFE, CAST(sum(A.VLF) AS DOUBLE) AS VLF, CAST(SUM(A.QLF) AS DOUBLE) AS QLF, 
               CAST(sum(A.ROL) AS DOUBLE) AS ROL, CAST(sum(A.CPV) AS DOUBLE) AS CPV, CAST(AVG(A.VLF) AS DOUBLE) AS MEDIA_VLF, 
               CAST(AVG(A.QLF) AS DOUBLE) AS MEDIA_QLF, CAST(AVG(A.ROL) AS DOUBLE) AS MEDIA_ROL, CAST(AVG(A.CPV) AS DOUBLE) AS MEDIA_CPV
        FROM gold_planejamento.fact_faturamento_B2c A
        JOIN gold.dim_filiais B ON split_part(A.ID_LOJA_VENDA, ':',2) = B.CODIGO_FILIAL
        JOIN gold_planejamento.dim_produtos C on A.PRODUTO = C.PRODUTO
        JOIN gold_planejamento.dim_marcas D ON A.REDE_LOJAS_VENDA = D.REDE_LOJAS
        WHERE D.MARCA_SIGLA = '{marca}' 
          AND C.GRIFFE in ({griffe_condition})
          AND {data_condition}
        GROUP BY A.DATA, D.MARCA_SIGLA, A.ID_LOJA_VENDA, A.CANAL_ORIGEM, A.LINHA, A.GRUPO, A.CATEGORIA_N1, 
                 A.TIPO_VENDA, A.STATUS_PRODUTO, B.CIDADE, B.UF, C.GRIFFE
        """
        
        return spark.sql(query).toPandas()

    def get_liquidacao_data(self, marca: str, data_inicio: str) -> pd.DataFrame:
        """
        Obtém dados de liquidação para uma marca específica.
        
        Args:
            marca: Sigla da marca
            data_inicio: Data inicial para filtrar os dados
            
        Returns:
            DataFrame com os dados de liquidação
        """
        query = f"""
        SELECT * 
        FROM gold.dim_colecoes_liquidacao 
        WHERE marca = '{marca}' 
          AND DATA_INICIO_LIQUIDACAO >= '{data_inicio}'
        """
        
        return spark.sql(query).toPandas()

    def execute_query(self, query_type: str, marca: str = None, tipo_previsao: str = None, data_fim: str = None) -> Union[pd.DataFrame, Dict[str, pd.DataFrame]]:
        """
        Executa a query apropriada baseada no tipo de consulta solicitado.
        
        Args:
            query_type: Tipo de consulta ('vendas' ou 'liquidacao')
            marca: Sigla da marca (opcional)
            tipo_previsao: Tipo de previsão (GERAL, GRIFFE, GRIFFE_N1)
            data_fim: Data final para filtrar os dados (opcional)
            
        Returns:
            DataFrame ou dicionário de DataFrames com os resultados
        """
        if query_type == 'vendas':
            if marca is None or tipo_previsao is None:
                raise ValueError("Marca e tipo_previsao são obrigatórios para consultas de vendas")
            
            if tipo_previsao == 'GERAL':
                if marca in self.griffe_config_geral:
                    return self.get_sales_data(
                        marca,
                        self.griffe_config_geral[marca]['griffe'],
                        self.griffe_config_geral[marca]['data_inicio'],
                        data_fim
                    )
                else:
                    raise ValueError(f"Marca '{marca}' não está configurada em griffe_config_geral")
            
            elif tipo_previsao == 'GRIFFE':
                if marca in self.griffe_config_unico:
                    data = {}
                    for conf in self.griffe_config_unico[marca]:
                        griffe_nome = conf['griffe'][0]
                        data[griffe_nome] = self.get_sales_data(
                            marca,
                            conf['griffe'],
                            conf['data_inicio'],
                            data_fim
                        )
                    return data
                else:
                    raise ValueError(f"Marca '{marca}' não está configurada em griffe_config_unico")
            
            elif tipo_previsao == 'GRIFFE_N1':
                if marca in self.griffe_linha_config:
                    data = {}
                    for griffe, linhas in self.griffe_linha_config[marca].items():
                        for linha in linhas:
                            df = self.get_sales_data(marca, [griffe], DATA_INICIO_BASE, data_fim)
                            data[f'{griffe}_{linha}'] = df
                    return data
                else:
                    raise ValueError(f"Marca '{marca}' não está configurada em griffe_linha_config")
            
            else:
                raise ValueError(f"Tipo de previsão '{tipo_previsao}' não é válido")
        
        elif query_type == 'liquidacao':
            if marca is None:
                raise ValueError("Marca é obrigatória para consultas de liquidação")
            return self.get_liquidacao_data(marca, DATA_INICIO_BASE)
        
        else:
            raise ValueError(f"Tipo de consulta '{query_type}' não é válido") 