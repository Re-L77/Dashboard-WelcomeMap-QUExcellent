import os
import pyodbc
import pymssql
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# Obtener variables de entorno para la conexión
DB_SERVER = os.getenv("DB_SERVER", "db")
DB_NAME = os.getenv("DB_NAME", "EmpresaDB")
DB_USER = os.getenv("DB_USER", "sa")
DB_PASSWORD = os.getenv("DB_PASSWORD", "YourStrongPassword123!")
DB_PORT = os.getenv("DB_PORT", 1433)

# Cadena de conexión para SQL Server (pyodbc)
CONNECTION_STRING = f"DRIVER={{ODBC Driver 18 for SQL Server}};SERVER={DB_SERVER};DATABASE={DB_NAME};UID={DB_USER};PWD={DB_PASSWORD};TrustServerCertificate=yes;"

# Crear el motor de SQLAlchemy
engine = create_engine(f"mssql+pyodbc:///?odbc_connect={CONNECTION_STRING}")

# Crear una sesión
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para los modelos
Base = declarative_base()

# Función para obtener una sesión de base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Función para obtener una conexión pymssql
def get_db_connection():
    """Retorna una conexión pymssql a la base de datos SQL Server"""
    conn = pymssql.connect(
        server=DB_SERVER,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        port=int(DB_PORT)
    )
    return conn

# Función para probar la conexión
def test_connection():
    try:
        conn = pyodbc.connect(CONNECTION_STRING)
        cursor = conn.cursor()
        cursor.execute("SELECT @@VERSION")
        row = cursor.fetchone()
        print(f"Conexión exitosa a SQL Server: {row[0]}")
        conn.close()
        return True
    except Exception as e:
        print(f"Error al conectar a SQL Server: {e}")
        return False