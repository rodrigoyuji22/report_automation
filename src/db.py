import pyodbc
import pandas as pd
from config import DB_DATABASE, DB_PWD, DB_SERVER, DB_UID

def get_connection() -> pyodbc.Connection:
    connectionString = (
        "DRIVER={ODBC Driver 18 for SQL Server};"
        f"SERVER={DB_SERVER};"
        f"DATABASE={DB_DATABASE};"
        f"UID={DB_UID};"
        f"PWD={DB_PWD};"
        "Encrypt=no;"
        "TrustServerCertificate=yes;"
    ) 
    return pyodbc.connect(connectionString)
# metodo para conectar ao db, vou armazenar em uma instancia essa conexao para poder realizar as queries

def run_query (query: str) -> pd.DataFrame:
    with get_connection() as conn:
        return pd.read_sql(query, conn)
# metodo para abrir a conexao, executar a query e depois fechar a conexao (com with executa o bloco e depois fecha a conexao)





