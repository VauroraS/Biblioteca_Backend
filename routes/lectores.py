from flask import Blueprint, request, jsonify
from models import Lector
from database import db

lectores_bp = Blueprint('lectores', __name__)

# Crear un nuevo lector
@lectores_bp.route('/lectores', methods=['POST'])
def create_lector():
    data = request.get_json()

    if 'nombre' not in data or 'email' not in data:
        return jsonify({'message': 'Nombre y email son obligatorios'}), 400

    new_lector = Lector(
        nombre=data['nombre'],
        email=data['email'],
        password=data.get('password', 'default_password'),
        estado=data.get('estado', 'activo'),
        deudor_contar=data.get('deudor_contar', 0),
        suspendido_hasta=data.get('suspendido_hasta', None)
    )
    db.session.add(new_lector)
    db.session.commit()
    return jsonify({'message': 'Lector creado con éxito','id': new_lector.id_lectores}), 201 # Incluye el ID del lector en la respuesta


# Obtener todos los lectores
@lectores_bp.route('/lectores', methods=['GET'])
def get_lectores():
    lectores = Lector.query.all()
    result = [
        {
            "id": l.id_lectores,
            "nombre": l.nombre,
            "email": l.email,
            "estado": l.estado,
            "deudor_contar": l.deudor_contar,
            "suspendido_hasta": l.suspendido_hasta
        } 
        for l in lectores
    ]
    return jsonify(result)

# Obtener un lector por ID
@lectores_bp.route('/lectores/<int:id>', methods=['GET'])
def get_lector(id):
    lector = Lector.query.get_or_404(id)
    return jsonify({
        "id": lector.id_lectores,
        "nombre": lector.nombre,
        "email": lector.email,
        "estado": lector.estado,
        "deudor_contar": lector.deudor_contar,
        "suspendido_hasta": lector.suspendido_hasta
    })

# Actualizar un lector por ID
@lectores_bp.route('/lectores/<int:id>', methods=['PUT'])
def update_lector(id):
    lector = Lector.query.get_or_404(id)
    data = request.get_json()
    lector.nombre = data['nombre']
    lector.email = data['email']
    lector.password = data['password']
    lector.estado = data['estado']
    lector.deudor_contar = data.get('deudor_contar', lector.deudor_contar)
    lector.suspendido_hasta = data.get('suspendido_hasta', lector.suspendido_hasta)
    db.session.commit()
    return jsonify({"message": "Lector actualizado"})

# Eliminar un lector por ID
@lectores_bp.route('/lectores/<int:id>', methods=['DELETE'])
def delete_lector(id):
    lector = Lector.query.get_or_404(id)
    db.session.delete(lector)
    db.session.commit()
    return jsonify({"message": "Lector eliminado"})

