import pandas as pd
from datetime import datetime, timedelta
import streamlit as st
import locale
locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')


# Carregando o dataframe
df = pd.read_excel('clients_db.xlsx')

# Convertendo a coluna 'DATA' para o formato de data
df['DATA'] = pd.to_datetime(df['DATA'], format='%d/%m/%Y')

# Criando coluna 'MES' para facilitar a segmentação por mês
df['MES'] = df['DATA'].dt.month

# Criando uma coluna 'TOTAL' para representar o valor total da compra (QUANTIDADE VENDIDA * VALOR UNITARIO)
df['TOTAL'] = df['QUANTIDADE VENDIDA'] * df['VALOR UNITARIO']

# Criando uma coluna 'BOM_CLIENTE' e iniciando com 'Não'
df['BOM_CLIENTE'] = 'Não'

# Criando um dataframe separado para os clientes
clientes_df = df[['CLIENTE', 'CNPJ / CPF']].drop_duplicates()

# Inicializando a coluna 'STATUS' para 'Inativo'
clientes_df['STATUS'] = 'Inativo'

# Adicionando a data da última compra dos clientes
clientes_df['ULTIMA_COMPRA'] = df.groupby('CLIENTE')['DATA'].transform("max")

# Identificando clientes ativos
data_base = datetime.now()
data_limite_ativos = data_base - timedelta(days=120)
ultimas_compras = df.groupby('CLIENTE')['DATA'].max().reset_index(name='ULTIMA_COMPRA')


ativos = ultimas_compras.loc[ultimas_compras['ULTIMA_COMPRA'] >= data_limite_ativos, 'CLIENTE']

# Ajustando a lógica para clientes ativos
clientes_df.loc[clientes_df['CLIENTE'].isin(ativos), 'STATUS'] = 'Ativo'

# Juntando a coluna 'BOM_CLIENTE' ao dataframe 'clientes_df'
clientes_df = clientes_df.merge(df[['CLIENTE', 'BOM_CLIENTE']].drop_duplicates(), on='CLIENTE', how='left')

# Criando a coluna "SOMA_COMPRAS"
clientes_df['CLIENTE'] = df['CLIENTE'].unique()
# Calculando a soma de compras anuais para cada cliente
clientes_df['SOMA_COMPRAS'] = clientes_df['CLIENTE'].apply(lambda x: df.loc[df['CLIENTE'] == x].groupby('CLIENTE')['TOTAL'].sum().sum())


# Atualizando 'BOM_CLIENTE' para 'Sim' se o cliente estiver ativo e a soma de compras for maior que R$1.000,00
clientes_df.loc[(clientes_df['SOMA_COMPRAS'] > 1000), 'BOM_CLIENTE'] = 'Sim'

# Filtrando apenas os bons clientes
bons_clientes_df = clientes_df[clientes_df['BOM_CLIENTE'] == 'Sim']

#bons_clientes_df.to_excel("bons_clientes.xlsx", index=False)  -tirar comentário ao atualizar planilha

contagem_ativos = bons_clientes_df[clientes_df['STATUS'] == 'Ativo'].shape[0]
contagem_inativos = bons_clientes_df[clientes_df['STATUS'] == 'Inativo'].shape[0]

# Calcular a quantidade de vezes (dias distintos) que os bons clientes foram à loja
bons_clientes_df['QTD_VEZES'] = df.groupby('CLIENTE')['DATA'].transform("nunique")


# Calcular a média diária para os bons clientes
bons_clientes_df['MEDIA_DIARIA'] = bons_clientes_df['SOMA_COMPRAS'] / bons_clientes_df['QTD_VEZES']

# Preencher possíveis valores NaN com 0, indicando que foram compras únicas
bons_clientes_df['MEDIA_DIARIA'] = bons_clientes_df['MEDIA_DIARIA'].fillna(1)

# Encontrar o grupo de produtos mais comprado por cada cliente
grupo_mais_comprado = df.groupby(['CLIENTE', 'grupo'])['QUANTIDADE VENDIDA'].sum().reset_index()
grupo_mais_comprado = grupo_mais_comprado.loc[grupo_mais_comprado.groupby('CLIENTE')['QUANTIDADE VENDIDA'].idxmax()]

# Adicionar a coluna 'grupo' ao bons_clientes_df
bons_clientes_df = pd.merge(bons_clientes_df, grupo_mais_comprado[['CLIENTE', 'grupo']], on='CLIENTE', how='left')
bons_clientes_df.rename(columns={'grupo': 'GRUPO_MAIS_COMPRADO'}, inplace=True)


# Encontrar a caracteristica de produtos mais comprada por cada cliente
caracteristica_mais_comprada = df.groupby(['CLIENTE', 'caracteristica'])['QUANTIDADE VENDIDA'].sum().reset_index()
caracteristica = caracteristica_mais_comprada.loc[caracteristica_mais_comprada.groupby('CLIENTE')['QUANTIDADE VENDIDA'].idxmax()]

# Adicionar a coluna 'grupo' ao bons_clientes_df
bons_clientes_df = pd.merge(bons_clientes_df, caracteristica_mais_comprada[['CLIENTE', 'caracteristica']], on='CLIENTE', how='left')
bons_clientes_df.rename(columns={'caracteristica': 'CARACTERISTICA_MAIS_COMPRADA'}, inplace=True)

#bons_clientes_df.to_excel('bons_clientes_df.xlsx') - tirar comentário ao atualizar planilha

# Título do Dashboard
def main():
    # Título do Dashboard
    st.set_page_config(
        layout='wide',
        page_title="Análise de clientes"
                       )
    st.title('Análise de Clientes')


    # Métricas gerais
    left, right = st.columns(2)

    with left:
        st.header('Métricas Gerais:')
        subleft, subright = st.columns(2)

        with subleft:
            quantidade_total_clientes = clientes_df.shape[0]
            st.metric("Total de Clientes em 2023: ", quantidade_total_clientes)

            # Quantidade de bons clientes
            df_bons_clientes = pd.read_excel("bons_clientes.xlsx")
            quantidade_bons_clientes = df_bons_clientes.shape[0]
            st.metric("Clientes destaques:", quantidade_bons_clientes)
        
        # Tabela de Clientes com Grupo Mais Comprado
            
        st.header("Grupos mais comprados pelos clientes ativos ")
        df_clientes_ativos = bons_clientes_df[bons_clientes_df['STATUS'] == 'Ativo']
        df_clientes_grupo_mais_comprado = df_clientes_ativos[['CLIENTE', 'GRUPO_MAIS_COMPRADO', 'SOMA_COMPRAS']]
        df_clientes_grupo_mais_comprado = df_clientes_grupo_mais_comprado.drop_duplicates(subset=['CLIENTE'])
        df_clientes_grupo_mais_comprado['SOMA_COMPRAS_FORMATADO'] = df_clientes_grupo_mais_comprado['SOMA_COMPRAS']

        st.write(df_clientes_grupo_mais_comprado[['CLIENTE', 'GRUPO_MAIS_COMPRADO', 'SOMA_COMPRAS_FORMATADO']], use_container_width=True)
    # Quantidade de clientes ativos e inativos
        
        with subright:
            
            quantidade_clientes_ativos = df_bons_clientes[df_bons_clientes['STATUS'] == 'Ativo'].shape[0]
            quantidade_clientes_inativos = df_bons_clientes[df_bons_clientes['STATUS'] == 'Inativo'].shape[0]
            st.metric(" - Ativos", quantidade_clientes_ativos)
            st.metric(" - Inativos", quantidade_clientes_inativos)

    with right:
        # Valor gasto por bons clientes no ano passado
        valor_gasto_bons_clientes = df_bons_clientes['SOMA_COMPRAS'].sum()

        st.metric("Valor Gasto por Clientes Destaques", f'R$ {valor_gasto_bons_clientes}')

        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.write("")

        st.header("Grupos mais comprados pelos clientes inativos ")
        df_clientes_inativos = bons_clientes_df[bons_clientes_df['STATUS'] == 'Inativo'] 
        df_clientes_grupo_mais_comprado = df_clientes_inativos[['CLIENTE', 'GRUPO_MAIS_COMPRADO', 'SOMA_COMPRAS']]
        df_clientes_grupo_mais_comprado = df_clientes_grupo_mais_comprado.drop_duplicates(subset=['CLIENTE'])
        df_clientes_grupo_mais_comprado['SOMA_COMPRAS_FORMATADO'] = df_clientes_grupo_mais_comprado['SOMA_COMPRAS']

        st.write(df_clientes_grupo_mais_comprado[['CLIENTE', 'GRUPO_MAIS_COMPRADO', 'SOMA_COMPRAS_FORMATADO']], use_container_width=True)

    # Grupos mais comprados por bons clientes
    st.header('Grupos Mais Comprados por Clientes destaques')
    #grupos_mais_comprados = bons_clientes_df['GRUPO_MAIS_COMPRADO'].value_counts()
    grupos_mais_comprados = bons_clientes_df.drop_duplicates(subset=['CLIENTE', 'GRUPO_MAIS_COMPRADO']).groupby('GRUPO_MAIS_COMPRADO')['CLIENTE'].count()
    st.bar_chart(grupos_mais_comprados)

    # Características mais compradas por bons clientes
    st.header('Características Mais Compradas por Clientes destaques')
    caracteristicas_mais_compradas = bons_clientes_df.drop_duplicates(subset=['CLIENTE','CARACTERISTICA_MAIS_COMPRADA']).groupby('CARACTERISTICA_MAIS_COMPRADA')['CLIENTE'].count()
    st.bar_chart(caracteristicas_mais_compradas)

# Adicione mais visualizações conforme necessário

# Rodar o aplicativo Streamlit
if __name__ == '__main__':
    main()
