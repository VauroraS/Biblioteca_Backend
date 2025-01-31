from flask import Blueprint, request, jsonify
from models import Etiqueta
from database import db

etiquetas_bp = Blueprint('etiquetas', __name__)

# Crear una nueva etiqueta
@etiquetas_bp.route('/etiquetas', methods=['POST'])
def create_etiqueta():
    data = request.get_json()
    if 'nombre' not in data:
        return jsonify({'error': 'El campo nombre es requerido'}), 400

    nueva_etiqueta = Etiqueta(nombre=data['nombre'])
    db.session.add(nueva_etiqueta)
    db.session.commit()
    return jsonify({'message': 'Etiqueta creada', 'id': nueva_etiqueta.id_etiquetas}), 201

# Obtener todas las etiquetas
@etiquetas_bp.route('/etiquetas', methods=['GET'])
def get_etiquetas():
    etiquetas = Etiqueta.query.all()
    result = [{"id": e.id_etiquetas, "nombre": e.nombre} for e in etiquetas]
    return jsonify(result)

# Eliminar una etiqueta
@etiquetas_bp.route('/etiquetas/<int:id>', methods=['DELETE'])
def delete_etiqueta(id):
    etiqueta = Etiqueta.query.get_or_404(id)
    db.session.delete(etiqueta)
    db.session.commit()
    return jsonify({"message": "Etiqueta eliminada"})

