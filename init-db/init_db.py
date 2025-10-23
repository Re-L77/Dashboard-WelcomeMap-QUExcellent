#!/usr/bin/env python3
"""Script para inicializar la BD ejecutando init.sql"""
import time
import sys
import re

try:
    import pymssql
except ImportError:
    print("❌ pymssql no está instalado, intentando instalar...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-q", "pymssql"])
    import pymssql

def execute_sql_file(host, user, password, file_path, max_retries=10):
    """Ejecuta un archivo SQL contra SQL Server"""
    
    for attempt in range(max_retries):
        try:
            print(f"🔄 Intento {attempt + 1}/{max_retries}...")
            
            # Conexión - con autocommit ON para permitir CREATE DATABASE
            conn = pymssql.connect(
                server=host,
                user=user,
                password=password,
                timeout=10,
                as_dict=False
            )
            conn.autocommit(True)  # Autocommit para CREATE DATABASE
            
            print(f"✅ Conectado a SQL Server en {host}")
            
            # Leer el archivo SQL
            with open(file_path, 'r', encoding='utf-8') as f:
                sql_content = f.read()
            
            # Reemplazar comentarios
            sql_content = re.sub(r'--.*$', '', sql_content, flags=re.MULTILINE)
            sql_content = re.sub(r'/\*.*?\*/', '', sql_content, flags=re.DOTALL)
            
            # Dividir por GO
            batches = re.split(r'\nGO\s*\n', sql_content, flags=re.IGNORECASE)
            
            successful_batches = 0
            for i, batch in enumerate(batches):
                batch = batch.strip()
                if not batch:
                    continue
                    
                try:
                    cursor = conn.cursor()
                    print(f"⏳ Batch {i+1}/{len(batches)}...", end="", flush=True)
                    cursor.execute(batch)
                    cursor.close()
                    print(" ✅")
                    successful_batches += 1
                except Exception as e:
                    error_msg = str(e)
                    if "already exists" in error_msg:
                        print(f" ⚠️  (ya existe)")
                        successful_batches += 1
                        continue
                    else:
                        print(f" ❌")
                        raise
            
            conn.close()
            
            if successful_batches > 0:
                print(f"✅ Base de datos inicializada correctamente ({successful_batches} batches ejecutados)")
                return True
            
        except Exception as e:
            print(f"❌ Error: {str(e)[:80]}")
            if attempt < max_retries - 1:
                print(f"⏳ Esperando 3 segundos...")
                time.sleep(3)
            else:
                print("❌ Máximo número de intentos alcanzado")
                return False
    
    return False

if __name__ == "__main__":
    success = execute_sql_file(
        host="db",
        user="sa",
        password="YourStrongPassword123!",
        file_path="/init.sql"
    )
    sys.exit(0 if success else 1)
