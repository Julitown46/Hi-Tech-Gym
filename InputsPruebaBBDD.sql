-- Insertar usuarios (clientes y administradores)
INSERT INTO Usuario (nombre, email, contrasena, rol) VALUES
('Carlos Pérez', 'carlos@email.com', 'hashed_password1', 'cliente'),
('Ana López', 'ana@email.com', 'hashed_password2', 'cliente'),
('David García', 'david@email.com', 'hashed_password3', 'administrador');

-- Insertar membresías para clientes (solo usuarios con membresía activa podrán reservar)
INSERT INTO Membresia (id_usuario, tipo, precio, fecha_inicio, fecha_fin, estado) VALUES
(1, 'mensual', 29.99, '2025-03-01', '2025-03-31', 'activa'),
(2, 'anual', 299.99, '2025-01-01', '2025-12-31', 'activa');

-- Insertar pistas de pádel
INSERT INTO Pista (nombre, ubicacion, estado) VALUES
('Pista 1', 'Zona A', 'disponible'),
('Pista 2', 'Zona B', 'disponible'),
('Pista 3', 'Zona C', 'mantenimiento');

-- Insertar pagos de membresías
INSERT INTO Pago (id_usuario, id_membresia, importe, fecha, metodo) VALUES
(1, 1, 29.99, '2025-03-01', 'tarjeta'),
(2, 2, 299.99, '2025-01-01', 'PayPal');

-- Insertar reservas de pistas de pádel (solo si el usuario tiene membresía activa)
INSERT INTO Reserva (id_usuario, id_pista, fecha, hora, estado) VALUES
(1, 1, '2025-03-10', '10:00', 'confirmada'),
(2, 2, '2025-03-12', '16:30', 'confirmada');

-- Prueba: Intentar hacer una reserva con un usuario sin membresía activa (esto fallará)
INSERT INTO Usuario (nombre, email, contrasena, rol) VALUES
('Pedro Sánchez', 'pedro@email.com', 'hashed_password4', 'cliente');

-- Intento de reserva con usuario sin membresía activa (debería fallar por el trigger)
INSERT INTO Reserva (id_usuario, id_pista, fecha, hora, estado) VALUES
(4, 1, '2025-03-15', '18:00:00', 'confirmada'); 
-- Esto dará error porque el usuario no tiene una membresía activa

