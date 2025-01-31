from datetime import datetime
from flask import Blueprint, request, jsonify
from models import Devolucion, Prestamo
from database import db

devoluciones_bp = Blueprint('devoluciones', __name__)

# Crear una nueva devolución
@devoluciones_bp.route('/devoluciones', methods=['POST'])
def create_devolucion():
    data = request.get_json()

    # Validar y convertir la fecha recibida en formato ISO 8601
    fecha_str = data.get('fecha')  # Ejemplo: '2025-01-27T12:35:17.845Z'
    try:
        fecha = datetime.fromisoformat(fecha_str.replace("Z", "+00:00")) if fecha_str else datetime.utcnow()
    except ValueError:
        return jsonify({'error': 'Formato de fecha inválido. Use ISO 8601 (YYYY-MM-DDTHH:MM:SS.mmmZ).'}), 400

    # Validar si el préstamo ya fue devuelto
    existing_devolucion = Devolucion.query.filter_by(id_prestamos=data['id_prestamos']).first()
    if existing_devolucion:
        return jsonify({'error': 'El préstamo ya fue devuelto'}), 400

    # Validar si el préstamo existe
    prestamo = Prestamo.query.get(data['id_prestamos'])
    if not prestamo:
        return jsonify({'error': 'Préstamo no encontrado'}), 404

    # Crear la devolución
    nueva_devolucion = Devolucion(
        id_prestamos=data['id_prestamos'],
        id_bibliotecarios=data.get('id_bibliotecarios'),
        fecha=fecha,
        comentario=data.get('comentario'),
    )
    db.session.add(nueva_devolucion)
    db.session.commit()

    return jsonify({'message': 'Devolución registrada correctamente'}), 201

# Obtener todas las devoluciones
@devoluciones_bp.route('/devoluciones', methods=['GET'])
def get_devoluciones():
    devoluciones = Devolucion.query.all()
    result = [{
        "id": d.id_devoluciones,
        "id_prestamos": d.id_prestamos,
        "id_bibliotecarios": d.id_bibliotecarios,
        "fecha": d.fecha,
        "comentario": d.comentario
    } for d in devoluciones]
    return jsonify(result)

# devolucion por id
@devoluciones_bp.route('/devoluciones/<int:id>', methods=['GET'])
def get_devolucion(id):
    devolucion = Devolucion.query.get_or_404(id)
    return jsonify({
        "id": devolucion.id_devoluciones,
        "id_prestamos": devolucion.id_prestamos,
        "id_bibliotecarios": devolucion.id_bibliotecarios,
        "fecha": devolucion.fecha,
        "comentario": devolucion.comentario
    })

# Eliminar una devolución
@devoluciones_bp.route('/devoluciones/<int:id>', methods=['DELETE'])
def delete_devolucion(id):
    devolucion = Devolucion.query.get_or_404(id)
    db.session.delete(devolucion)
    db.session.commit()
    return jsonify({"message": "Devolución eliminada"})


@devoluciones_bp.route('/devoluciones/<int:id>', methods=['PUT'])
def update_devolucion(id):
    devolucion = Devolucion.query.get_or_404(id)
    data = request.get_json()
    devolucion.id_prestamos = data['id_prestamos']
    devolucion.id_bibliotecarios = data['id_bibliotecarios']
    devolucion.fecha = data.get('fecha', devolucion.fecha)
    devolucion.comentario = data.get('comentario', devolucion.comentario)
    db.session.commit()
    return jsonify({"message": "Devolución actualizada"})