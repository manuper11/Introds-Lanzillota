CREATE DATABASE IF NOT EXISTS flaskdb;
USE flaskdb;

CREATE TABLE IF NOT EXISTS Users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    rol VARCHAR(50) NOT NULL,
    password VARCHAR(255) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS Habitaciones (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(80) NOT NULL,
    descripcion VARCHAR(200),
    precio_noche DECIMAL(10, 2),
    url_imagen VARCHAR(150),
    personas_max INT NULL,
    cantidad_disponible INT DEFAULT 1
);

CREATE TABLE IF NOT EXISTS Reservas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email_cliente VARCHAR(100) NOT NULL,
    nombre_cliente VARCHAR(80) NOT NULL,
    telefono_cliente VARCHAR(20),
    fecha_desde DATE NOT NULL,
    fecha_hasta DATE NOT NULL,
    cantidad_habitaciones INT NOT NULL,
    cantidad_personas INT NOT NULL,
    metodo_pago VARCHAR(50),
    estado VARCHAR(50),
    motivo_rechazo VARCHAR(150),
    precio_total DECIMAL(10, 2),
    habitacion_id INT,
    codigo_reserva VARCHAR(10) NULL,
    FOREIGN KEY (habitacion_id) REFERENCES Habitaciones(id)
);

CREATE TABLE IF NOT EXISTS Reviews (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre_autor VARCHAR(80) NOT NULL,
    texto VARCHAR(150) NOT NULL,
    visible BOOLEAN DEFAULT false,
    estado VARCHAR(50) DEFAULT 'nueva',
    reserva_id INT NULL,
    FOREIGN KEY (reserva_id) REFERENCES Reservas(id)
);

-- Inserción de datos ficticios en la tabla Habitaciones
INSERT INTO Habitaciones (nombre, descripcion, precio_noche, personas_max,url_imagen) 
VALUES
    ('Suite Deluxe', 'Suite con vista al lago', 150.00, 4,'habitacion-1.jpg'),
    ('Suite Deluxe', 'Suite con vista al lago', 150.00, 4,'habitacion-2.jpg'),
    ('Habitación Doble', 'Habitación con dos camas individuales', 80.00, 2,'habitacion-3.jpg'),
    ('Habitación Simple', 'Habitación con una cama individual', 50.00, 1,'habitacion-4.jpg');

-- Inserción de datos ficticios en la tabla Reservas
INSERT INTO Reservas (email_cliente, nombre_cliente, telefono_cliente, fecha_desde, fecha_hasta, 
                      cantidad_habitaciones, cantidad_personas, metodo_pago, estado, motivo_rechazo, 
                      precio_total, habitacion_id, codigo_reserva) 
VALUES
    ('marting.riveiro@gmail.com', 'Cliente Uno', '123456789', '2024-05-01', '2024-05-07', 1, 2, 'Tarjeta de Crédito', 'pendiente', NULL, 560.00, 1, "1s"),
    ('tinchoriveiro@gmail.com', 'Cliente Dos', '987654321', '2024-07-10', '2024-07-15', 2, 4, 'Transferencia Bancaria', 'pendiente', NULL, 800.00, 2, "sa2"),
    ('tinchoriveiro@gmail.com', 'Cliente Tres', '123123123', '2024-08-01', '2024-08-05', 1, 1, 'Efectivo', 'pendiente', NULL, 200.00, 3, "ds54");

-- Inserción de datos ficticios en la tabla Reviews
INSERT INTO Reviews (nombre_autor, texto) 
VALUES
    ('Jacinto Perez', "Muy feo todo, chau."),
    ('Pandolfa Gervasia Meijidez', "Muy lindo todo, chau."),
    ('Pandolfo Gervasio Meijidez Anacleto', "Muy lindo todo, chau.");

