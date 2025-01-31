from flask import Blueprint, request, jsonify
from models import Reserva
from database import db

reservas_bp = Blueprint('reservas', __name__)

# Crear una nueva reserva
@reservas_bp.route('/reservas', methods=['POST'])
def create_reserva():
    data = request.get_json()

    # Verificar si el lector ya reservó el libro
    reserva_existente = Reserva.query.filter_by(
        id_libros=data['id_libros'],
        id_lectores=data['id_lectores']
    ).first()

    if reserva_existente:
        return jsonify({'error': 'El libro ya está reservado por este lector'}), 400

    # Crear nueva reserva
    new_reserva = Reserva(
        id_libros=data['id_libros'],
        id_lectores=data['id_lectores'],
        fecha_reserva=data.get('fecha_reserva'),
        vencida=data.get('vencida', False)
    )
    db.session.add(new_reserva)
    db.session.commit()

    return jsonify({'message': 'Reserva creada'}), 201

# Obtener todas las reservas
@reservas_bp.route('/reservas', methods=['GET'])
def get_reservas():
    reservas = Reserva.query.all()
    result = [{
        "id": r.id_reservas,
        "id_libros": r.id_libros,
        "id_lectores": r.id_lectores,
        "fecha_reserva": r.fecha_reserva,
        "vencida": r.vencida
    } for r in reservas]
    return jsonify(result)

# Actualizar una reserva
@reservas_bp.route('/reservas/<int:id>', methods=['PUT'])
def update_reserva(id):
    reserva = Reserva.query.get_or_404(id)
    data = request.get_json()
    reserva.id_libros = data['id_libros']
    reserva.id_lectores = data['id_lectores']
    reserva.fecha_reserva = data.get('fecha_reserva', reserva.fecha_reserva)
    reserva.vencida = data.get('vencida', reserva.vencida)
    db.session.commit()
    return jsonify({"message": "Reserva actualizada"})

# Eliminar una reserva
@reservas_bp.route('/reservas/<int:id>', methods=['DELETE'])
def delete_reserva(id):
    reserva = Reserva.query.get_or_404(id)
    db.session.delete(reserva)
    db.session.commit()
    return jsonify({"message": "Reserva eliminada"})
