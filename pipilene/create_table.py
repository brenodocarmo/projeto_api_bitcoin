import os

from sqlalchemy import create_engine, Column, Integer, String, Numeric, DateTime
from sqlalchemy.orm import declarative_base
from dotenv import load_dotenv

load_dotenv()
Base = declarative_base()


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




class Bitcoin(Base):
    __tablename__=os.getenv("my_table")

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome_ativo = Column(String)
    cotacao_ativo = Column(Numeric(10, 2))
    data_hora_cotacao = Column(DateTime)

    def __repr__(self):
        return f"Bitcoin(name='{self.nome_ativo}', cotacao_ativo='{self.cotacao_ativo}', data_hora_cotacao='{self.data_hora_cotacao}')"




conn = create_connection(
    user_name=os.getenv("my_user"),
    user_password=os.getenv("my_password"),
    host_name="localhost",
    number_port="5440",
    db_name=os.getenv("my_database")
)

Base.metadata.create_all(conn)
