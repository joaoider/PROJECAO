#base

df = sql(""" 
            SELECT A.DATA,D.MARCA_SIGLA, split_part(A.ID_LOJA_VENDA, ':',2) as CODIGO_FILIAL, 
                   A.CANAL_ORIGEM, A.LINHA, A.GRUPO, A.TIPO_VENDA, A.STATUS_PRODUTO, 
                   B.CIDADE, B.UF, C.GRIFFE, sum(A.VLF) AS VLF, SUM(A.QLF) AS QLF, sum(A.ROL) AS ROL, sum(A.CPV) AS CPV, AVG(A.VLF) AS MEDIA_VLF, AVG(A.QLF) AS MEDIA_QLF, AVG(A.ROL) AS MEDIA_ROL, AVG(A.CPV) AS MEDIA_CPV
            FROM gold_planejamento.fact_faturamento_B2c A
            JOIN gold.dim_filiais B ON split_part(A.ID_LOJA_VENDA, ':',2) = B.CODIGO_FILIAL
            JOIN gold_planejamento.dim_produtos C on A.PRODUTO = C.PRODUTO
            JOIN gold_planejamento.dim_marcas D ON A.REDE_LOJAS_VENDA = D.REDE_LOJAS
            -- 'JJ' 'DD' 'LL'
            WHERE D.MARCA_SIGLA = 'JJ' 
              -- 'John John Fem', 'John John Masc'
              -- 'Le Lis Blanc Deux', 'Le Lis Casa', 'Le Lis Beaute'
              -- 'Dudalina Masc', 'Dudalina Fem'
              AND C.GRIFFE in ('John John Fem', 'John John Masc')
              AND DATA BETWEEN '2013-01-01' AND '2024-09-30'
            GROUP BY A.DATA, D.MARCA_SIGLA, A.ID_LOJA_VENDA, A.CANAL_ORIGEM, A.LINHA, A.GRUPO, A.TIPO_VENDA, A.STATUS_PRODUTO, B.CIDADE, B.UF, C.GRIFFE
        """)

#liquidacao

   
  # Query dinâmica para cada marca
df2 = sql(""" 
        select * from gold.dim_colecoes_liquidacao 
        where marca = 'DD' and DATA_INICIO_LIQUIDACAO >= '2012-01-01' 
        --where marca = 'JJ' and DATA_INICIO_LIQUIDACAO >= '2012-01-01'
        --where marca = 'LL' and DATA_INICIO_LIQUIDACAO >= '2012-01-01'
          """)