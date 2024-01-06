import pandas as pd
import plotly.express as px
import streamlit as st

def faturamento_por_grupo(sdf):
    # Gráfico de barras para o faturamento total por grupo
    fig = px.bar(sdf.groupby('GRUPO')['FATURAMENTO TOTAL'].sum().reset_index(), x='GRUPO', y="FATURAMENTO TOTAL", title="Faturamento total por grupo")
    st.plotly_chart(fig)

def produtos_mais_vendidos_por_grupo(sdf):
    # Produto mais vendido por grupo
    idx = sdf.groupby('GRUPO')['QTD'].idxmax()
    produto_mais_vendido_por_grupo = sdf.loc[idx, ['GRUPO', 'DESCRIÇÃO', 'QTD', 'FATURAMENTO TOTAL']]
    st.write("Produto mais vendido por grupo:")
    st.table(produto_mais_vendido_por_grupo)

def produtos_mais_lucrativos(sdf):
    # Produto mais lucrativo
    sdf['LUCRO POR UNIDADE'] = sdf['FAT - CUSTO'] / sdf['QTD']
    sdf['INDICATIVO DE LUCRATIVIDADE'] = sdf['LUCRO POR UNIDADE'] * sdf['QTD']
    produto_mais_lucrativo = sdf.sort_values(by='INDICATIVO DE LUCRATIVIDADE', ascending=False).head(10)
    
    # Exibição do produto mais lucrativo
    st.write("Produtos mais lucrativos:")
    fig = px.bar(produto_mais_lucrativo, x='DESCRIÇÃO', y='INDICATIVO DE LUCRATIVIDADE', title="Top 10 Produtos Mais Lucrativos")
    st.plotly_chart(fig)

def main():
    # Leitura do arquivo Excel
    sdf = pd.read_excel("sales_db.xlsx")
    st.set_page_config(layout='wide')

    # Escolher entre análise de produtos e clientes
    analise_selecionada = st.sidebar.radio("Escolha a Análise", ["Produtos", "Clientes"])

    st.title('Análise de dados')

    # Layout com duas colunas
    left, right = st.columns(2)

    # Executar a análise de produtos
    if analise_selecionada == "Produtos":
        with left:
            faturamento_por_grupo(sdf)
            produtos_mais_vendidos_por_grupo(sdf)

        with right:
            produtos_mais_lucrativos(sdf)

    # Adicionar aqui a lógica para a análise de clientes se necessário

if __name__ == '__main__':
    main()