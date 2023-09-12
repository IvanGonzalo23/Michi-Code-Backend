
CREATE SCHEMA IF NOT EXISTS michicode;

USE michicode;

CREATE TABLE IF NOT EXISTS usuarios (
    id INT NOT NULL UNIQUE AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) NOT NULL,
    nombre VARCHAR(255) NOT NULL,
    lastname VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    contrasenia VARCHAR(255) NOT NULL,
    fecha_de_nacimiento DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS servidores (
    id INT NOT NULL UNIQUE AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL,
    created_by INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (created_by) REFERENCES usuarios(id)
);

CREATE TABLE IF NOT EXISTS usuarios_servidores (
    id INT NOT NULL UNIQUE AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT NOT NULL,
    servidor_id INT NOT NULL,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id),
    FOREIGN KEY (servidor_id) REFERENCES servidores(id)
);

CREATE TABLE IF NOT EXISTS canales (
    id INT NOT NULL UNIQUE AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL,
    servidor_id INT NOT NULL,
    FOREIGN KEY (servidor_id) REFERENCES servidores(id)
);

CREATE TABLE IF NOT EXISTS mensajes (
    id INT NOT NULL UNIQUE AUTO_INCREMENT PRIMARY KEY,
    contenido TEXT NOT NULL,
    autor_id INT NOT NULL,
    canal_id INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (autor_id) REFERENCES usuarios(id),
    FOREIGN KEY (canal_id) REFERENCES canales(id)
);

