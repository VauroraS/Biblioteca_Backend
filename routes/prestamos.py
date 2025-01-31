from flask import Blueprint, request, jsonify
from models import Prestamo, Libro, Lector, Bibliotecario
from database import db

prestamos_bp = Blueprint('prestamos', __name__)

# Crear un nuevo préstamo
@prestamos_bp.route('/prestamos', methods=['POST'])
def create_prestamo():
    data = request.get_json()

    # Validación básica de datos
    if not all(key in data for key in ('id_libros', 'id_lectores', 'id_bibliotecarios', 'fecha_fin')):
        return jsonify({'error': 'Faltan datos obligatorios'}), 400

    # Verificar que el libro y lector existen
    libro = Libro.query.get(data['id_libros'])
    lector = Lector.query.get(data['id_lectores'])
    bibliotecario = Bibliotecario.query.get(data['id_bibliotecarios'])

    if not libro:
        return jsonify({'error': 'Libro no encontrado'}), 404
    if not lector:
        return jsonify({'error': 'Lector no encontrado'}), 404
    if not bibliotecario:
        return jsonify({'error': 'Bibliotecario no encontrado'}), 404

    # Crear el préstamo
    new_prestamo = Prestamo(
        id_libros=data['id_libros'],
        id_lectores=data['id_lectores'],
        id_bibliotecarios=data['id_bibliotecarios'],
        fecha_fin=data['fecha_fin']
    )
    db.session.add(new_prestamo)
    db.session.commit()

    return jsonify({'message': 'Préstamo creado'}), 201


# Obtener todos los préstamos
@prestamos_bp.route('/prestamos', methods=['GET'])
def get_prestamos():
    prestamos = Prestamo.query.all()
    result = [{
        "id": p.id_prestamos,
        "libro": p.libro.titulo,
        "lector": p.lector.nombre,
        "bibliotecario": p.bibliotecario.nombre,
        "fecha_inicio": p.fecha_inicio,
        "fecha_fin": p.fecha_fin,
        "estado": p.estado
    } for p in prestamos]
    return jsonify(result)

# Obtener un préstamo por ID
@prestamos_bp.route('/prestamos/<int:id>', methods=['GET'])
def get_prestamo(id):
    prestamo = Prestamo.query.get_or_404(id)
    return jsonify({
        "id": prestamo.id_prestamos,
        "libro": prestamo.libro.titulo,
        "lector": prestamo.lector.nombre,
        "bibliotecario": prestamo.bibliotecario.nombre,
        "fecha_inicio": prestamo.fecha_inicio,
        "fecha_fin": prestamo.fecha_fin,
        "estado": prestamo.estado
    })

# Actualizar un préstamo por ID
@prestamos_bp.route('/prestamos/<int:id>', methods=['PUT'])
def update_prestamo(id):
    prestamo = Prestamo.query.get_or_404(id)
    data = request.get_json()
    prestamo.id_libros = data['id_libros']
    prestamo.id_lectores = data['id_lectores']
    prestamo.id_bibliotecarios = data['id_bibliotecarios']
    prestamo.fecha_fin = data['fecha_fin']
    prestamo.estado = data.get('estado', prestamo.estado)
    db.session.commit()
    return jsonify({"message": "Préstamo actualizado"})

# Eliminar un préstamo por ID
@prestamos_bp.route('/prestamos/<int:id>', methods=['DELETE'])
def delete_prestamo(id):
    prestamo = Prestamo.query.get_or_404(id)
    db.session.delete(prestamo)
    db.session.commit()
    return jsonify({"message": "Préstamo eliminado"})
