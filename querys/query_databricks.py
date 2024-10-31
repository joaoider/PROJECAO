#base
from configuracoes import marca

#print(marca)

def get_sales_data(marca, griffe_list, data_inicio, data_fim):
    griffe_condition = ', '.join(f"'{griffe}'" for griffe in griffe_list)
    
    query = f"""
    SELECT A.DATA, D.MARCA_SIGLA, split_part(A.ID_LOJA_VENDA, ':',2) as CODIGO_FILIAL, 
           A.CANAL_ORIGEM, A.LINHA, A.GRUPO, A.TIPO_VENDA, A.STATUS_PRODUTO, 
           B.CIDADE, B.UF, C.GRIFFE, sum(A.VLF) AS VLF, SUM(A.QLF) AS QLF, 
           sum(A.ROL) AS ROL, sum(A.CPV) AS CPV, AVG(A.VLF) AS MEDIA_VLF, 
           AVG(A.QLF) AS MEDIA_QLF, AVG(A.ROL) AS MEDIA_ROL, AVG(A.CPV) AS MEDIA_CPV
    FROM gold_planejamento.fact_faturamento_B2c A
    JOIN gold.dim_filiais B ON split_part(A.ID_LOJA_VENDA, ':',2) = B.CODIGO_FILIAL
    JOIN gold_planejamento.dim_produtos C on A.PRODUTO = C.PRODUTO
    JOIN gold_planejamento.dim_marcas D ON A.REDE_LOJAS_VENDA = D.REDE_LOJAS
    WHERE D.MARCA_SIGLA = '{marca}' 
      AND C.GRIFFE in ({griffe_condition})
      AND DATA BETWEEN '{data_inicio}' AND '{data_fim}'
    GROUP BY A.DATA, D.MARCA_SIGLA, A.ID_LOJA_VENDA, A.CANAL_ORIGEM, A.LINHA, A.GRUPO, 
             A.TIPO_VENDA, A.STATUS_PRODUTO, B.CIDADE, B.UF, C.GRIFFE
    """
    
    df = sql(query)
    return df

if marca == 'LL':
  print(marca)
  data = get_sales_data('LL', ['Le Lis Blanc Deux', 'Le Lis Casa', 'Le Lis Beaute'], '2013-01-01', '2023-09-30')
elif marca == 'JJ':
  data = get_sales_data('JJ', ['John John Fem', 'John John Masc'], '2013-01-01', '2023-09-30')
elif marca == 'DD':
  data = get_sales_data('DD', ['Dudalina Masc', 'Dudalina Fem'], '2018-01-01', '2023-09-30')

#liquidacao  
def get_liquidacao_data(marca, data_inicio):
    query = f"""
    SELECT * 
    FROM gold.dim_colecoes_liquidacao 
    WHERE marca = '{marca}' 
      AND DATA_INICIO_LIQUIDACAO >= '{data_inicio}'
    """
    
    df = sql(query)
    return df

if marca == 'LL':
  data_liqui = get_liquidacao_data('LL',  '2012-01-01')
elif marca == 'DD': 
  data_liqui = get_liquidacao_data('DD', '2012-01-01')
elif marca == 'JJ':
  data_liqui = get_liquidacao_data('JJ', '2012-01-01')
