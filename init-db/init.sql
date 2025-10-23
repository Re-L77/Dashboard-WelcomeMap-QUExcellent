-- Crear base de datos 
CREATE DATABASE EmpresaDB;

GO
    USE EmpresaDB;

GO
    -- ==================================== 
    -- TABLA DE DEPARTAMENTOS 
    -- ==================================== 
    CREATE TABLE Departamento (
        id_departamento INT IDENTITY(1, 1) PRIMARY KEY,
        nombre NVARCHAR(100) NOT NULL
    );

-- ==================================== 
-- TABLA DE PUESTOS 
-- ==================================== 
CREATE TABLE Puesto (
    id_puesto INT IDENTITY(1, 1) PRIMARY KEY,
    nombre NVARCHAR(100) NOT NULL
);

-- ==================================== 
-- TABLA DE LOCACIONES 
-- ==================================== 
CREATE TABLE Locacion (
    id_locacion INT IDENTITY(1, 1) PRIMARY KEY,
    nombre NVARCHAR(100) NOT NULL
);

-- ==================================== 
-- TABLA DE EMPLEADOS 
-- ==================================== 
CREATE TABLE Empleado (
    id_empleado INT IDENTITY(1, 1) PRIMARY KEY,
    nombre NVARCHAR(100) NOT NULL,
    email NVARCHAR(150) NOT NULL UNIQUE,
    status NVARCHAR(50),
    fecha_contratacion DATE,
    id_puesto INT FOREIGN KEY REFERENCES Puesto(id_puesto),
    id_departamento INT FOREIGN KEY REFERENCES Departamento(id_departamento),
    id_locacion INT FOREIGN KEY REFERENCES Locacion(id_locacion),
    -- Campos adicionales para modelo ML
    edad INT,
    genero NVARCHAR(10),
    experiencia_previa INT,
    -- años de experiencia antes de ser contratado
    tipo_contrato NVARCHAR(50),
    -- Indefinido, Temporal, Proyecto, etc.
    nivel_seniority NVARCHAR(50) -- Junior, Semi-Senior, Senior, etc.
);

-- ==================================== python scripts/init_db.py
-- TABLA DE EQUIPOS 
-- ==================================== 
CREATE TABLE Equipo (
    id_equipo INT IDENTITY(1, 1) PRIMARY KEY,
    nombre NVARCHAR(100) NOT NULL,
    fecha_inicio DATE
);

-- Relación muchos a muchos Empleado-Equipo 
CREATE TABLE Empleado_Equipo (
    id_empleado INT FOREIGN KEY REFERENCES Empleado(id_empleado),
    id_equipo INT FOREIGN KEY REFERENCES Equipo(id_equipo),
    PRIMARY KEY (id_empleado, id_equipo)
);

-- ==================================== 
-- TABLA DE ENTRENAMIENTO 
-- ==================================== 
CREATE TABLE Plan_Entrenamiento (
    id_entrenamiento INT IDENTITY(1, 1) PRIMARY KEY,
    tipo NVARCHAR(100),
    estatus NVARCHAR(50),
    fecha_inicio DATE,
    fecha_termino DATE,
    id_departamento INT FOREIGN KEY REFERENCES Departamento(id_departamento)
);

-- Relación muchos a muchos Empleado-Entrenamiento 
CREATE TABLE Empleado_Entrenamiento (
    id_empleado INT FOREIGN KEY REFERENCES Empleado(id_empleado),
    id_entrenamiento INT FOREIGN KEY REFERENCES Plan_Entrenamiento(id_entrenamiento),
    PRIMARY KEY (id_empleado, id_entrenamiento)
);

-- ==================================== 
-- TABLA DE CURSOS 
-- ==================================== 
CREATE TABLE Curso (
    id_curso INT IDENTITY(1, 1) PRIMARY KEY,
    fecha_inicio DATE,
    id_departamento INT FOREIGN KEY REFERENCES Departamento(id_departamento),
    id_entrenamiento INT FOREIGN KEY REFERENCES Plan_Entrenamiento(id_entrenamiento)
);

-- Relación muchos a muchos Empleado-Curso 
CREATE TABLE Empleado_Curso (
    id_empleado INT FOREIGN KEY REFERENCES Empleado(id_empleado),
    id_curso INT FOREIGN KEY REFERENCES Curso(id_curso),
    PRIMARY KEY (id_empleado, id_curso)
);

-- ==================================== 
-- TABLA DE CATEGORIAS 
-- ==================================== 
CREATE TABLE Categoria (
    id_categoria INT IDENTITY(1, 1) PRIMARY KEY,
    nombre NVARCHAR(100) NOT NULL
);

-- ==================================== 
-- TABLA DE FEEDBACK 
-- ==================================== 
CREATE TABLE Feedback (
    id_feedback INT IDENTITY(1, 1) PRIMARY KEY,
    rating INT,
    descripcion NVARCHAR(MAX),
    fecha DATE,
    estatus NVARCHAR(50),
    id_empleado INT FOREIGN KEY REFERENCES Empleado(id_empleado),
    id_categoria INT FOREIGN KEY REFERENCES Categoria(id_categoria)
);

-- ==================================== 
-- TABLA DE TAREAS Y RELACION EQUIPO-TAREA 
-- ==================================== 
CREATE TABLE Tarea (
    id_tarea INT IDENTITY(1, 1) PRIMARY KEY,
    descripcion NVARCHAR(200) NOT NULL
);

CREATE TABLE Equipo_Tarea (
    id_equipo INT FOREIGN KEY REFERENCES Equipo(id_equipo),
    id_tarea INT FOREIGN KEY REFERENCES Tarea(id_tarea),
    PRIMARY KEY (id_equipo, id_tarea)
);

-- Insertar datos de ejemplo en Departamento
INSERT INTO
    Departamento (nombre)
VALUES
    ('Recursos Humanos'),
    ('Tecnología'),
    ('Ventas'),
    ('Marketing'),
    ('Finanzas');

-- Insertar datos de ejemplo en Puesto
INSERT INTO
    Puesto (nombre)
VALUES
    ('Gerente'),
    ('Desarrollador'),
    ('Analista'),
    ('Diseñador'),
    ('Contador');

-- Insertar datos de ejemplo en Locacion
INSERT INTO
    Locacion (nombre)
VALUES
    ('Ciudad de México'),
    ('Guadalajara'),
    ('Monterrey'),
    ('Querétaro'),
    ('Tijuana');

-- ==================================== 
-- TABLAS PARA MODELO ML DE ONBOARDING
-- ==================================== 
-- Proceso de Reclutamiento
CREATE TABLE Proceso_Reclutamiento (
    id_reclutamiento INT IDENTITY(1, 1) PRIMARY KEY,
    id_empleado INT UNIQUE FOREIGN KEY REFERENCES Empleado(id_empleado),
    tiempo_proceso_reclutamiento_dias INT,
    num_entrevistas INT,
    calificacion_entrevista FLOAT,
    -- promedio de calificaciones de entrevistas
    oferta_inicial_aceptada BIT,
    -- 1 si aceptó la primera oferta, 0 si negoció
    fecha_registro DATETIME DEFAULT GETDATE()
);

-- Proceso de Inducción
CREATE TABLE Proceso_Induccion (
    id_induccion INT IDENTITY(1, 1) PRIMARY KEY,
    id_empleado INT UNIQUE FOREIGN KEY REFERENCES Empleado(id_empleado),
    asistencia_curso_induccion BIT,
    puntuacion_induccion FLOAT,
    -- calificación del curso de inducción
    materiales_entregados BIT,
    -- 1 si recibió laptop, accesos, etc.
    sesion_bienvenida BIT,
    -- 1 si asistió a sesión de bienvenida
    fecha_registro DATETIME DEFAULT GETDATE()
);

-- Proceso de Integración
CREATE TABLE Proceso_Integracion (
    id_integracion INT IDENTITY(1, 1) PRIMARY KEY,
    id_empleado INT UNIQUE FOREIGN KEY REFERENCES Empleado(id_empleado),
    dias_hasta_primer_proyecto INT,
    -- días desde contratación hasta primer proyecto
    asignacion_mentor BIT,
    -- 1 si se le asignó mentor
    reunion_equipo_realizadas INT,
    -- número de reuniones con el equipo en primer mes
    actividades_integracion INT,
    -- número de actividades sociales/team building
    satisfaccion_lider FLOAT,
    -- calificación del líder sobre integración del empleado (1-5)
    compatibilidad_equipo FLOAT,
    -- evaluación de compatibilidad con el equipo (1-5)
    fecha_registro DATETIME DEFAULT GETDATE()
);

-- Métricas de Capacitación
CREATE TABLE Metricas_Capacitacion (
    id_metricas_capacitacion INT IDENTITY(1, 1) PRIMARY KEY,
    id_empleado INT UNIQUE FOREIGN KEY REFERENCES Empleado(id_empleado),
    horas_capacitacion INT,
    -- total de horas de capacitación en primer mes
    cursos_completados INT,
    -- número de cursos completados
    evaluacion_tecnica FLOAT,
    -- puntuación de evaluación técnica (0-100)
    plan_entrenamiento_formal BIT,
    -- 1 si tiene plan de entrenamiento formal
    conocimiento_herramientas FLOAT,
    -- auto-evaluación de conocimiento de herramientas (0-100)
    fecha_registro DATETIME DEFAULT GETDATE()
);

-- Encuestas de Onboarding
CREATE TABLE Encuesta_Onboarding (
    id_encuesta INT IDENTITY(1, 1) PRIMARY KEY,
    id_empleado INT UNIQUE FOREIGN KEY REFERENCES Empleado(id_empleado),
    encuesta_satisfaccion_reclutamiento FLOAT,
    -- satisfacción con proceso de hiring (1-5)
    encuesta_satisfaccion_induccion FLOAT,
    -- satisfacción con inducción (1-5)
    encuesta_satisfaccion_integracion FLOAT,
    -- satisfacción con integración (1-5)
    nps_primer_mes INT,
    -- Net Promoter Score en primer mes (0-10)
    cantidad_feedback_recibido INT,
    -- número de sesiones de feedback recibidas
    fecha_registro DATETIME DEFAULT GETDATE()
);

-- Métricas de Engagement
CREATE TABLE Metricas_Engagement (
    id_engagement INT IDENTITY(1, 1) PRIMARY KEY,
    id_empleado INT UNIQUE FOREIGN KEY REFERENCES Empleado(id_empleado),
    participacion_eventos INT,
    -- número de eventos corporativos a los que asistió
    conexiones_linkedin INT,
    -- número de conexiones con colegas en LinkedIn
    interaccion_comunidad_interna INT,
    -- participaciones en foros/canales internos
    tamanio_equipo INT,
    -- tamaño del equipo al que pertenece
    fecha_registro DATETIME DEFAULT GETDATE()
);