import os
import requests
import datetime
from sqlalchemy import create_engine, inspect
from dotenv import load_dotenv
import pandas as pd
from time import sleep

load_dotenv()

def extract_bitcoin_value(url):

    response = requests.get(url=url).json()

    # response = response.json()
    return response

def transform_bitcoin_values(btc_json):

    nome_ativo = btc_json["pair"]
    cotacao_ativo = btc_json["last"]
    data_hora_cotacao = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    dado_bitcoin = {
        "nome_ativo": nome_ativo,
        "cotacao_ativo": cotacao_ativo,
        "data_hora_cotacao": data_hora_cotacao,
    }

    return dado_bitcoin

def create_connection(user_name, user_password, host_name, number_port, db_name):
    """
    Cria a conexão com o banco de dados PostgreSQL
    """
    conexao_postgres = None
    try:
        conexao_postgres = create_engine(
            f"postgresql://{user_name}:{user_password}@{host_name}:{number_port}/{db_name}"
        )
        with conexao_postgres.connect():
            print("Postgres conectado com sucesso", "\n")
    except Exception as e:
        print(f"Deu ruim {e}")

    return conexao_postgres

def load_bitcoin_extraction(dados_btc, conexao):
    df_bitcoin = pd.DataFrame(data=[dados_btc])

    valida_tabela = inspect(conexao)

    if valida_tabela.has_table(os.getenv("my_table")):
        print(f"Inserindo dados na Tabela {os.getenv('my_table')}!")
        df_bitcoin.to_sql(
            name=os.getenv("my_table"), con=conexao, if_exists="append", index=False
        )
    else:
        print("tabela não existente, favor verificar")


if __name__ == "__main__":
    url_btc = "https://cointradermonitor.com/api/pbb/v1/ticker"
    btc_extract = extract_bitcoin_value(url=url_btc)
    btc_transform = transform_bitcoin_values(btc_json=btc_extract)
    
    # print(url_btc)

    conn = create_connection(
        user_name=os.getenv("my_user"),
        user_password=os.getenv("my_password"),
        host_name="localhost",
        number_port="5440",
        db_name=os.getenv("my_database"),
    )

    # load_bitcoin_extraction(dados_btc=btc_transform, conexao=conn)
    while True:
        sleep(30)
        load_bitcoin_extraction(dados_btc=btc_transform, conexao=conn)