-- Crear la base de datos
CREATE DATABASE HiTechGym;
USE HiTechGym;

-- Crear la tabla Usuario
CREATE TABLE Usuario (
    id_usuario INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    contraseña VARCHAR(255) NOT NULL,
    rol ENUM('cliente', 'administrador') NOT NULL
);

-- Crear la tabla Membresía
CREATE TABLE Membresia (
    id_membresia INT AUTO_INCREMENT PRIMARY KEY,
    id_usuario INT UNIQUE NOT NULL,
    tipo ENUM('mensual', 'anual') NOT NULL,
    precio DECIMAL(10,2) NOT NULL,
    fecha_inicio DATE NOT NULL,
    fecha_fin DATE NOT NULL,
    estado ENUM('activa', 'inactiva') NOT NULL DEFAULT 'activa',
    FOREIGN KEY (id_usuario) REFERENCES Usuario(id_usuario) ON DELETE CASCADE
);

-- Crear la tabla Pista
CREATE TABLE Pista (
    id_pista INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    ubicación VARCHAR(100) NOT NULL,
    estado ENUM('disponible', 'ocupada', 'mantenimiento') NOT NULL DEFAULT 'disponible'
);

-- Crear la tabla Reserva
CREATE TABLE Reserva (
    id_reserva INT AUTO_INCREMENT PRIMARY KEY,
    id_usuario INT NOT NULL,
    id_pista INT NOT NULL,
    fecha DATE NOT NULL,
    hora TIME NOT NULL,
    estado ENUM('confirmada', 'cancelada') NOT NULL DEFAULT 'confirmada',
    FOREIGN KEY (id_usuario) REFERENCES Usuario(id_usuario) ON DELETE CASCADE,
    FOREIGN KEY (id_pista) REFERENCES Pista(id_pista) ON DELETE CASCADE
);

-- Crear la tabla Pago
CREATE TABLE Pago (
    id_pago INT AUTO_INCREMENT PRIMARY KEY,
    id_usuario INT NOT NULL,
    id_membresia INT NOT NULL,
    monto DECIMAL(10,2) NOT NULL,
    fecha DATE NOT NULL,
    método ENUM('tarjeta', 'efectivo', 'PayPal') NOT NULL,
    FOREIGN KEY (id_usuario) REFERENCES Usuario(id_usuario) ON DELETE CASCADE,
    FOREIGN KEY (id_membresia) REFERENCES Membresia(id_membresia) ON DELETE CASCADE
);

-- Trigger para evitar que un usuario sin una membresía activa haga una reserva
DELIMITER //
CREATE TRIGGER before_insert_reserva
BEFORE INSERT ON Reserva
FOR EACH ROW
BEGIN
    DECLARE estado_membresia VARCHAR(20);
    
    -- Obtener el estado de la membresía del usuario
    SELECT estado INTO estado_membresia
    FROM Membresia
    WHERE id_usuario = NEW.id_usuario
    ORDER BY fecha_fin DESC
    LIMIT 1;
    
    -- Si no tiene membresía activa, bloquear la reserva
    IF estado_membresia IS NULL OR estado_membresia != 'activa' THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'No puedes reservar una pista sin una membresía activa';
    END IF;
END;
//
DELIMITER ;

