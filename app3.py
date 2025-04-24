import streamlit as st
import pandas as pd
import plotly.express as px
import os

# Caminho do arquivo CSV
csv_path = "Banco.csv"

# Função para carregar os dados do CSV ou criar DataFrame vazio
def load_data():
    if os.path.exists(csv_path):
        return pd.read_csv(csv_path, sep=";")
    else:
        return pd.DataFrame(columns=["Projeto", "Atividade", "Inicio", "Fim", "Total Dias"])

# Função para salvar os dados editados no CSV
def save_data(df):
    df.to_csv(csv_path, sep=";", index=False)

# Título da página
st.title("Gestão de Projetos - Dashboard Interativo")

# Carrega os dados
df = load_data()

# Converter colunas de data e calcular total de dias
try:
    df["Inicio"] = pd.to_datetime(df["Inicio"], dayfirst=True, errors="coerce")
    df["Fim"] = pd.to_datetime(df["Fim"], dayfirst=True, errors="coerce")
    df["Total Dias"] = (df["Fim"] - df["Inicio"]).dt.days
except Exception as e:
    st.error(f"Erro ao converter datas: {e}")

# Editor interativo de dados
st.subheader("📋 Edição dos Dados")
edited_df = st.data_editor(df, num_rows="dynamic", use_container_width=True)

# Botão para salvar alterações
if st.button("Salvar Alterações"):
    df_to_save = edited_df.copy()
    df_to_save["Inicio"] = pd.to_datetime(df_to_save["Inicio"], errors="coerce").dt.strftime("%d/%m/%Y")
    df_to_save["Fim"] = pd.to_datetime(df_to_save["Fim"], errors="coerce").dt.strftime("%d/%m/%Y")
    save_data(df_to_save)
    st.success("Dados salvos com sucesso!")

# Gráfico empilhado por atividade
st.subheader("📊 Gráfico de Coluna Empilhada")
if not edited_df.empty:
    try:
        edited_df["Total Dias"] = pd.to_numeric(edited_df["Total Dias"], errors="coerce")
        fig = px.bar(edited_df, x="Projeto", y="Total Dias", color="Atividade", title="Distribuição de Atividades por Projeto")
        st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        st.error(f"Erro ao gerar gráfico: {e}")
else:
    st.warning("Nenhum dado disponível.")

