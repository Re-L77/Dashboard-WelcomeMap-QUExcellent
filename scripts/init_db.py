"""Utility to check SQL Server databases and run init-db/init.sql if needed.

Usage:
  python scripts/init_db.py           # lists DBs and creates EmpresaDB if missing
  python scripts/init_db.py --dry-run # just lists DBs, doesn't run the SQL

It reads DB credentials from environment variables (DB_SERVER, DB_USER, DB_PASSWORD)
or from the project `.env` (python-dotenv is used).
"""
import os
import sys
import pathlib
import pyodbc
from dotenv import load_dotenv

ROOT = pathlib.Path(__file__).resolve().parents[1]
DOTENV = ROOT / ".env"
if DOTENV.exists():
    load_dotenv(DOTENV)

DB_SERVER = os.getenv("DB_SERVER", "localhost")
DB_NAME = os.getenv("DB_NAME", "EmpresaDB")
DB_USER = os.getenv("DB_USER", "sa")
DB_PASSWORD = os.getenv("DB_PASSWORD", "YourStrongPassword123!")
DB_PORT = os.getenv("DB_PORT", "1433")
DRIVER = os.getenv("ODBC_DRIVER", "ODBC Driver 18 for SQL Server")

INIT_SQL = ROOT / "init-db" / "init.sql"

CONN_STR = (
    f"DRIVER={{{DRIVER}}};"
    f"SERVER={DB_SERVER},{DB_PORT};"
    f"UID={DB_USER};PWD={DB_PASSWORD};"
    f"TrustServerCertificate=yes;"
)


def list_databases(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sys.databases")
    rows = [r[0] for r in cursor]
    cursor.close()
    return rows


def split_sql_batches(sql_text: str):
    batches = []
    current = []
    for ln in sql_text.splitlines():
        if ln.strip().upper() == "GO":
            if current:
                batches.append("\n".join(current))
                current = []
        else:
            current.append(ln)
    if current:
        batches.append("\n".join(current))
    return batches


def run_init_sql(conn):
    if not INIT_SQL.exists():
        print(f"init.sql not found at {INIT_SQL}")
        return False
    sql_text = INIT_SQL.read_text(encoding="utf-8")
    batches = split_sql_batches(sql_text)
    # Some commands (like CREATE DATABASE) must run with autocommit (outside a multi-statement transaction).
    prev_autocommit = getattr(conn, 'autocommit', False)
    try:
        try:
            conn.autocommit = True
        except Exception:
            # some pyodbc builds may not allow setting autocommit; ignore and proceed
            pass

        cursor = conn.cursor()
        for i, batch in enumerate(batches, start=1):
            print(f"Executing batch {i}/{len(batches)}...")
            try:
                cursor.execute(batch)
            except Exception as e:
                print(f"Error executing batch {i}: {e}")
                cursor.close()
                return False
        cursor.close()
    finally:
        try:
            conn.autocommit = prev_autocommit
        except Exception:
            pass
    return True


def main(dry_run: bool = False):
    print("Connecting to SQL Server using:")
    print(f"  server: {DB_SERVER}:{DB_PORT}")
    print(f"  user: {DB_USER}")
    print(f"  database target: {DB_NAME}")
    try:
        conn = pyodbc.connect(CONN_STR, timeout=10)
    except Exception as e:
        print(f"Failed to connect to SQL Server: {e}")
        return 2

    try:
        dbs = list_databases(conn)
    except Exception as e:
        print(f"Failed to list databases: {e}")
        conn.close()
        return 3

    print("Databases on server:")
    for d in dbs:
        print(" -", d)

    if DB_NAME in dbs:
        print(f"Database '{DB_NAME}' already exists. Nothing to do.")
        conn.close()
        return 0

    if dry_run:
        print(f"Dry run - not creating '{DB_NAME}'.")
        conn.close()
        return 0

    print(f"Database '{DB_NAME}' not found. Running init script: {INIT_SQL}")
    ok = run_init_sql(conn)
    conn.close()
    if ok:
        print("Initialization completed successfully.")
        return 0
    else:
        print("Initialization failed. See errors above.")
        return 4


if __name__ == "__main__":
    dry = False
    if len(sys.argv) > 1 and sys.argv[1] in ("--dry-run", "-n"):
        dry = True
    sys.exit(main(dry))
