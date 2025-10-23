#!/usr/bin/env python3
"""Script para consultar datos de la BD"""
import pymssql

conn = pymssql.connect(
    server="db",
    user="sa",
    password="YourStrongPassword123!",
    database="EmpresaDB",
    timeout=10
)
cursor = conn.cursor()

print("\n" + "="*80)
print("📊 DATOS DE EMPLEADOS (Primeros 15)")
print("="*80)
cursor.execute("SELECT TOP 15 id_empleado, nombre, email, edad, genero, tipo_contrato, nivel_seniority FROM Empleado ORDER BY id_empleado")
for row in cursor.fetchall():
    print(f"ID: {row[0]:2d} | Nombre: {row[1]:15s} | Email: {row[2]:25s} | Edad: {row[3]:2d} | Género: {row[4]} | Contrato: {row[5]:10s} | Seniority: {row[6]}")

print("\n" + "="*80)
print("📊 ESTADÍSTICAS GENERALES")
print("="*80)

# Contar empleados
cursor.execute("SELECT COUNT(*) FROM Empleado")
emp_count = cursor.fetchone()[0]
print(f"✅ Total de empleados: {emp_count}")

# Contar equipos
cursor.execute("SELECT COUNT(*) FROM Equipo")
eq_count = cursor.fetchone()[0]
print(f"✅ Total de equipos: {eq_count}")

# Contar procesos de reclutamiento
cursor.execute("SELECT COUNT(*) FROM Proceso_Reclutamiento")
proc_count = cursor.fetchone()[0]
print(f"✅ Total de procesos de reclutamiento: {proc_count}")

# Contar feedback
cursor.execute("SELECT COUNT(*) FROM Feedback")
feed_count = cursor.fetchone()[0]
print(f"✅ Total de feedback: {feed_count}")

# Contar tareas
cursor.execute("SELECT COUNT(*) FROM Tarea")
task_count = cursor.fetchone()[0]
print(f"✅ Total de tareas: {task_count}")

print("\n" + "="*80)
print("📊 DATOS DE EJEMPLO (Proceso de Reclutamiento)")
print("="*80)
cursor.execute("""
    SELECT TOP 5 
        pr.id_reclutamiento, 
        e.nombre,
        pr.tiempo_proceso_reclutamiento_dias,
        pr.num_entrevistas,
        pr.calificacion_entrevista,
        pr.oferta_inicial_aceptada
    FROM Proceso_Reclutamiento pr
    JOIN Empleado e ON pr.id_empleado = e.id_empleado
    ORDER BY pr.id_reclutamiento
""")
print(f"{'ID':<4} {'Empleado':<20} {'Días Proceso':<15} {'Entrevistas':<12} {'Calificación':<14} {'Oferta Aceptada':<16}")
print("-" * 80)
for row in cursor.fetchall():
    print(f"{row[0]:<4} {row[1]:<20} {row[2]:<15} {row[3]:<12} {row[4]:<14.2f} {row[5]:<16}")

print("\n" + "="*80)
print("📊 DATOS DE EJEMPLO (Proceso de Integración)")
print("="*80)
cursor.execute("""
    SELECT TOP 5 
        pi.id_integracion,
        e.nombre,
        pi.dias_hasta_primer_proyecto,
        pi.asignacion_mentor,
        pi.satisfaccion_lider,
        pi.compatibilidad_equipo
    FROM Proceso_Integracion pi
    JOIN Empleado e ON pi.id_empleado = e.id_empleado
    ORDER BY pi.id_integracion
""")
print(f"{'ID':<4} {'Empleado':<20} {'Días Proyecto':<16} {'Mentor':<8} {'Satisfacción':<14} {'Compatibilidad':<16}")
print("-" * 80)
for row in cursor.fetchall():
    print(f"{row[0]:<4} {row[1]:<20} {row[2]:<16} {row[3]:<8} {row[4]:<14.2f} {row[5]:<16.2f}")

cursor.close()
conn.close()
print("\n✅ Consulta completada\n")
