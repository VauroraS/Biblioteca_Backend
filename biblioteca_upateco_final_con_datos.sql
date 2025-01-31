CREATE DATABASE biblioteca_upateco_final;
USE biblioteca_upateco_final;

-- Tabla de bibliotecarios
CREATE TABLE bibliotecarios (
    id_bibliotecarios INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    estado ENUM('activo', 'suspendido') DEFAULT 'activo',
    creado_el DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Tabla de lectores
CREATE TABLE lectores (
    id_lectores INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    deudor_contar INT DEFAULT 0, -- Contador de deudas
    suspendido_hasta DATE DEFAULT NULL, -- Fecha de suspensión
    estado ENUM('activo', 'suspendido') DEFAULT 'activo',
    creado_el DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Tabla de categorías de libros
CREATE TABLE categorias (
    id_categorias INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL UNIQUE
);

-- Tabla de libros
CREATE TABLE libros (
    id_libros INT AUTO_INCREMENT PRIMARY KEY,
    titulo VARCHAR(200) NOT NULL,
    isbn VARCHAR(20) NOT NULL UNIQUE,
    autor VARCHAR(150) NOT NULL,
    editorial VARCHAR(150) NOT NULL,
    anio_publicacion INT NOT NULL,
    cantidad_total INT NOT NULL CHECK (cantidad_total >= 0),
    cantidad_disponible INT NOT NULL CHECK (cantidad_disponible >= 0),
    id_categorias INT NULL,
    creado_el DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_categorias) REFERENCES categorias(id_categorias)
        ON DELETE RESTRICT
        ON UPDATE CASCADE
);

-- Tabla de etiquetas
CREATE TABLE etiquetas (
    id_etiquetas INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL UNIQUE
);

-- Relación libros-etiquetas
CREATE TABLE libros_etiquetas (
    id_libros_etiquetas INT AUTO_INCREMENT PRIMARY KEY,
    id_libros INT NOT NULL,
    id_etiquetas INT NOT NULL,
    UNIQUE KEY (id_libros, id_etiquetas),
    FOREIGN KEY (id_libros) REFERENCES libros(id_libros)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    FOREIGN KEY (id_etiquetas) REFERENCES etiquetas(id_etiquetas)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

-- Tabla de préstamos
CREATE TABLE prestamos (
    id_prestamos INT AUTO_INCREMENT PRIMARY KEY,
    id_libros INT NOT NULL,
    id_lectores INT NOT NULL,
    id_bibliotecarios INT NOT NULL,
    fecha_inicio DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    fecha_fin DATE NOT NULL, -- Fecha de vencimiento del préstamo
    fecha_devolucion DATETIME DEFAULT NULL, -- Fecha de devolución del libro
    renovado BOOLEAN DEFAULT FALSE, -- Indica si el préstamo fue renovado
    estado ENUM('activo', 'vencido', 'devuelto') DEFAULT 'activo',
    FOREIGN KEY (id_libros) REFERENCES libros(id_libros)
        ON DELETE RESTRICT
        ON UPDATE CASCADE,
    FOREIGN KEY (id_lectores) REFERENCES lectores(id_lectores)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
	FOREIGN KEY (id_bibliotecarios) REFERENCES bibliotecarios(id_bibliotecarios)
		ON DELETE CASCADE
        ON UPDATE CASCADE
);

-- Tabla de devoluciones
CREATE TABLE devoluciones (
    id_devoluciones INT AUTO_INCREMENT PRIMARY KEY,
    id_prestamos INT NOT NULL, -- Relación con el préstamo
    id_bibliotecarios INT NOT NULL, -- Bibliotecario que gestionó la devolución
    fecha DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP, -- Fecha de la devolución
    comentario TEXT DEFAULT NULL, -- Comentarios adicionales
    FOREIGN KEY (id_prestamos) REFERENCES prestamos(id_prestamos)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    FOREIGN KEY (id_bibliotecarios) REFERENCES bibliotecarios(id_bibliotecarios)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

-- Tabla de reservas
CREATE TABLE reservas (
    id_reservas INT AUTO_INCREMENT PRIMARY KEY,
    id_libros INT NOT NULL,
    id_lectores INT NOT NULL,
    fecha_reserva DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    vencida BOOLEAN DEFAULT FALSE, -- Indica si la reserva está vencida
    FOREIGN KEY (id_libros) REFERENCES libros(id_libros)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    FOREIGN KEY (id_lectores) REFERENCES lectores(id_lectores)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);
-- Usar la base de datos
USE biblioteca_upateco_final;

-- Insertar datos en la tabla bibliotecarios
INSERT INTO bibliotecarios (nombre, email, password, estado) VALUES
('Juan Pérez', 'juan.perez@biblioteca.com', 'hashed_password1', 'activo'),
('María López', 'maria.lopez@biblioteca.com', 'hashed_password2', 'activo'),
('Carlos Sánchez', 'carlos.sanchez@biblioteca.com', 'hashed_password3', 'suspendido'),
('Ana Fernández', 'ana.fernandez@biblioteca.com', 'hashed_password4', 'activo');

-- Insertar datos en la tabla lectores
INSERT INTO lectores (nombre, email, password, deudor_contar, suspendido_hasta, estado) VALUES
('Pedro Gómez', 'pedro.gomez@lectores.com', 'hashed_password5', 0, NULL, 'activo'),
('Lucía Martínez', 'lucia.martinez@lectores.com', 'hashed_password6', 1, '2025-02-01', 'suspendido'),
('Miguel Torres', 'miguel.torres@lectores.com', 'hashed_password7', 0, NULL, 'activo'),
('Laura Díaz', 'laura.diaz@lectores.com', 'hashed_password8', 2, '2025-01-20', 'suspendido');

-- Insertar datos en la tabla categorias
INSERT INTO categorias (nombre) VALUES
('Ficción'), ('Ciencia Ficción'), ('Historia'), ('Biografía'),
('Fantasía'), ('Terror'), ('Misterio'), ('Educación'),
('Cómics'), ('Aventura'), ('Romance'), ('Ciencia'),
('Poesía'), ('Ensayo'), ('Política'), ('Religión'),
('Autoayuda'), ('Tecnología'), ('Arte'), ('Deportes');

-- Insertar datos en la tabla libros
INSERT INTO libros (titulo, isbn, autor, editorial, anio_publicacion, cantidad_total, cantidad_disponible, id_categorias) VALUES
('El señor de los anillos', '9780618260300', 'J.R.R. Tolkien', 'Allen & Unwin', 1954, 10, 8, 5), -- Fantasía
('1984', '9780451524935', 'George Orwell', 'Secker & Warburg', 1949, 15, 12, 1), -- Ficción
('Cien años de soledad', '9780060883287', 'Gabriel García Márquez', 'Harper & Row', 1967, 20, 15, 1), -- Ficción
('La sombra del viento', '9788490624291', 'Carlos Ruiz Zafón', 'Planeta', 2001, 12, 9, 7), -- Misterio
('Sapiens', '9780062316110', 'Yuval Noah Harari', 'Harper', 2014, 8, 6, 3), -- Historia
('El alquimista', '9780061122415', 'Paulo Coelho', 'HarperOne', 1988, 14, 10, 17), -- Autoayuda
('El código Da Vinci', '9780307474278', 'Dan Brown', 'Doubleday', 2003, 12, 11, 7), -- Misterio
('Harry Potter y la piedra filosofal', '9780747532743', 'J.K. Rowling', 'Bloomsbury', 1997, 20, 18, 5), -- Fantasía
('El Principito', '9780156012195', 'Antoine de Saint-Exupéry', 'Reynal & Hitchcock', 1943, 10, 9, 1), -- Ficción
('El arte de la guerra', '9781590302255', 'Sun Tzu', 'Shambhala', -500, 7, 5, 15); -- Política

-- Insertar datos en la tabla etiquetas
INSERT INTO etiquetas (nombre) VALUES
('Clásicos'), ('Bestsellers'), ('Novela gráfica'), ('Juvenil'),
('Literatura latinoamericana'), ('Historia universal'), ('Ciencia avanzada'),
('Mitos y leyendas'), ('Libros prácticos'), ('Ficción distópica');

-- Insertar datos en la tabla libros_etiquetas
INSERT INTO libros_etiquetas (id_libros, id_etiquetas) VALUES
(1, 1), (1, 8), (2, 10), (2, 1),
(3, 5), (4, 2), (5, 6), (6, 9);

-- Insertar datos en la tabla prestamos
INSERT INTO prestamos (id_libros, id_lectores, id_bibliotecarios, fecha_fin, estado) VALUES
(1, 1, 1, '2025-01-15', 'devuelto'),
(2, 2, 2, '2025-01-20', 'activo'),
(3, 3, 3, '2025-01-25', 'vencido'),
(4, 4, 4, '2025-02-01', 'activo');

-- Insertar datos en la tabla devoluciones
INSERT INTO devoluciones (id_prestamos, id_bibliotecarios, comentario) VALUES
(1, 1, 'Devuelto sin daños'),
(3, 2, 'Tarde, sin daños');

-- Insertar datos en la tabla reservas
INSERT INTO reservas (id_libros, id_lectores, vencida) VALUES
(2, 3, FALSE),
(4, 1, TRUE),
(5, 2, FALSE),
(6, 4, TRUE);
