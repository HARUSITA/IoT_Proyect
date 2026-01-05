DROP DATABASE IF EXISTS sistema_escom;
CREATE DATABASE sistema_escom;
USE sistema_escom;

CREATE TABLE alumnos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    boleta VARCHAR(20) UNIQUE NOT NULL,
    nombre VARCHAR(100) NOT NULL,
    carrera VARCHAR(50) NOT NULL,
    password VARCHAR(50) NOT NULL, 
    rol VARCHAR(20) DEFAULT 'usuario'
);

CREATE TABLE vehiculos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    placas VARCHAR(15) UNIQUE NOT NULL,
    marca_modelo VARCHAR(100) NOT NULL,
    alumno_id INT,
    FOREIGN KEY (alumno_id) REFERENCES alumnos(id) ON DELETE CASCADE
);

CREATE TABLE historial (
    id INT AUTO_INCREMENT PRIMARY KEY,
    placa VARCHAR(15) NOT NULL,
    fecha_hora TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    alumno_nombre VARCHAR(100),
    tipo VARCHAR(10) NOT NULL
);

INSERT INTO alumnos (boleta, nombre, carrera, password, rol) 
VALUES ('admin', 'Administrador General', 'Sistemas', '123', 'admin');