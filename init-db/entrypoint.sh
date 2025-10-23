#!/bin/bash
set -e

echo "Esperando a que SQL Server esté listo..."
sleep 30

echo "Ejecutando script de inicialización..."
/opt/mssql-tools/bin/sqlcmd -S localhost -U sa -P "${SA_PASSWORD}" -i /docker-entrypoint-initdb.d/init.sql

echo "✅ Base de datos inicializada correctamente"
