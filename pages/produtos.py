import pandas as pd
import plotly.express as px
import streamlit as st

def faturamento_por_grupo(sdf):
    # Gráfico de barras para o faturamento total por grupo
    fig = px.bar(sdf.groupby('GRUPO')['FATURAMENTO TOTAL'].sum().reset_index(), x='GRUPO', y="FATURAMENTO TOTAL", title="Faturamento total por grupo")
    st.plotly_chart(fig)

def produtos_mais_vendidos_por_grupo(sdf, grupo_selecionado):
    # Filtrar por grupo selecionado
    produtos_grupo_selecionados = sdf[sdf['GRUPO'] == grupo_selecionado]

    # Gráfico de barras verticais para os produtos mais vendidos no grupo selecionado
    fig = px.bar(
        produtos_grupo_selecionados,
        x='DESCRIÇÃO',
        y='QTD',
        title=f"Produtos mais vendidos no grupo {grupo_selecionado}",
        labels={'QTD': 'Quantidade Vendida', 'DESCRIÇÃO': 'Descrição do Produto'},
        color='QTD',  # Adicionando escala de cores
        color_continuous_scale='Viridis',  # Escolhendo um mapa de cores (pode ser ajustado)
    )

    # Configurar layout para largura de 100%
    fig.update_layout(margin=dict(l=0, r=0, b=0, t=50))  # Ajuste a largura conforme necessário

    st.write(f"Produtos do grupo {grupo_selecionado}:")
    st.plotly_chart(fig, use_container_width=True)

def produtos_mais_lucrativos(sdf):
    # Produto mais lucrativo
    sdf['LUCRO POR UNIDADE'] = sdf['FAT - CUSTO'] / sdf['QTD']
    sdf['INDICATIVO DE LUCRATIVIDADE'] = sdf['LUCRO POR UNIDADE'] * sdf['QTD']
    produto_mais_lucrativo = sdf.sort_values(by='INDICATIVO DE LUCRATIVIDADE', ascending=False).head(10)
    
    # Exibição do produto mais lucrativo com escala de cores
    st.write("Produtos mais lucrativos:")
    fig = px.bar(
        produto_mais_lucrativo,
        x='DESCRIÇÃO',
        y='INDICATIVO DE LUCRATIVIDADE',
        title="Top 10 Produtos Mais Lucrativos",
        color='INDICATIVO DE LUCRATIVIDADE',  # Adicionando escala de cores
        color_continuous_scale='Viridis',  # Escolhendo um mapa de cores (pode ser ajustado)
    )
    st.plotly_chart(fig)

def main():
    # Leitura do arquivo Excel
    sdf = pd.read_excel("sales_db.xlsx")
    st.set_page_config(layout='wide')

    # Escolher entre análise de produtos e clientes
    
    st.title('Análise de dados')

    # Layout com duas colunas
    left, right = st.columns(2)

    # Executar a análise de produtos

    with left:
            faturamento_por_grupo(sdf)
            
    with right:
            produtos_mais_lucrativos(sdf)

        # Seleção do grupo
    grupo_selecionado = st.selectbox("Selecione um grupo", sdf['GRUPO'].unique())

        # Lógica para mostrar os produtos mais vendidos no grupo selecionado
    if grupo_selecionado:
            produtos_mais_vendidos_por_grupo(sdf, grupo_selecionado)

    # Adicionar aqui a lógica para a análise de clientes se necessário

if __name__ == '__main__':
    main()
