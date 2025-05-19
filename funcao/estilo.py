import streamlit as st

#----------------------------------------------------------------------------------------------------------------------

# 1.0>>> Função para editar o botão filtro (cores de fundo , fonte e tamanho)
def estilo_botao(cor_fundo="#ED8232", tamanho_fonte="20px", borda="10px", largura="285px",altura="50px", topo = "0px"):
    st.markdown(f"""
        <style>
            /* Estilo da área do botão */
            div[data-baseweb="select"] > div {{
                background-color: {cor_fundo};
                font-size: {tamanho_fonte};
                padding: 4px 4px;
                border-radius: {borda};
                width: {largura};
                height: {altura};
                max-width: 100%;
                display: flex;
                margin-top: {topo};
                border: 1px solid #ccc;
            }}

            /* Estilo dos itens selecionados (tags) */
            div[data-baseweb="select"] span {{
                background-color: transparent !important;
                color: white !important; /* Altere para a cor que desejar no texto */
                font-weight: 100;
            }}
        </style>
    """, unsafe_allow_html=True)

# div[data-baseweb="select"] →  é o seletor usado pelo componente selectbox no HTML gerado pelo Streamlit.
# background-color: #f0f2f6 → muda o fundo do botão.
# font-size: 14px → ajusta a fonte.
# padding e border-radius → ajustes estéticos de tamanho e arredondamento.

#----------------------------------------------------------------------------------------------------------------------

# 2.0>>> Função para editar o botão filtro das abas

def abas():
    st.markdown(
        """
        <style>
        /* Tamanho e estilo do texto das abas */
        .stTabs [data-baseweb="tab"] {
            font-size: 100px !important;
            font-weight: bold;
            padding: 12px 100px;
            color: #FFFFFF;
        }

        /* Aumenta a fonte do texto real das abas */
        .stTabs [data-baseweb="tab"] > div > div {
            font-size: 50px !important;
        }

        /* Aba ativa */
        .stTabs [aria-selected="true"] {
            background-color: #2A6AAE !important;
            color: #FFFFFF !important;
            border-radius: 12px 12px 0 0;
        }

        /* Aba inativa */
        .stTabs [aria-selected="false"] {
            background-color: #595959 !important;
            color: #FFFFFF !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
