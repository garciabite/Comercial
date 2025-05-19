# Importa as bibliotecas necessárias
import streamlit as st                          # Biblioteca para criar a aplicação web
import pandas as pd                             # Biblioteca para manipulação de dados em DataFrames
import os                                       # Biblioteca para lidar com arquivos no sistema operacional
from funcao.estilo import estilo_botao
import plotly.express as px
#from datetime import datetime                   # Para lidar com datas


def lateral():

    st.sidebar.image("painel.png", caption="", use_container_width=True)

    st.sidebar.write("""
    <hr style="border: none; height: 5px; background-image: linear-gradient(to right, #2A6AAE, #ED8232);">
    """, unsafe_allow_html=True)

    # 1.1>>> Título principal exibido na página
    st.sidebar.title("Gestão Comercial")

    st.sidebar.write("""
    <hr style="border: none; height: 5px; background-image: linear-gradient(to right, #2A6AAE, #ED8232);">
    """, unsafe_allow_html=True)

    st.sidebar.write("NOTA:")    
    st.sidebar.write("1) Data de exibição: ano/mês/dia.")
    st.sidebar.write("2) Deadline: Data limite para entrega.")    
    st.sidebar.write("3) TAP: Termo de Abertura do Projeto.")
    st.sidebar.write("4) Clicar em 💾 Salvar ao final do preenchimento.")

    st.sidebar.write("""
    <hr style="border: none; height: 5px; background-image: linear-gradient(to right, #2A6AAE, #ED8232);">
    """, unsafe_allow_html=True)

    st.sidebar.markdown(
        """
        <p style="line-height:1.5;margin-top:175px";>
        <span style="color:#ED8232;"><b>Adm:</b></span> <span style="color:white;">Cristian Garcia</span><br>
        <span style="color:#ED8232;"><b>Data:</b></span> <span style="color:white;">16/05/25</span><br>
        <span style="color:#ED8232;"><b>Versão:</b></span> <span style="color:white;">00</span>
        </p>
        """, unsafe_allow_html=True
    )

#----------------------------------------------------------------------------------------------------------------------

# 1.0>>> Define as colunas esperadas no Dataframe (banco de dados)
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

#----------------------------------------------------------------------------------------------------------------------

# 1.1>>> Criando o banco de dados confome a lista de colunas acima
BASE = "Dados Comerciais.csv"

#----------------------------------------------------------------------------------------------------------------------

# 1.2>>> # Função que carrega os dados do arquivo CSV ou cria um novo arquivo vazio se não existir
def carregar():  
    #1.2.1
    if not os.path.exists(BASE):                
        dados_vazio = pd.DataFrame(columns=colunas)
        dados_vazio.to_csv(BASE, index=False)

    #1.2.2
    dados = pd.read_csv(BASE, dtype={"Codigo": str,"Cliente": str})
  
    #1.2.3
    for col in colunas:                                 
        if col not in dados.columns:
            dados[col] = ""                       
    
    #1.2.4 
    for col in colunas[2:]:
        dados[col] = pd.to_datetime(dados[col])
    return dados  # Retorna o DataFrame carregado e tratado

#----------------------------------------------------------------------------------------------------------------------

# 1.3>>> # Função com o objetivo de filtrar o nome dos clientes, e esta recebe dois parâmetros:

def filtro(dados,colunas):
    #1.3.1
    dados = dados.copy()
    dados["Filtro"] = dados["Codigo"].fillna("") + " - " + dados["Cliente"].fillna("")
    selecao = sorted(dados["Filtro"].dropna().unique().tolist())
    estilo_botao(cor_fundo="#ED8232", tamanho_fonte="20px")

    st.markdown("""
        <p style="font-size:22px; color:white; font-weight:bold;">
            Filtrar Projetos:
        </p>
    """, unsafe_allow_html=True)

    selecionados = st.selectbox(
        label="Seleção", 
        options=["Todos"] + selecao,
        label_visibility="collapsed"
        )

    #1.3.2
    if selecionados !="Todos":
        dados_filtrado = dados[dados["Filtro"]==selecionados].copy()
    else:
        dados_filtrado =dados.copy()    

    # 1.3.3
    dados_editado = st.data_editor(
        dados_filtrado[colunas],
        column_config={
            "Codigo": st.column_config.TextColumn(required=True),
            "Cliente": st.column_config.TextColumn(required=True),
            "Deadline": st.column_config.DateColumn("Deadline"),
            "TAP": st.column_config.DateColumn("TAP"),
            "Eng. Produto": st.column_config.DateColumn("Eng. Produto"),
            "Eng. Aplicação": st.column_config.DateColumn("Eng. Aplicação"),
            "Projeto Elétrico": st.column_config.DateColumn("Projeto Elétrico"),
            "Compras": st.column_config.DateColumn("Compras"),
            "Montagem Elétrica": st.column_config.DateColumn("Montagem Elétrica"),
            "Testes E/M": st.column_config.DateColumn("Testes E/M"),
            "Automação": st.column_config.DateColumn("Automação"), 
            "Tryout": st.column_config.DateColumn("Tryout"), 
            "Embalagem": st.column_config.DateColumn("Embalagem"), 
        },
        num_rows="dynamic",
        use_container_width=True
    )
    return dados_editado


#----------------------------------------------------------------------------------------------------------------------

# 1.4>>> Função para salvar os dados no CSV
def salvar(dados, BASE):
    # Salva o DataFrame editado de volta no arquivo CSV
    dados.to_csv(BASE, index=False)

#----------------------------------------------------------------------------------------------------------------------

# 1.5>>> Função para salvar os dados no CSV

def calcular_intervalos(dados,colunas):
    for col in colunas:
        if col in dados.columns:
            dados[col]=pd.to_datetime(dados[col],errors='coerce')

    intervalos = []
    for _, row in dados.iterrows():
        codigo = row.get("Codigo", "")
        cliente = row.get("Cliente", "")
        codigo_cliente = f"{codigo}-{cliente}"

        etapas_dias = {
            "Eng. Produto": (row["Eng. Produto"] - row["TAP"]).days
            if pd.notna(row.get("Eng. Produto")) and pd.notna(row.get("TAP")) else None,

            "Eng. Aplicação": (row["Eng. Aplicação"] - row["Eng. Produto"]).days
            if pd.notna(row.get("Eng. Aplicação")) and pd.notna(row.get("Eng. Produto")) else None,

            "Projeto Elétrico": (row["Projeto Elétrico"] - row["Eng. Aplicação"]).days
            if pd.notna(row.get("Projeto Elétrico")) and pd.notna(row.get("Eng. Aplicação")) else None,

            "Compras": (row["Compras"] - row["Projeto Elétrico"]).days
            if pd.notna(row.get("Compras")) and pd.notna(row.get("Projeto Elétrico")) else None,

            "Montagem Elétrica": (row["Montagem Elétrica"] - row["Compras"]).days
            if pd.notna(row.get("Montagem Elétrica")) and pd.notna(row.get("Compras")) else None,

            "Testes E/M": (row["Testes E/M"] - row["Montagem Elétrica"]).days
            if pd.notna(row.get("Testes E/M")) and pd.notna(row.get("Montagem Elétrica")) else None,
            
            "Automação": (row["Automação"] - row["Testes E/M"]).days
            if pd.notna(row.get("Automação")) and pd.notna(row.get("Testes E/M")) else None,

            "Tryout": (row["Tryout"] - row["Automação"]).days
            if pd.notna(row.get("Tryout")) and pd.notna(row.get("Automação")) else None,

            "Embalagem": (row["Embalagem"] - row["Tryout"]).days
            if pd.notna(row.get("Embalagem")) and pd.notna(row.get("Tryout")) else None,


        }

        for etapa, dias in etapas_dias.items():
            if dias is not None:
                intervalos.append({
                    "Codigo": codigo,
                    "Cliente": cliente,
                    "Cliente_Projeto": codigo_cliente,
                    "Etapa": etapa,
                    "Dias": dias,
                    "Início": row[etapa] - pd.Timedelta(days=dias),
                    "Fim": row[etapa],
                })
    return pd.DataFrame(intervalos)

#----------------------------------------------------------------------------------------------------------------------


def cronograma():
    try:
        # Carrega os dados
        banco = carregar()

        # Calcula os intervalos entre etapas de cada projeto
        df_intervalos = calcular_intervalos(banco, ["TAP","Eng. Produto", "Eng. Aplicação", "Projeto Elétrico"])
        df_intervalos["Codigo_Cliente"]=df_intervalos["Codigo"] + "_"+ df_intervalos["Cliente"]

        #estilo_botao()

# Lista única de opções
        todos_clientes = df_intervalos["Codigo_Cliente"].unique()

        # Checkbox para selecionar todos
        selecionar_todos = st.checkbox("Selecionar todos os projetos", value=True)
        
        st.markdown("""
            <p style="font-size:22px; color:white; font-weight:bold;">
                Selecionar Clientes:
            </p>
        """, unsafe_allow_html=True)

        clientes = st.multiselect(
            label= "Seleção",
            options= todos_clientes, default=todos_clientes if selecionar_todos else [],
            label_visibility = "collapsed"

        )

        df_filtrado = df_intervalos[df_intervalos["Codigo_Cliente"].isin(clientes)].copy()
        df_filtrado["Rótulo"] = df_filtrado["Etapa"] + " - " + df_filtrado["Dias"].astype(str) + " dias"

        fig = px.timeline(
            df_filtrado,
            x_start="Início",
            x_end="Fim",
            y="Cliente_Projeto",
            color="Etapa",
            labels={"Cliente_Projeto": "Cliente / Projeto"},
            text= "Rótulo",
        )

        fig.update_yaxes(autorange="reversed")
        fig.update_traces(textposition="auto")
        st.plotly_chart(fig, use_container_width=True)

    except Exception as e:
        st.error(f"Erro ao carregar a aba Cronograma: {e}")