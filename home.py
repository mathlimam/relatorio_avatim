import streamlit as st
from PIL import Image
import numpy as np

logo = Image.open("logo.png")

st.set_page_config(layout="wide")
st.image(logo) 
st.header("Análise de dados")




st.write("Esta análise de dados foi conduzida com base no dataframe extraído do sistema Exatto, referentes à loja do Pátio Buriti, abrangendo o período de 01 de Janeiro de 2023 a 01 de Janeiro de 2024. O foco principal envolveu duas abordagens distintas: a análise dos clientes e a análise dos produtos.")


st.divider()
st.markdown("#### Análise de Clientes:")
st.write("""Na seção dedicada aos clientes, priorizamos a identificação dos clientes com as melhores compras. Além disso, realizamos um estudo detalhado do perfil de cada cliente. Exploramos aspectos como as linhas de produtos mais adquiridas e outros padrões de compra. O objetivo é personalizar conteúdos e ofertas específicas, entregues via WhatsApp, para aumentar o engajamento e fidelidade desses clientes.

Outro ponto de foco na análise de clientes foi a identificação daqueles que fizeram boas compras no passado, mas que não realizaram nenhuma transação nos últimos 4 meses. Para esses clientes, estamos estudando estratégias para reatraí-los, visando reativar seu interesse na loja e incentivá-los a realizar novas compras.
""")
st.divider()
st.markdown("#### Análise de Produtos:")
st.write("""Na seção dedicada aos produtos, buscamos entender o desempenho de vendas em relação aos grupos de produtos. Descobrimos quais são os grupos mais vendidos, bem como os produtos mais vendidos em cada grupo. Essas informações são cruciais para ajustar estratégias de estoque, marketing e promoções.

Além disso, identificamos os 10 produtos mais lucrativos do último ano. Essa análise é fundamental para maximizar a rentabilidade da loja, concentrando esforços em produtos que contribuem significativamente para os resultados financeiros.""")

st.divider()
st.markdown("""
            Em resumo, as análises abrangem uma abordagem abrangente para otimizar o desempenho de vendas, focando na compreensão aprofundada dos clientes e na maximização da eficácia das estratégias relacionadas aos produtos. Essas informações proporcionam uma base sólida para decisões informadas e aprimoramento contínuo das operações de vendas.
            """)
st.write("Data: 05/01/2024 - Responsável pelo estudo: Matheus Lima Moreira")
