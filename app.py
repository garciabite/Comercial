# Importa as bibliotecas necessárias-----------------------------------------------------------------
import streamlit as st                  # Biblioteca para criar a aplicação web
import pandas as pd                     # Biblioteca para manipulação de dados em DataFrames
import os                               # Biblioteca para lidar com arquivos no sistema operacional
import plotly.express as px
from datetime import datetime           # Para lidar com datas
from funcao.auxiliar import carregar, filtro,salvar,cronograma,lateral
from funcao.estilo import abas

# ---------------------------------------------------------------------------------------------------

# 1.0>>> Configura a página do Streamlit (título da aba e layout em largura total)
st.set_page_config(page_title="Gestão Comercial",layout="wide")

lateral()

#st.sidebar.image("painel.png", caption="", use_container_width=True)

# 1.1>>> Título principal exibido na página
#st.sidebar.title("Gestão Comercial")

# 1.2>>> Criando as abas
abas()
aba1, aba2 = st.tabs(["Exibir Projetos", "Indicadores"])

# ---------------------------------------------------------------------------------------------------

# 2.0>>> Configurando a primeira aba

with aba1:
    # 2.1>>> Especificando as colunas de exibição
    
    colunas =["Codigo",
          "Cliente",
          "Deadline",
          "TAP",
          "Eng. Produto",
          "Eng. Aplicação",
          "Projeto Elétrico",
          "Compras",
          "Montagem Elétrica",
          "Testes E/M",
          "Automação",
          "Tryout",
          "Embalagem"
          ]

    # 2.2>>>  Nome do arquivo/Dataframe
    BASE = "Dados Comerciais.csv"

    base_dados = carregar()

    base_filtrada = filtro(base_dados,colunas)

    # 2.3>>> Botão de salvar
    if st.button("💾 Salvar"):
        salvar(base_filtrada,BASE)
        st.success("Dados salvos com sucesso!")

# 3.0>>> Configurando a segunda aba

    with aba2:
        #3.1>>> Inserindo Subtitulo
        #st.subheader("Projetos em Andamento")
        cronograma()
