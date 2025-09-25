import pyodbc
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()
serverName = os.getenv("DB_SERVER")
database = os.getenv("DB_DATABASE")
uid = os.getenv("DB_UID")
pwd = os.getenv("DB_PWD")

def get_connection() -> pyodbc.Connection:
    connectionString = (
        "DRIVER={ODBC Driver 17 for SQL Server};"
        f"SERVER={serverName};"
        f"DATABASE={database};"
        f"UID={uid};"
        f"PWD={pwd};"
        "Encrypt=no;"
        "TrustServerCertificate=yes;"
    ) 
    return pyodbc.connect(connectionString)
# metodo para conectar ao db, vou armazenar em uma instancia essa conexao para poder realizar as queries

def run_query (query: str) -> pd.DataFrame:
    with get_connection() as conn:
        return pd.read_sql(query, conn)
# metodo para abrir a conexao, executar a query e depois fechar a conexao (com with executa o bloco e depois fecha a conexao)





