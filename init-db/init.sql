-- Crear base de datos 
CREATE DATABASE EmpresaDB; 
GO 

USE EmpresaDB; 
GO 

-- ==================================== 
-- TABLA DE DEPARTAMENTOS 
-- ==================================== 
CREATE TABLE Departamento ( 
    id_departamento INT IDENTITY(1,1) PRIMARY KEY, 
    nombre NVARCHAR(100) NOT NULL 
); 

-- ==================================== 
-- TABLA DE PUESTOS 
-- ==================================== 
CREATE TABLE Puesto ( 
    id_puesto INT IDENTITY(1,1) PRIMARY KEY, 
    nombre NVARCHAR(100) NOT NULL 
); 

-- ==================================== 
-- TABLA DE LOCACIONES 
-- ==================================== 
CREATE TABLE Locacion ( 
    id_locacion INT IDENTITY(1,1) PRIMARY KEY, 
    nombre NVARCHAR(100) NOT NULL 
); 

-- ==================================== 
-- TABLA DE EMPLEADOS 
-- ==================================== 
CREATE TABLE Empleado ( 
    id_empleado INT IDENTITY(1,1) PRIMARY KEY, 
    nombre NVARCHAR(100) NOT NULL, 
    email NVARCHAR(150) NOT NULL UNIQUE, 
    status NVARCHAR(50), 
    fecha_contratacion DATE, 
    id_puesto INT FOREIGN KEY REFERENCES Puesto(id_puesto), 
    id_departamento INT FOREIGN KEY REFERENCES Departamento(id_departamento), 
    id_locacion INT FOREIGN KEY REFERENCES Locacion(id_locacion) 
); 

-- ==================================== 
-- TABLA DE EQUIPOS 
-- ==================================== 
CREATE TABLE Equipo ( 
    id_equipo INT IDENTITY(1,1) PRIMARY KEY, 
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
    id_entrenamiento INT IDENTITY(1,1) PRIMARY KEY, 
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
    id_curso INT IDENTITY(1,1) PRIMARY KEY, 
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
    id_categoria INT IDENTITY(1,1) PRIMARY KEY, 
    nombre NVARCHAR(100) NOT NULL 
); 

-- ==================================== 
-- TABLA DE FEEDBACK 
-- ==================================== 
CREATE TABLE Feedback ( 
    id_feedback INT IDENTITY(1,1) PRIMARY KEY, 
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
    id_tarea INT IDENTITY(1,1) PRIMARY KEY, 
    descripcion NVARCHAR(200) NOT NULL 
); 

CREATE TABLE Equipo_Tarea ( 
    id_equipo INT FOREIGN KEY REFERENCES Equipo(id_equipo), 
    id_tarea INT FOREIGN KEY REFERENCES Tarea(id_tarea), 
    PRIMARY KEY (id_equipo, id_tarea) 
);

-- Insertar datos de ejemplo en Departamento
INSERT INTO Departamento (nombre) VALUES 
('Recursos Humanos'),
('Tecnología'),
('Ventas'),
('Marketing'),
('Finanzas');

-- Insertar datos de ejemplo en Puesto
INSERT INTO Puesto (nombre) VALUES 
('Gerente'),
('Desarrollador'),
('Analista'),
('Diseñador'),
('Contador');

-- Insertar datos de ejemplo en Locacion
INSERT INTO Locacion (nombre) VALUES 
('Ciudad de México'),
('Guadalajara'),
('Monterrey'),
('Querétaro'),
('Tijuana');