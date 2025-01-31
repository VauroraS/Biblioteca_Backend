from datetime import datetime
from database import db

# Modelo para los bibliotecarios
class Bibliotecario(db.Model):
    __tablename__ = 'bibliotecarios'
    id_bibliotecarios = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    estado = db.Column(db.Enum('activo', 'suspendido', name='estado_bibliotecarios'), default='activo')
    creado_el = db.Column(db.DateTime, default=datetime.utcnow)

# Modelo para los lectores
class Lector(db.Model):
    __tablename__ = 'lectores'
    id_lectores = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    deudor_contar = db.Column(db.Integer, default=0)
    suspendido_hasta = db.Column(db.Date, nullable=True)
    estado = db.Column(db.Enum('activo', 'suspendido', name='estado_lectores'), default='activo')
    creado_el = db.Column(db.DateTime, default=datetime.utcnow)

# Modelo para los libros
class Libro(db.Model):
    __tablename__ = 'libros'
    id_libros = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(200), nullable=False)
    isbn = db.Column(db.String(20), unique=True, nullable=False)
    autor = db.Column(db.String(150), nullable=False)
    editorial = db.Column(db.String(150), nullable=False)
    anio_publicacion = db.Column(db.Integer, nullable=False)
    cantidad_total = db.Column(db.Integer, nullable=False)
    cantidad_disponible = db.Column(db.Integer, nullable=False)
    id_categorias = db.Column(db.Integer, db.ForeignKey('categorias.id_categorias'))
    creado_el = db.Column(db.DateTime, default=datetime.utcnow)

    categoria = db.relationship('Categoria', back_populates="libros")

# Modelo para las categorías de libros
class Categoria(db.Model):
    __tablename__ = 'categorias'
    id_categorias = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), unique=True, nullable=False)
    libros = db.relationship('Libro', back_populates="categoria")

# Modelo para los préstamos
class Prestamo(db.Model):
    __tablename__ = 'prestamos'
    id_prestamos = db.Column(db.Integer, primary_key=True)
    id_libros = db.Column(db.Integer, db.ForeignKey('libros.id_libros'))
    id_lectores = db.Column(db.Integer, db.ForeignKey('lectores.id_lectores'))
    id_bibliotecarios = db.Column(db.Integer, db.ForeignKey('bibliotecarios.id_bibliotecarios'))
    fecha_inicio = db.Column(db.DateTime, default=datetime.utcnow)
    fecha_fin = db.Column(db.Date, nullable=False)
    fecha_devolucion = db.Column(db.DateTime, nullable=True)
    renovado = db.Column(db.Boolean, default=False)
    estado = db.Column(db.Enum('activo', 'vencido', 'devuelto', name='estado_prestamos'), default='activo')

    libro = db.relationship('Libro')
    lector = db.relationship('Lector')
    bibliotecario = db.relationship('Bibliotecario')

# Modelo para las devoluciones
class Devolucion(db.Model):
    __tablename__ = 'devoluciones'
    id_devoluciones = db.Column(db.Integer, primary_key=True)
    id_prestamos = db.Column(db.Integer, db.ForeignKey('prestamos.id_prestamos'))
    id_bibliotecarios = db.Column(db.Integer, db.ForeignKey('bibliotecarios.id_bibliotecarios'))
    fecha = db.Column(db.DateTime, default=datetime.utcnow)
    comentario = db.Column(db.Text, nullable=True)

    prestamo = db.relationship('Prestamo')
    bibliotecario = db.relationship('Bibliotecario')

# Modelo para las reservas
class Reserva(db.Model):
    __tablename__ = 'reservas'
    id_reservas = db.Column(db.Integer, primary_key=True)
    id_libros = db.Column(db.Integer, db.ForeignKey('libros.id_libros'))
    id_lectores = db.Column(db.Integer, db.ForeignKey('lectores.id_lectores'))
    fecha_reserva = db.Column(db.DateTime, default=datetime.utcnow)
    vencida = db.Column(db.Boolean, default=False)

    libro = db.relationship('Libro')
    lector = db.relationship('Lector')

