import psycopg2
import os
from dotenv import load_dotenv
import pandas as pd
import streamlit as st


load_dotenv()

conexao = psycopg2.connect(
    host="localhost",
    database=os.getenv("my_database"),
    port="5440", 
    user=os.getenv("my_user"),
    password=os.getenv("my_password")
)


def buscar_dados():
    """Lê os dados do banco PostgreSQL e retorna como DataFrame."""
    try:
        tabela_curso = pd.read_sql_query("select * from tb_cotacao", conexao)
        return tabela_curso
    except Exception as e:
        st.error(f"Erro ao conectar no PostgreSQL: {e}")
        return pd.DataFrame()
    
def dash():
    st.set_page_config(page_title="Dashboard de Preços do Bitcoin", layout="wide")
    st.title("📊 Dashboard de Preços do Bitcoin")
    st.write("Este dashboard exibe os dados do preço do Bitcoin coletados periodicamente em um banco PostgreSQL.")

    df = buscar_dados()

    if not df.empty:
        st.subheader("🔢 Estatísticas Gerais")
        col1, col2, col3 = st.columns(3)
        col1.metric("Preço Atual", f"${df['cotacao_ativo'].iloc[-1]:,.2f}")
        col2.metric("Preço Máximo", f"${df['cotacao_ativo'].max():,.2f}")
        col3.metric("Preço Mínimo", f"${df['cotacao_ativo'].min():,.2f}")

        st.subheader("📋 Dados Recentes")
        st.dataframe(df)

        df['data_hora_cotacao'] = pd.to_datetime(df['data_hora_cotacao'])
        df = df.sort_values(by='data_hora_cotacao')

    else:
        st.warning("Nenhum dado encontrado no banco de dados PostgreSQL.")


if __name__ == "__main__":
    dash()
