from flask import Blueprint, request, jsonify
from models import Categoria
from database import db

categorias_bp = Blueprint('categorias', __name__)

# Crear una nueva categoría
@categorias_bp.route('/categorias', methods=['POST'])
def create_categoria():
    data = request.get_json()
    new_categoria = Categoria(nombre=data['nombre'])
    db.session.add(new_categoria)
    db.session.commit()
    return jsonify({'message': 'Categoría creada'}), 201

# Obtener todas las categorías
@categorias_bp.route('/categorias', methods=['GET'])
def get_categorias():
    categorias = Categoria.query.all()
    result = [{"id": c.id_categorias, "nombre": c.nombre} for c in categorias]
    return jsonify(result)

# Eliminar una categoría
@categorias_bp.route('/categorias/<int:id>', methods=['DELETE'])
def delete_categoria(id):
    categoria = Categoria.query.get_or_404(id)
    db.session.delete(categoria)
    db.session.commit()
    return jsonify({"message": "Categoría eliminada"})
