from fastapi import APIRouter, Depends, HTTPException
from app.models.db_connection import get_db_connection
import logging
import os

router = APIRouter(prefix="/api/integration", tags=["Integration"])
logger = logging.getLogger("integration_controller")

@router.get("/employees")
def get_employees():
    """Obtiene todos los empleados y su estado de integración"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        query = """
            SELECT TOP 100
                e.id_empleado,
                e.nombre,
                e.email,
                ISNULL(d.nombre, 'N/A') as departamento,
                e.fecha_contratacion,
                pi.dias_hasta_primer_proyecto,
                pi.asignacion_mentor,
                pi.satisfaccion_lider,
                pi.compatibilidad_equipo,
                CASE 
                    WHEN pi.satisfaccion_lider >= 4.5 AND pi.compatibilidad_equipo >= 4 THEN 'Excelente'
                    WHEN pi.satisfaccion_lider >= 4 AND pi.compatibilidad_equipo >= 3.5 THEN 'Muy Bueno'
                    WHEN pi.satisfaccion_lider >= 3 AND pi.compatibilidad_equipo >= 3 THEN 'Bueno'
                    ELSE 'En Progreso'
                END as estado_integracion,
                CAST(
                    (ISNULL(pi.satisfaccion_lider, 0) + ISNULL(pi.compatibilidad_equipo, 0)) / 2.0 * 100 / 5.0 
                    AS INT
                ) as porcentaje_integracion
            FROM Empleado e
            LEFT JOIN Departamento d ON e.id_departamento = d.id_departamento
            LEFT JOIN Proceso_Integracion pi ON e.id_empleado = pi.id_empleado
            ORDER BY e.id_empleado
        """
        
        cursor.execute(query)
        employees = []
        for row in cursor.fetchall():
            employees.append({
                "id": row[0],
                "nombre": row[1],
                "email": row[2],
                "departamento": row[3],
                "fecha_contratacion": row[4].isoformat() if row[4] else None,
                "dias_hasta_proyecto": row[5],
                "mentor_asignado": bool(row[6]),
                "satisfaccion_lider": row[7],
                "compatibilidad_equipo": row[8],
                "estado": row[9],
                "porcentaje": row[10]
            })
        
        cursor.close()
        conn.close()
        
        return {
            "total": len(employees),
            "usuarios": employees
        }
    except Exception as e:
        logger.error(f"Error fetching employees: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/employees/{employee_id}")
def get_employee_details(employee_id: int):
    """Obtiene detalles completos de un empleado"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Datos del empleado
        query = """
            SELECT TOP 1
                e.id_empleado, e.nombre, e.email, e.edad, e.genero,
                e.departamento, e.fecha_contratacion, e.tipo_contrato, e.nivel_seniority
            FROM Empleado e
            WHERE e.id_empleado = %d
        """ % employee_id
        
        cursor.execute(query)
        emp_row = cursor.fetchone()
        
        if not emp_row:
            raise HTTPException(status_code=404, detail="Empleado no encontrado")
        
        # Proceso de reclutamiento
        cursor.execute(f"""
            SELECT TOP 1
                tiempo_proceso_reclutamiento_dias, num_entrevistas, calificacion_entrevista, oferta_inicial_aceptada
            FROM Proceso_Reclutamiento
            WHERE id_empleado = {employee_id}
        """)
        reclutamiento = cursor.fetchone()
        
        # Proceso de integración
        cursor.execute(f"""
            SELECT TOP 1
                dias_hasta_primer_proyecto, asignacion_mentor, satisfaccion_lider, 
                compatibilidad_equipo, calificacion_entrevista, puntuacion_induccion
            FROM Proceso_Integracion
            WHERE id_empleado = {employee_id}
        """)
        integracion = cursor.fetchone()
        
        # Métricas de capacitación
        cursor.execute(f"""
            SELECT TOP 1
                horas_capacitacion, cursos_completados, evaluacion_tecnica, conocimiento_herramientas
            FROM Metricas_Capacitacion
            WHERE id_empleado = {employee_id}
        """)
        capacitacion = cursor.fetchone()
        
        cursor.close()
        conn.close()
        
        return {
            "empleado": {
                "id": emp_row[0],
                "nombre": emp_row[1],
                "email": emp_row[2],
                "edad": emp_row[3],
                "genero": emp_row[4],
                "departamento": emp_row[5],
                "fecha_contratacion": emp_row[6].isoformat() if emp_row[6] else None,
                "tipo_contrato": emp_row[7],
                "nivel_seniority": emp_row[8]
            },
            "reclutamiento": {
                "dias_proceso": reclutamiento[0] if reclutamiento else None,
                "num_entrevistas": reclutamiento[1] if reclutamiento else None,
                "calificacion_entrevista": reclutamiento[2] if reclutamiento else None,
                "oferta_aceptada": bool(reclutamiento[3]) if reclutamiento else None
            } if reclutamiento else None,
            "integracion": {
                "dias_primer_proyecto": integracion[0] if integracion else None,
                "mentor_asignado": bool(integracion[1]) if integracion else None,
                "satisfaccion_lider": integracion[2] if integracion else None,
                "compatibilidad_equipo": integracion[3] if integracion else None,
                "calificacion": integracion[4] if integracion else None,
                "puntuacion_induccion": integracion[5] if integracion else None
            } if integracion else None,
            "capacitacion": {
                "horas_total": capacitacion[0] if capacitacion else None,
                "cursos_completados": capacitacion[1] if capacitacion else None,
                "evaluacion_tecnica": capacitacion[2] if capacitacion else None,
                "conocimiento_herramientas": capacitacion[3] if capacitacion else None
            } if capacitacion else None
        }
    except Exception as e:
        logger.error(f"Error fetching employee details: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/departments")
def get_departments():
    """Obtiene lista de departamentos"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT DISTINCT nombre FROM Departamento WHERE nombre IS NOT NULL ORDER BY nombre")
        departments = [row[0] for row in cursor.fetchall()]
        
        cursor.close()
        conn.close()
        
        return {"departamentos": departments}
    except Exception as e:
        logger.error(f"Error fetching departments: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/statistics")
def get_integration_statistics():
    """Obtiene estadísticas de integración"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Total de empleados
        cursor.execute("SELECT COUNT(*) FROM Empleado")
        total_empleados = cursor.fetchone()[0]
        
        # Empleados integrados (satisfacción_lider >= 4 y compatibilidad >= 3.5)
        cursor.execute("""
            SELECT COUNT(*) FROM Proceso_Integracion 
            WHERE satisfaccion_lider >= 4 AND compatibilidad_equipo >= 3.5
        """)
        empleados_integrados = cursor.fetchone()[0]
        
        # Promedio de satisfacción
        cursor.execute("SELECT AVG(CAST(satisfaccion_lider AS FLOAT)) FROM Proceso_Integracion")
        promedio_satisfaccion = cursor.fetchone()[0] or 0
        
        # Promedio de compatibilidad
        cursor.execute("SELECT AVG(CAST(compatibilidad_equipo AS FLOAT)) FROM Proceso_Integracion")
        promedio_compatibilidad = cursor.fetchone()[0] or 0
        
        cursor.close()
        conn.close()
        
        porcentaje_integracion = (empleados_integrados / total_empleados * 100) if total_empleados > 0 else 0
        
        return {
            "total_empleados": total_empleados,
            "empleados_integrados": empleados_integrados,
            "porcentaje_integracion": round(porcentaje_integracion, 2),
            "promedio_satisfaccion_lider": round(promedio_satisfaccion, 2),
            "promedio_compatibilidad_equipo": round(promedio_compatibilidad, 2)
        }
    except Exception as e:
        logger.error(f"Error fetching statistics: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
