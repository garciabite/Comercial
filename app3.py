# app.py
import streamlit as st
import pandas as pd
import plotly.express as px
import os

csv_path = "Banco.csv"

def load_data():
    if os.path.exists(csv_path):
        return pd.read_csv(csv_path, sep=";")
    else:
        return pd.DataFrame(columns=["Projeto", "Atividade", "Inicio", "Fim", "Total Dias"])

def save_data(df):
    df.to_csv(csv_path, sep=";", index=False)

st.title("Gestão de Projetos - Dashboard Interativo")

df = load_data()

# Converter datas e recalcular "Total Dias"
try:
    df["Inicio"] = pd.to_datetime(df["Inicio"], dayfirst=True, errors="coerce")
    df["Fim"] = pd.to_datetime(df["Fim"], dayfirst=True, errors="coerce")
    df["Total Dias"] = (df["Fim"] - df["Inicio"]).dt.days
except Exception as e:
    st.error(f"Erro ao converter datas: {e}")

st.subheader("📋 Edição dos Dados")
edited_df = st.data_editor(df, num_rows="dynamic", use_container_width=True)

# Botão para salvar alterações
if st.button("Salvar Alterações"):
    save_data(edited_df)
    st.success("Dados salvos com sucesso!")

# Deletar linha por índice
if not edited_df.empty:
    index_to_delete = st.number_input("Índice da linha para deletar:", min_value=0, max_value=len(edited_df)-1, step=1)
    if st.button("Deletar linha"):
        edited_df = edited_df.drop(index=index_to_delete).reset_index(drop=True)
        save_data(edited_df)
        st.success("Linha deletada e dados atualizados.")

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